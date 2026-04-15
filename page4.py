import tkinter as tk
import os
from tkinter import messagebox, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SENDER_EMAIL = "myprojectemails4u@gmail.com"
SENDER_PASSWORD = "joriikysgfbptiuv"

# SMTP Server details
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

class Page4(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.background_image = tk.PhotoImage(file="bg.png")  # Replace with your image path
        # Create a label to display the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Recipient Email
        tk.Label(self, text="Recipient Email:", font=("Arial", 12)).pack(pady=5)
        self.recipient_entry = tk.Entry(self, width=40)
        self.recipient_entry.pack(pady=5)

        # Subject
        tk.Label(self, text="Subject:", font=("Arial", 12)).pack(pady=5)
        self.subject_entry = tk.Entry(self, width=40)
        self.subject_entry.pack(pady=5)

        # Message Body
        tk.Label(self, text="Message:", font=("Arial", 12)).pack(pady=5)
        self.message_text = tk.Text(self, width=40, height=10)
        self.message_text.pack(pady=5)

        # Select Image Button
        self.image_path = None
        select_image_button = tk.Button(self, text="Attach Image", command=self.select_image)
        select_image_button.pack(pady=5)

        # Send Email Button
        send_button = tk.Button(self, text="Send Email", command=self.send_email)
        send_button.pack(pady=20)

    def select_image(self):
        # Open file dialog to select an image
        self.image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if self.image_path:
            messagebox.showinfo("File Selected", f"Selected: {os.path.basename(self.image_path)}")
        else:
            messagebox.showwarning("No File", "No file selected!")

    def send_email(self):
        recipient = self.recipient_entry.get()
        subject = self.subject_entry.get()
        message_body = self.message_text.get("1.0", tk.END)

        if not recipient or not subject or not message_body.strip():
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message_body, 'plain'))

            # Attach the selected image
            if self.image_path:
                with open(self.image_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(self.image_path)}"
                )
                msg.attach(part)

            # Send the email
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, recipient, msg.as_string())

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")