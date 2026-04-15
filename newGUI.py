import pytesseract
from ultralytics import YOLO
import os, cv2, re
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from PIL import ImageTk, Image
import numpy as np
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyttsx3
#import python_to_arduino
# Initialize GUI window
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech (default is 200)
engine.setProperty('volume', 1.0)  # Volume (ranges from 0.0 to 1.0)
top = tk.Tk()
top.geometry('1500x800')
top.title('Number Plate Recognition')

# Background image
img = PhotoImage(file='bg.png', master=top)
img_label = Label(top, image=img)
img_label.place(x=0, y=0)

# Create directory for predicted images
save_dir = "predicted_image"
os.makedirs(save_dir, exist_ok=True)

# Load YOLO model
model = YOLO("best.pt")

np.set_printoptions(suppress=True)

label1=ttk.Label(top, text="Enter Vehicle numeber", font= ('Century 16 bold'))
label1.place(relx=0.50, rely=0.65)
entry= ttk.Entry(top,font=('Century 12 bold'),width=20)
entry.place(relx=0.50, rely=0.70)
# Complaints dropdown
complaints = ["Speeding", "Illegal Parking", "Signal Jumping", "Wrong Lane", "No Helmet"]
complaint_var = StringVar(top)
complaint_var.set("Select Complaint")
complaint_menu = ttk.Combobox(top, textvariable=complaint_var, values=complaints, state="readonly", width=30)
complaint_menu.place(relx=0.50, rely=0.75)

# Date selection
def show_calendar():
    top_calendar = Toplevel(top)
    cal = Calendar(top_calendar, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)

    def select_date():
        selected_date.set(cal.get_date())
        top_calendar.destroy()

    select_btn = Button(top_calendar, text="Select Date", command=select_date)
    select_btn.pack()

selected_date = StringVar(top)
date_label = Label(top, text="Select Date:", font=('arial', 10, 'bold'))
date_label.place(relx=0.50, rely=0.80)
date_button = Button(top, text="Choose Date", command=show_calendar)
date_button.place(relx=0.60, rely=0.80)

# Function to send email
def send_email(vemail, vnumber, complaint, date):
    sender_email = "myprojectemails4u@gmail.com"
    sender_password = "cyaoslrmrystypcm"
    subject = "Violation Email"
    message = f"Complaint: {complaint}\nDate: {date}\nVehicle Number: {vnumber}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = vemail
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    engine.say(message)
    engine.runAndWait()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Alert", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Display vehicle information and send email
df = pd.read_csv('data.csv')

def display_info(vnumber):
    if vnumber in df['number'].values:
        row = df[df['number'] == vnumber].iloc[0]

        messagebox.showinfo("sms Alert", "sms send successfully!")
        send_email(row['email'], row['number'])
    else:

        messagebox.showinfo("Alert", "Vehicle number not found!")

def extract_letters_numbers(s):
    return ''.join(re.findall(r'[A-Za-z0-9]', s))

def browse_and_predict(file_path):
    '''
    if complaint_var.get() == "Select Complaint" or not selected_date.get():
        messagebox.showinfo("Alert", "Please select both a complaint and a date!")
        return
    if not file_path:
        return
    '''
    # Run prediction
    results = model.predict(source=file_path, conf=0.5, save=False)

    # Process results and save cropped annotations
    for result in results:
        img = cv2.imread(file_path)
        for i, box in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box)  # Get bounding box coordinates
            cropped_img = img[y1:y2, x1:x2]  # Crop the image
            save_path = os.path.join(save_dir, f"cropped_{i}.jpg")
            cv2.imwrite(save_path, cropped_img)  # Save cropped image

    display_cropped_image()


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    filtered_image = cv2.medianBlur(binary_image, 3)
    return filtered_image

def extract_handwritten_text(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image, config='--psm 6')
    return text

