from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import re

class F2SDCaptioner:
    def __init__(self,image:Image) -> None:
        self.__image = image
        self.__model = AutoModelForCausalLM.from_pretrained('gokaygokay/Florence-2-SD3-Captioner', trust_remote_code=True).eval()
        self.__processor = AutoProcessor.from_pretrained('gokaygokay/Florence-2-SD3-Captioner', trust_remote_code=True)

    def __modify_caption(self,caption: str) -> str:
        """
        Removes specific prefixes from captions if present, otherwise returns the original caption.
        Args:
            caption (str): A string containing a caption.
        Returns:
            str: The caption with the prefix removed if it was present, or the original caption.
        """
        # Define the prefixes to remove
        prefix_substrings = [
            ('captured from ', ''),
            ('captured at ', '')
        ]
        
        # Create a regex pattern to match any of the prefixes
        pattern = '|'.join([re.escape(opening) for opening, _ in prefix_substrings])
        replacers = {opening.lower(): replacer for opening, replacer in prefix_substrings}
        
        # Function to replace matched prefix with its corresponding replacement
        def replace_fn(match):
            return replacers[match.group(0).lower()]
        
        # Apply the regex to the caption
        modified_caption = re.sub(pattern, replace_fn, caption, count=1, flags=re.IGNORECASE)
        
        # If the caption was modified, return the modified version; otherwise, return the original
        return modified_caption if modified_caption != caption else caption
    

    def __call__(self):
        task_prompt = "<DESCRIPTION>"
        prompt = task_prompt + "Describe this image in great detail."

        if self.__image.mode != "RGB":
            self.__image.convert("RGB")

        inputs = self.__processor(text=prompt,images=self.__image,return_tensors="pt")
        gen_ids = self.__model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3
        )
        gen_text = self.__processor.batch_decode(gen_ids,skip_special_tokens=False)[0]
        parsed_answer = self.__processor.post_process_generation(gen_text, task=task_prompt, image_size=(self.__image.width, self.__image.height))
        return self.__modify_caption(parsed_answer["<DESCRIPTION>"])
    
if __name__ == "__main__":
    img = Image.open("./inputs/004.png")
    cap = F2SDCaptioner(image=img)()