import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model('animalRecognitionCNN')
print('model loaded')

classes = ['cat', 'chicken', 'cow', 'dog', 'horse', 'sheep', 'squirrel', 'deer']

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def predict_image(img_path):
    processed_img = preprocess_image(img_path)
    predictions = model.predict(processed_img)
    predicted_class = np.argmax(predictions, axis=1)[0]
    return classes[predicted_class]

# Open file search
def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if filepath:
        img = Image.open(filepath)
        img = img.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk
        
        prediction = predict_image(filepath)
        result_label.config(text=f"{prediction}")

root = tk.Tk()
root.title("Animal predictor")

# Select image button
btn = tk.Button(root, text="Select an Image", command=open_file)
btn.pack(pady=10)

# Image panel
panel = tk.Label(root)
panel.pack()

# Prediction
result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

root.mainloop()