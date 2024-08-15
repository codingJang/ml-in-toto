import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import torch
from net import Net

class App:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.root.geometry("350x206")

        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=200, height=200, bg="black")
        self.canvas.grid(row=0, column=0, rowspan=4)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Predict Button
        self.predict_button = tk.Button(root, text="Predict", command=self.predict)
        self.predict_button.grid(row=0, column=1)

        # Clear Button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=1)

        # Label to display the prediction result
        self.result_label = tk.Label(root, text="Draw a digit", font=('Helvetica', 16))
        self.result_label.grid(row=2, column=1)

        # Label to display the confidence score
        self.confidence_label = tk.Label(root, text="", font=('Helvetica', 12))
        self.confidence_label.grid(row=3, column=1)

        # Create a blank image for drawing
        self.image = Image.new("L", (200, 200), 0)
        self.draw = ImageDraw.Draw(self.image)
    
    def paint(self, event):
        x1, y1 = (event.x - 10), (event.y - 10)
        x2, y2 = (event.x + 10), (event.y + 10)
        self.canvas.create_oval(x1, y1, x2, y2, fill="white", width=0)
        self.draw.ellipse([x1, y1, x2, y2], fill="white")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (200, 200), 0)
        self.draw = ImageDraw.Draw(self.image)
        self.result_label.config(text="Draw a digit")
        self.confidence_label.config(text="")

    def predict(self):
        # Preprocess the image
        image = self.image.resize((28, 28))
        image = np.array(image).astype(np.float32)
        image = torch.tensor(image).unsqueeze(0).unsqueeze(0)
        image = image / 255.0

        # Get model prediction
        with torch.no_grad():
            output = self.model(image)
            prediction = output.argmax(dim=1, keepdim=True).item()
            confidence = torch.max(torch.softmax(output, dim=1)).item() * 100

            # Update the result label with the prediction and confidence
            self.result_label.config(text=f"Predicted Digit: {prediction}")
            self.confidence_label.config(text=f"Confidence: {confidence:.2f}%")

model = Net()
model.load_state_dict(torch.load('models/mnist_cnn.pt'))
model.eval()

root = tk.Tk()
app = App(root, model)
root.mainloop()
