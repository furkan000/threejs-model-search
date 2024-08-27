import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Ensure CUDA is available
if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available. Please ensure you have a compatible GPU and the necessary drivers installed.")

# Set the device to CUDA
device = torch.device("cuda")

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Move the model to the GPU
model.to(device)

def caption_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    # Move the input tensors to the GPU
    inputs = {key: value.to(device) for key, value in inputs.items()}

    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # Filter the caption
    caption = caption.lstrip('a ').lstrip('an ')
    phrases_to_remove = [
        'on a white background', 'with a white background', 'a white background', 'white background'
    ]
    for phrase in phrases_to_remove:
        caption = caption.replace(phrase, '')
    caption = caption.strip()

    return caption

def rename_images_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            base_name, ext = os.path.splitext(filename)

            # Check if the file already contains a caption
            if "_" in base_name:
                potential_caption = base_name.split("_")[-1]
                if potential_caption.isalpha():
                    print(f"Skipping already labeled file '{filename}'")
                    continue

            image_path = os.path.join(folder_path, filename)
            caption = caption_image(image_path)
            new_filename = f"{base_name}_{caption}{ext}"
            new_path = os.path.join(folder_path, new_filename)
            os.rename(image_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

# Specify the folder containing images
folder_path = "render_classroom"

# Rename the images with captions
rename_images_in_folder(folder_path)