def display_cropped_image():

    cropped_images = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]
    if cropped_images:
        first_cropped_path = os.path.join(save_dir, cropped_images[0])
        img = Image.open(first_cropped_path)
        img = img.resize((350, 250), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        resultimg.configure(image=img_tk)
        resultimg.image = img_tk
        text = extract_handwritten_text(first_cropped_path)
        filtered_text = extract_letters_numbers(text)
        messagebox.showinfo("Extracted Number", filtered_text)
        entry.insert(0, text)
        #classify_b = Button(top, text="Detect Number plate", command=lambda: detect_number_plate(), padx=10,  pady=5)
        #classify_b.configure(background='Red', foreground='Black', font=('arial', 10, 'bold'))
        #classify_b.place(relx=0.30, rely=0.75)

def detect_number_plate():
    if complaint_var.get() == "Select Complaint" or not selected_date.get():
        messagebox.showinfo("Alert", "Please select both a complaint and a date!")
        return
    if entry.get()=="":
        messagebox.showinfo("Alert", "Please enter Vehicle number")
        return
    text = entry.get()
    filtered_text = extract_letters_numbers(text)
    messagebox.showinfo("Extracted Number", filtered_text)
    display_info(filtered_text)

def show_classify_button(file_path):
    classify_b = Button(top, text="Detect Number plate", command=lambda: browse_and_predict(file_path), padx=10, pady=5)
    classify_b.configure(background='Red', foreground='Black', font=('arial', 10, 'bold'))
    classify_b.place(relx=0.30, rely=0.75)

def webcam_live():
    cap = cv2.VideoCapture(0)
    model = YOLO('best.pt')
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        results = model.predict(mode="predict", model="best.pt", conf=0.80, source=frame)
        # Display the frame
        annotatedimg = results[0].plot()
        cv2.imshow('Webcam Live Feed', annotatedimg)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    if not file_path:
        print("Error: No file selected.")
        return

    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Load YOLO model
    model = YOLO('best.pt')

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)  # Calculate delay based on fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video or error reading frame.")
                break

            # Run prediction
            results = model.predict(source=frame, conf=0.80, save=False)

            # Annotate and display the frame
            annotatedimg = results[0].plot()
            cv2.imshow('Video Frame', annotatedimg)

            # Exit on pressing 'q'
            if cv2.waitKey(frame_delay) & 0xFF == ord('q'):  # Use calculated delay
                break
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released successfully.")

def contactus():
    os.system("python contactus.py")

def capture_image():
    print("Capturing image")
    cap = cv2.VideoCapture(0)  # Open webcam
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        messagebox.showinfo("Success", "Image Captured Successfully!")
        uploaded = Image.open("captured_image.jpg")
        uploaded.thumbnail(((top.winfo_width() / 3.25), (top.winfo_height() / 3.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button("captured_image.jpg")


    else:
        messagebox.showerror("Error", "Failed to Capture Image")
    cap.release()

def upload_image():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 3.25), (top.winfo_height() / 3.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        #show_classify_button(file_path)
        browse_and_predict(file_path)

    except:
        pass

label = Label(top, background='white', font=('arial', 15, 'bold'))
sign_image = Label(top)
sign_image.place(relx=0.30, rely=0.26)

resultimg = Label(top)
resultimg.place(relx=0.60, rely=0.26)



upload = Button(top, text="Upload Vehicle Image", padx=10, pady=5, command=upload_image)
upload.configure(background='Red', foreground='Black', font=('arial', 10, 'bold'),width=20, height=2)
upload.place(relx=0.05, rely=0.50)


contact = Button(top, text="Contact us", padx=10, pady=5, command=contactus)
contact.configure(background='Red', foreground='Black', font=('arial', 10, 'bold'),width=20, height=2)
contact.place(relx=0.05, rely=0.80)

default_bg = Image.new("RGB", (250, 250), (200, 200, 200))
default_bg = ImageTk.PhotoImage(default_bg)

heading = Label(top, text="Number Plate Recognition", pady=20, font=('arial', 20, 'bold'))
heading.configure(background=None, foreground='Red')
heading.pack()

top.mainloop()
