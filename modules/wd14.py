# used wd-swinv2-tagger-v3-hf
from PIL import Image
from optimum.pipelines import pipeline

class WD14Tagger:
    def __init__(self,image:Image) -> None:
        self.__img = image

        # pipeline
        # used onnx
        self.__pipe = pipeline(
            task="image-classification",
            model="p1atdev/wd-swinv2-tagger-v3-hf",
            trust_remote_code=True,
        )
    
    def __call__(self,top_k:int=20):
        return ",".join([item["label"] for item in self.__pipe(self.__img, top_k=top_k) if ":" not in item['label']])
    

# if __name__ == "__main__":
#     img = Image.open("./inputs/003.png")
#     tg = WD14Tagger(img)
#     print(tg())