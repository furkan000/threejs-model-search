import classifier.classifier as classifier
import renderer.renderer as renderer
from PIL import Image











classify_image = classifier.load_image_classifier()

image_path = "./example.png"
top_prediction = classify_image(image_path)
print("Top prediction:", top_prediction)

image = Image.open("./example.png")
top_prediction = classify_image(image)

print("Top prediction:", top_prediction)
