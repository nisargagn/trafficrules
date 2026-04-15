import tkinter as tk
import tkinter as tk
import os
import webbrowser
from tkinter import messagebox
from tkinter import filedialog, messagebox
from tkinter import filedialog, messagebox
from ultralytics import YOLO
import os, shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import ImageTk, Image
import cv2
import matplotlib.pyplot as plt

from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
class Page2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.background_image = tk.PhotoImage(file="bg.png")  # Replace with your image path
        # Create a label to display the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
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
        Button(self, text="Predict Violation",
               width=22, bg="#6A1B9A", fg="white",
               font=("Arial", 12, "bold"),
               command=self.openGUI).pack(pady=10)

        Button(self, text="Number plate Detection ",
               width=22, bg="#6A1B9A", fg="white",
               font=("Arial", 12, "bold"),
               command=self.openNumberplate).pack(pady=10)

    def openGUI(self):

        import sys, subprocess
        subprocess.Popen([sys.executable, "yologui2.py"])



    def openNumberplate(self):
        import sys, subprocess
        subprocess.Popen([sys.executable, "newGUIWith_ocr.py"])
