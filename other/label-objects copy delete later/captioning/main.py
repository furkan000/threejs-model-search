# Use a pipeline as a high-level helper
from transformers import pipeline
import gradio as gr


captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

# result = captioner("https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png")
# print(result)

demo = gr.Interface(
    captioner,
    gr.Image(type="pil"),
    "text"
)

demo.launch()