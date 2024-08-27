import classifier.classifier as classifier
import renderer.renderer as renderer
from PIL import Image
import os
from transformers import pipeline
from PIL import Image


captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


# renderer.render_meshes_from_scene('./renderer/cafeteria.glb', './render')

# --------------------------------------------------------------------

directory_path = 'render'
all_entries = os.listdir(directory_path)
files = [f for f in all_entries if os.path.isfile(os.path.join(directory_path, f))]
files = sorted(files)

# print(files)

classify_image = classifier.load_image_classifier()
for file in files:
    image = Image.open(file)
    result = captioner(image)
    print(file, result)


# image_path = "./example.png"
# top_prediction = classify_image(image_path)
# print("Top prediction:", top_prediction)

# image = Image.open("./example.png")
# top_prediction = classify_image(image)

# print("Top prediction:", top_prediction)
