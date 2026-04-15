from ultralytics import YOLO
import os, shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import pyttsx3
#pip install pyttsx3
# Initialize the TTS engine
engine = pyttsx3.init()
# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 4.0)  # Volume (0.0 to 1.0)
# Initialize GUI
np.set_printoptions(suppress=True)
top = tk.Tk()
top.geometry('1000x600')  # Adjust width for better layout
top.title('Machine Detection')
#img = PhotoImage(file='1.png', master=top)
#img_label = Label(top, image=img)
#img_label.place(x=0, y=0)

# Global variable to hold the file path of the uploaded image
uploaded_file_path = ""

# Function to classify image and display confidence score and class name
def classify():
    global uploaded_file_path

    if uploaded_file_path == "":
        confidence_label.configure(text='No image uploaded!', fg='red')
        class_label.configure(text='No prediction available', fg='red')
        return

    path = "output"
    if os.path.exists(path):
        # If directory exists, delete it
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

    model = YOLO("best.pt")

    # Update class names
    model.names[0] = "red apple"
    model.names[1] = "nice orange"

    results = model.predict(source=uploaded_file_path, project="output", save=True, save_txt=True, conf=0.5)

    # Extract the top prediction and confidence score
    result = results[0]
    boxes = result.boxes  # YOLO v8 returns boxes and their confidences

    if len(boxes) > 0:
        # Get the highest confidence prediction
        top_index = np.argmax(boxes.conf.numpy())  # Get the index of the highest confidence
        top_confidence = boxes.conf[top_index].item()  # Get the confidence score
        predicted_class = model.names[int(boxes.cls[top_index].item())]  # Get the class name

        # Display result image
        filename = os.path.splitext(os.path.basename(uploaded_file_path))[0]
        print("Predicted file path:" + "output/predict/" + filename + ".jpg")
        im = Image.open(r"output/predict/" + filename + ".jpg")
        im.save("output/predict/predictedimage.jpg")
        # cv2.imwrite("output/predict/predictedimage.jpg",im)
        # predicted_image_path = os.path.join(output_path, "predict", os.listdir(os.path.join(output_path, "predict"))[0])
        uploaded = Image.open("output/predict/predictedimage.jpg")
        uploaded.thumbnail((top.winfo_width() // 2, top.winfo_height() // 2))
        im = ImageTk.PhotoImage(uploaded)
        resultimg.configure(image=im)
        resultimg.image = im

        # Display confidence score and predicted class
        confidence_label.configure(text=f'Confidence: {top_confidence:.2f}', fg='green')
        class_label.configure(text=f'Predicted Class: {predicted_class}', fg='green')
        if predicted_class != "Helmet":
            engine.say("Rules Violated :"+predicted_class)
        # Run the speech
        engine.runAndWait()
    else:
        confidence_label.configure(text='No detections', fg='red')
        class_label.configure(text='No prediction available', fg='red')

# Upload image function
def upload_image():
    global uploaded_file_path
    try:
        uploaded_file_path = filedialog.askopenfilename(title="Select an image file",
                            filetypes=[("Image Files", "*.jpg;*.png"), ("JPG files", "*.jpg"), ("PNG files", "*.png")])  # Store the file path
        if uploaded_file_path:  # If a file was selected
            uploaded = Image.open(uploaded_file_path)
            uploaded.thumbnail(((top.winfo_width() / 3), (top.winfo_height() / 3)))  # Resize image for better layout
            im = ImageTk.PhotoImage(uploaded)
            sign_image.configure(image=im)
            sign_image.image = im
            label.configure(text='Image uploaded! Now click "Classify Image" to classify it.', fg='black')
            confidence_label.configure(text='Confidence: N/A')  # Reset confidence label
            class_label.configure(text='Predicted Class: N/A')  # Reset class label
        else:
            label.configure(text='No image selected.', fg='red')
    except Exception as e:
        print(f"Error: {e}")

# Instruction label
label = Label(top, font=('Helvetica', 12), bg='#F0F0F0', fg='#555555')
label.grid(row=6, column=0, columnspan=2, pady=20)

# Label for uploaded image
sign_image = Label(top, bg='#F0F0F0')
sign_image.grid(row=3, column=0, padx=30, pady=20)

# Label for result image
resultimg = Label(top, bg='#F0F0F0')
resultimg.grid(row=3, column=1, padx=30, pady=20)

# Confidence score label
confidence_label = Label(top, text="Confidence: N/A", font=('Helvetica', 14), bg='#F0F0F0', fg='#000000')
confidence_label.grid(row=4, column=0, columnspan=2, pady=10)

# Predicted class label
class_label = Label(top, text="Predicted Class: N/A", font=('Helvetica', 14), bg='#F0F0F0', fg='#000000')
class_label.grid(row=5, column=0, columnspan=2, pady=10)

# Upload Image Button
upload = Button(top, text="Upload Image", command=upload_image, padx=15, pady=10)
upload.configure(background='#5E81AC', foreground='white', font=('Helvetica', 14, 'bold'), relief="flat", borderwidth=0)
upload.grid(row=7, column=0, padx=20, pady=10)

# Classify Image Button
classify_button = Button(top, text="Classify Image", command=classify, padx=15, pady=10)
classify_button.configure(background='#5E81AC', foreground='white', font=('Helvetica', 14, 'bold'), relief="flat", borderwidth=0)
classify_button.grid(row=7, column=1, padx=20, pady=10)

# Heading with clean, large font
heading = Label(top, text="Traffic Rules Violations", pady=20, font=('Helvetica', 30, 'bold'))
heading.configure(background='#F0F0F0', foreground='#2E3440')
heading.grid(row=0, column=0, columnspan=2)

# Center the layout
top.grid_columnconfigure(0, weight=1)
top.grid_columnconfigure(1, weight=1)
top.grid_rowconfigure(0, weight=1)
top.grid_rowconfigure(1, weight=1)
top.grid_rowconfigure(2, weight=1)
top.grid_rowconfigure(3, weight=1)
top.grid_rowconfigure(4, weight=1)
top.grid_rowconfigure(5, weight=1)
top.grid_rowconfigure(6, weight=1)
top.grid_rowconfigure(7, weight=1)

# Run the GUI loop
top.mainloop()
