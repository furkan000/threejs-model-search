import torch
from datasets import load_dataset
from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification
import gradio as gr
from transformers import AutoImageProcessor, MobileViTV2ForImageClassification


# Load the dataset and image processor
dataset = load_dataset("huggingface/cats-image")
image = dataset["test"]["image"][0]

preprocessor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")
model = MobileViTV2ForImageClassification.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")

# Create a Gradio interface
def classify_image(input_image):
    inputs = preprocessor(input_image, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    # Model predicts one of the 1000 ImageNet classes
    predicted_label = logits.argmax(-1).item()
    return model.config.id2label[predicted_label]

iface = gr.Interface(fn=classify_image, inputs="image", outputs="text")
iface.launch()
