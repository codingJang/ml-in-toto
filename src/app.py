import tkinter as tk
import numpy as np
from PIL import Image, ImageOps, ImageDraw
import torch
from net import Net

class App:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.button = tk.Button(root, text="Predict", command=self.predict)
        self.button.pack()
        self.image = Image.new("L", (200, 200), 255)
        self.draw = ImageDraw.Draw(self.image)
    
    def paint(self, event):
        x1, y1 = (event.x - 10), (event.y - 10)
        x2, y2 = (event.x + 10), (event.y + 10)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=10)
        self.draw.ellipse([x1, y1, x2, y2], fill="black")

    def predict(self):
        # Preprocess the image
        image = self.image.resize((28, 28))
        image = ImageOps.invert(image)
        image = np.array(image).astype(np.float32)
        image = torch.tensor(image).unsqueeze(0).unsqueeze(0)
        image = image / 255.0

        # Get model prediction
        with torch.no_grad():
            output = self.model(image)
            prediction = output.argmax(dim=1, keepdim=True).item()
            print(f"Predicted digit: {prediction}")

model = Net()
model.load_state_dict(torch.load('model/model.pt'))
root = tk.Tk()
app = App(root, model)
root.mainloop()
