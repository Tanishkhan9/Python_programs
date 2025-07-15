# Image Captioning
from transformers import BlipProcessor,  BlipForConditionalGeneration
from PIL import Image
import requests
import gradio as gr
import torch
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
def caption_image(image):
  inputs = processor(image,return_tensors="pt")
  output = model.generate(**inputs)
  return processor.decode(output[0], skip_special_tokens=True)
gr.Interface(fn=caption_image, inputs=gr.Image(type="pil"),outputs="text",title="Image Captioning").launch(share = True)