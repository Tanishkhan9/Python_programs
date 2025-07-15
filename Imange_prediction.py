#gradio :- Build Gui for ml model/api,torch pytorch Deep Learning Networks,torchvision: pretrained Image model Like resent pillow :image Handling


#import required LIBs
import gradio as gr
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from PIL import Image
import torch
import urllib.request

#load pretarined resnet 50 and set to eval mode
model=models.resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

#load Imagene class labels
LABELS_URL="https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_classes=urllib.request.urlopen(LABELS_URL).read().decode("UTF-8").splitlines()

# step 5 Define Image Preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])



#step 6 Define prediction function
def predict(img):
  if not isinstance(img, Image.Image):
    img=Image.fromarray(img)
  img = preprocess(img).unsqueeze(0)
  with torch.no_grad():
    output = model(img)
  _, index = output[0].max(0)
  label = imagenet_classes[index.item()]
  return f"Predicted:{label}(class index:{index.item()})"

  # Lanuch Gradio App (GUI)
gr.Interface(fn=predict, inputs=gr.Image(type="pil"),outputs="text",title="AI Object Classifier(Imagenet)").launch(share=True)