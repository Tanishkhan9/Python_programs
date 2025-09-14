# Video Captioning with BLIP
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import cv2
import gradio as gr
import torch

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_video(video_path, frame_skip=30):
    """
    video_path: uploaded video file path
    frame_skip: process 1 frame every N frames (default=30 ~ 1 per sec for 30fps video)
    """
    cap = cv2.VideoCapture(video_path)
    captions = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            # Convert frame (OpenCV -> PIL)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            inputs = processor(image, return_tensors="pt")
            output = model.generate(**inputs)
            caption = processor.decode(output[0], skip_special_tokens=True)
            captions.append(caption)

        frame_count += 1

    cap.release()

    # Join captions into a simple description
    return " | ".join(captions)

# Gradio interface
demo = gr.Interface(
    fn=caption_video,
    inputs=gr.Video(),
    outputs="text",
    title="Video Captioning with BLIP"
)

demo.launch(share=True)
