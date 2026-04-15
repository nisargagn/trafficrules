import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL for handling images
from PIL import ImageTk, Image

class Page1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.background_image = tk.PhotoImage(file="bg.png")  # Replace with your image path
        # Create a label to display the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title = tk.Label(self, text="Traffic Rules Violations", font=("Arial", 24), bg="white")
        title.pack(pady=10)

        # Description label
        description = tk.Label(self, text="The traffic rules violation detection system is an "
                                          "advanced technology that can identify and analyze traffic"
                                          "violations using computer vision techniques. The system"
                                          "uses cameras installed at traffic junctions to capture"
                                          "images and videos of vehicles violating traffic rules."
                                          "These images and videos are then processed using"
                                          "artificial intelligence algorithms to detect and classify the"
                                          "type of violation, such as jumping a red light, overspeeding, or lane violation. The system can also generate"
                                          "automated alerts and notifications to law enforcement"
                                          "agencies to take action against the violators. The system"
                                          "helps in reducing the number of accidents and improving"
                                          "overall road safety by enforcing traffic rules and"
                                          "regulations",
                               font=("Arial", 14), bg="white", wraplength=800, justify="center")
        description.pack(pady=10)

        # Displaying an image
        try:
            # Open the image file and resize it
            image = Image.open("homepageimg.png")  # Replace with your image path
            image = image.resize((350, 250), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self, image=image_tk, bg="white")
            image_label.image = image_tk  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(self, text="Image could not be loaded.", font=("Arial", 12), bg="white", fg="red")
            error_label.pack(pady=10)
            print(f"Error loading image: {e}")

        # Additional content or links
        more_info = tk.Label(self, text="Explore more by navigating through the sidebar!",
                             font=("Arial", 12), bg="white")
        more_info.pack(pady=20)
