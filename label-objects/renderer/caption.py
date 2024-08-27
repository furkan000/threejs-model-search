import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs)
    result = processor.decode(out[0], skip_special_tokens=True)
    
    # Filter out unwanted phrases
    if result.startswith('a '):
        result = result[2:]
    if result.startswith('an '):
        result = result[3:]
    result = result.replace('on a white background', '')
    result = result.replace('with a white background', '')
    result = result.replace('a white background', '')
    result = result.replace('white background', '')
    result = result.strip()

    return result

def get_mesh_id(filename):
    parts = filename.split('_')
    return int(parts[2]), int(parts[3])

def generate_mesh_name(captions):
    prompt = "Based on these captions from different perspectives, provide a single, short name for the 3D mesh:\n"
    prompt += "\n".join(captions)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10
    )
    return response.choices[0].text.strip()

def main():
    folder_path = 'path_to_your_folder'
    mesh_captions = {}

    for filename in os.listdir(folder_path):
        if filename.startswith('rendered_mesh_'):
            mesh_id, camera_id = get_mesh_id(filename)
            image_path = os.path.join(folder_path, filename)
            caption = generate_caption(image_path)
            
            if mesh_id not in mesh_captions:
                mesh_captions[mesh_id] = []
            mesh_captions[mesh_id].append(caption)

    mesh_names = {}
    for mesh_id, captions in mesh_captions.items():
        mesh_name = generate_mesh_name(captions)
        mesh_names[mesh_id] = mesh_name

    print(mesh_names)

if __name__ == "__main__":
    main()
