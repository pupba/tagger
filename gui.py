import gradio as gr
import pandas as pd
import os
from PIL import Image

# module
from modules.log import logging

# theme
from theme.themes import small_and_pretty

class WebUI:
    def __init__(self,img_path:str="./inputs",save_path:str="./outputs",default_tag_path:str="./default.xlsx"):
        # img
        if not img_path.endswith("/"):
            self.__img_path=img_path+"/"
        else:
            self.__img_path = img_path
        self.__imgs = [(Image.open(self.__img_path+i),i) for i in os.listdir(self.__img_path) if i!=".DS_Store" and (i.endswith(".jpg") or i.endswith(".png"))]
        # output
        if not save_path.endswith("/"):
            self.__save_path=save_path+"/"
        else:
            self.__save_path = save_path

        df = pd.read_excel(default_tag_path)
        # default value
        self.__genre:list = df.loc[:,'장르'].dropna().to_list()
        self.__character:list = df.loc[:,'캐릭터'].dropna().to_list()
        self.__style:list = df.loc[:,'스타일'].dropna().to_list()
        self.__cam_shot:list = df.loc[:,'카메라샷'].dropna().to_list()
        self.__cam_move:list = df.loc[:,'카메라 무빙'].dropna().to_list()
        
        self.__filename = None
        self.__demo = None
        self.__gui()

    def __tagging(self,image:Image,genre:str,character:str,style:str,cam_shot:str,cam_move:str,add_tags:str,progress=gr.Progress()):
        try:
            if len(add_tags) != 0:
                add_tags = ","+add_tags
            tags = f"{genre},{character},{style},{cam_shot},{cam_move}{add_tags}"
            filename = f"{self.__filename.split('.')[0]}.txt"
            image.save(f"{self.__save_path}{self.__filename}")
            with open(f"{self.__save_path}{filename}","w+") as f:
                f.write(tags)
            gr.Info("태깅 완료")
        except Exception as e:
            logging.error(e)
            gr.Warning("태깅 실패... log 확인")


    def __imgSet(self,data:gr.SelectData):
        self.__filename = self.__imgs[data.index][1]
        return self.__imgs[data.index][0]

    def __tag_model(self,image:Image,tagger:str| None):
        if tagger == None:
            return ""
        elif tagger == "wd-14":
            from modules.wd14 import WD14Tagger
            tags = WD14Tagger(image=image)()
            return tags
        elif tagger == "Florence-2-SD3-Captioner": # GPU 필요
            from modules.F2SDCap import F2SDCaptioner
            tags = F2SDCaptioner(image=image)()
            return tags
    def __reaload(self):
        imgs = [(Image.open(self.__img_path+i),i) for i in os.listdir(self.__img_path) if i!=".DS_Store" and (i.endswith(".jpg") or i.endswith(".png"))]
        return imgs
    def __gui(self):
        # -------- GUI -----------
        with gr.Blocks(title="수동 Tagging",theme=small_and_pretty) as demo:
            with gr.Tab("태깅") as t1:
                # 왼쪽 이미지
                with gr.Row() as r1:
                    with gr.Column() as r1c1:
                        gallery = gr.Gallery(self.__imgs,format="png",height="auto")
                # 오른쪽 설정
                with gr.Row() as r2:
                    with gr.Column() as r2c1:
                        image = gr.Image(None,format="png",width="100%",type="pil")
                    with gr.Column() as r2c2:
                        reload = gr.Button("🌀 Image Reload..")
                        reload.click(fn=self.__reaload,inputs=None,outputs=gallery)
                        genre = gr.Radio(self.__genre,value=self.__genre[0],label="장르")
                        character = gr.Radio(self.__character,value=self.__character[0],label="캐릭터")
                        style = gr.Radio(self.__style,value=self.__style[0],label="스타일")
                        cam_shot = gr.Radio(self.__cam_shot,value=self.__cam_shot[0],label="카메라 샷")
                        cam_move = gr.Radio(self.__cam_move,value=self.__cam_move[0],label="카메라 무빙")
                        add_tags = gr.Text(label="추가 프롬프트",placeholder="콤마로 구분해서 입력하세요. ex. shirt,bag,...")
                        # tagger model
                        import torch
                        if torch.cuda.is_available():
                            taggers = [None,"wd-14","Florence-2-SD3-Captioner"]
                        else:
                            taggers = [None,"wd-14"]
                        tagger = gr.Radio(taggers)
                        tag_btn = gr.Button("Use Model tagging")
                        tag_btn.click(fn=self.__tag_model,inputs=[image,tagger],outputs=[add_tags])
                        # button
                        btn = gr.Button("Start Tagging!",variant="primary")
                gallery.select(fn=self.__imgSet,inputs=None,outputs=[image])
                btn.click(fn=self.__tagging,inputs=[image,genre,character,style,cam_shot,cam_move,add_tags],outputs=None,api_name="tagging")
            with gr.Tab("설명서") as t2:
                with open("./guide/guidebook.html","r") as f:
                    html = f.read()
                HTML = gr.HTML(html)

        self.__demo = demo

    def run(self,config:dict):
        self.__demo.launch(**config)

# if __name__ == "__main__":
#     WebUI().run({
#         "server_name": None,
#         "server_port": None,
#         "share":False
#     })
