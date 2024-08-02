import os
import pandas as pd
import gradio as gr
from PIL import Image
# 분류 기준대로 분류

class ClassSorter:
    def __init__(self) -> None:
        df = pd.read_excel("./default.xlsx")
        self.__genre:list = df.loc[:,'장르'].dropna().to_list()
        self.__character:list = df.loc[:,'캐릭터'].dropna().to_list()
        self.__depo:list = df.loc[:,'데포르메'].dropna().to_list()
        self.__color:list = df.loc[:,"컬러"].dropna().to_list()
        self.__style:list = df.loc[:,'스타일'].dropna().to_list()
        self.__cam_shot:list = df.loc[:,'카메라샷'].dropna().to_list()
        self.__cam_move:list = df.loc[:,'카메라 무빙'].dropna().to_list()

    def __file_load(self,target_path:str)->list:
        def read_f(path:str):
            with open(path,"r") as f:
                tags = f.read()
            return tags.split(",")
        
        caps = [i for i in os.listdir(target_path) if i.endswith(".txt")]
        imgs = [i for i in os.listdir(target_path) if (i.endswith(".jpg") or i.endswith(".png")) and i.split(".")[0]+".txt" in caps]
        files = [(img,Image.open(target_path+img),read_f(target_path+cap)) for cap in caps for img in imgs if cap[:-4] == img[:-4]]
        return files

    def __selected(self,target_path:str,root:str,select:str)->None: 
        if select == "장르":
            kinds = self.__genre
        elif select == "캐릭터":
            kinds = self.__character
        elif select == "그림체":
            kinds = self.__style
        elif select == "데포르메":
            kinds = self.__depo
        elif select == "컬러":
            kinds = self.__color
        elif select == "카메라 샷":
            kinds = self.__cam_shot
        elif select == "카메라 무빙":
            kinds = self.__cam_move
        
        files = self.__file_load(target_path)

        # dir 생성
        for kind in kinds:
            PATH = root+kind+"/"
            os.mkdir(PATH)
            for f,img,cap in files:
                if kind in cap:
                    img.save(PATH+f)
                    with open(PATH+f.split(".")[0]+".txt","w") as f:
                        f.write(",".join(cap))

        gr.Info("Sucess...")

    def __classfifcation(self,target_path:str,save_path:str,select:str)->None:
        if target_path == "":
            target_path = "./outputs/"
        
        if not target_path.endswith("/"):
            target_path += "/"
        if not save_path.endswith("/"):
            save_path += "/"
        try:
            if not os.path.isdir(target_path):
                raise FileNotFoundError 
            
            os.makedirs(save_path,exist_ok=True) # 없는 경우 생성

            self.__selected(target_path,save_path,select)
        except FileExistsError:
            print("디렉토리가 없습니다.")

    def gui(self):
        with gr.Row() as demo:
            target_path = gr.Text(None,placeholder="분류할 폴더를 지정, 아무것도 입력 안할 시 ./outputs 지정",label="타겟 위치")
            save_path = gr.Text(None,placeholder="저장 경로를 입력해주세요.(절대 경로!)",label="저장 위치")
            # options
            select = gr.Radio(["장르","캐릭터","그림체","데포르메","컬러","카메라 샷","카메라 무빙"],label="분류 기준")
            btn = gr.Button("분류하기",variant="primary")

            btn.click(fn=self.__classfifcation,inputs=[target_path,save_path,select])