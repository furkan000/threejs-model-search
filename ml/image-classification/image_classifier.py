import torch
from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification
from PIL import Image

def load_image_classifier():
    preprocessor = EfficientNetImageProcessor.from_pretrained("google/efficientnet-b0")
    model = EfficientNetForImageClassification.from_pretrained("google/efficientnet-b0")

    def classify_image(input_image):
        if isinstance(input_image, str):
            # If input_image is a string, assume it's a file path and load the image using PIL
            image = Image.open(input_image)
        elif isinstance(input_image, Image.Image):
            # If input_image is already a PIL Image, use it directly
            image = input_image
        else:
            raise ValueError("Input must be a file path (str) or a PIL Image")

        # Ensure the image has 3 channels (RGB)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert the image to a PyTorch tensor and normalize it
        image = preprocessor(images=image, return_tensors="pt")["pixel_values"]

        # Make predictions
        with torch.no_grad():
            logits = model(image).logits

        # Get the top prediction label
        predicted_label = logits.argmax(-1).item()
        top_prediction = model.config.id2label[predicted_label]

        return top_prediction

    return classify_image

if __name__ == "__main__":
    # You can add test code here if needed
    pass
