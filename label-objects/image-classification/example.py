from image_classifier import load_image_classifier
from PIL import Image

# Load the image classifier function
classify_image = load_image_classifier()

# Example 1: Provide a file path as input
image_path = "./example.png"
top_prediction = classify_image(image_path)
print("Top prediction:", top_prediction)


# Example 2: Provide a PIL Image as input
image = Image.open("./example.png")
top_prediction = classify_image(image)

# Print the top prediction
print("Top prediction:", top_prediction)
