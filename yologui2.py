import tkinter as tk
import webbrowser
from tkinter import filedialog, Label, Button, Canvas, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import random
from ultralytics import YOLO

# ========================= CONFIGURATION ==========================
# Directory where your YOLO models are stored
MODEL_DIR = "models"
# Base directory for violation images (folders)
DATASET_PATH = "images"

# Maps violation folder name (key) to the model file name (value)
# The full path will be constructed as: MODEL_DIR / MODEL_FILENAME
MODEL_MAPPING = {
    # Ensure your folder names exactly match these keys
    "helmat_overload": "helmate_overload_best.pt",
    "mobile": "mobilebest.pt",
    "no parking": "noparkingbest.pt",
    "one way": "onewaybest.pt",
    "seatbelt": "seatbeltbest.pt",
    "stunts": "stuntbest.pt",
    # Add other mappings if you have them
}


# ========================= GUI CLASS ================================
class TrafficViolationPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Rule Violation Predictor (YOLOv8)")
        self.root.geometry("1300x850")
        self.root.config(bg="#f0f0f0")

        self.image_path = None
        self.current_yolo_model = None  # To store the loaded model instance

        # --- Initial Setup ---
        self.violation_folders = self.get_violation_folders()

        # ---------- HEADER ----------
        header = tk.Frame(root, bg="#000066", height=60)
        header.pack(fill="x")
        Label(header, text="Traffic Rule Violation Predictor (YOLOv8)", bg="#000066",
              fg="white", font=("Arial", 24, "bold")).pack(pady=10)

        # ---------- MAIN FRAME ----------
        self.main_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # =====================================================================
        # LEFT PANEL
        # =====================================================================
        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.left_frame.pack(side="left", padx=20, pady=20, fill="y")

        # IMAGE CANVAS
        self.image_canvas = Canvas(self.left_frame, width=350, height=350,
                                   bg="#e0e0e0", bd=2, relief="solid")
        self.image_canvas.pack(pady=10)

        self.placeholder_label = Label(self.image_canvas, text="No Image Selected",
                                       bg="#e0e0e0", fg="gray", font=("Arial", 12))
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

        # -------- UPLOAD BUTTON --------
        Button(self.left_frame, text="Upload Image", width=22,
               command=self.upload_image, bg="#2196F3", fg="white",
               font=("Arial", 12, "bold")).pack(pady=10)

        # -------- VIOLATION/FOLDER DROPDOWN --------
        Label(self.left_frame, text="Select Violation (Folder)", bg="white",
              font=("Arial", 12, "bold")).pack(pady=(20, 5))

        self.violation_combo = ttk.Combobox(self.left_frame, width=22,
                                            font=("Arial", 12), state="readonly")
        # Populate with folder names
        self.violation_combo["values"] = self.violation_folders
        self.violation_combo.pack()

        # Set a default value if folders exist
        if self.violation_folders:
            self.violation_combo.set(self.violation_folders[0])
        else:
            self.violation_combo.set("No Folders Found")

        # -------- GET RANDOM IMAGE BUTTON --------
        Button(self.left_frame, text="Get Random Image",
               width=22, bg="#6A1B9A", fg="white",
               font=("Arial", 12, "bold"),
               command=self.get_random_image).pack(pady=10)

        # -------- PREDICT BUTTON --------
        self.predict_button = Button(self.left_frame, text="Predict",
                                     width=22, bg="#FFC107", fg="black",
                                     font=("Arial", 12, "bold"),
                                     state=tk.DISABLED,
                                     command=self.predict_image)
        self.predict_button.pack(pady=10)

        # -------- CLOSE BUTTON --------
        Button(self.left_frame, text="Close", width=22,
               bg="#F44336", fg="white",
               font=("Arial", 12, "bold"),
               command=self.root.destroy).pack(pady=20)

        # =====================================================================
        # RIGHT PANEL (RESULTS & GRAPH)
        # =====================================================================
        self.right_frame = tk.Frame(self.main_frame, bg="white")
        self.right_frame.pack(side="right", padx=20, pady=20,
                              fill="both", expand=True)

        self.result_label = Label(self.right_frame, text="Prediction Result:",
                                  bg="white", font=("Arial", 16, "bold"))
        self.result_label.pack(anchor="w")

        self.confidence_label = Label(self.right_frame, text="Confidence: N/A",
                                      bg="white", font=("Arial", 14))
        self.confidence_label.pack(anchor="w", pady=(0, 10))

        # GRAPH
        self.fig, self.ax = plt.subplots(figsize=(6, 3.5))
        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas_mpl.get_tk_widget().pack(fill="both", expand=True)

        # INFO BOX
        info_frame = tk.Frame(self.right_frame, bg="white")
        info_frame.pack(fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(info_frame)
        scrollbar.pack(side="right", fill="y")

        Label(info_frame, text="Violation Info:", bg="white", font=("Arial", 12, "bold")).pack(anchor="w")

        self.info_text = tk.Text(
            info_frame, height=10, wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            bg="#F9F9F9"
        )
        self.info_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.info_text.yview)

    # =====================================================================
    # HELPER METHODS
    # =====================================================================
    def get_violation_folders(self):
        """Finds all subdirectories (folders) in the DATASET_PATH."""
        if os.path.exists(DATASET_PATH):
            folders = [f for f in os.listdir(DATASET_PATH)
                       if os.path.isdir(os.path.join(DATASET_PATH, f))]
            return folders
        return []

    def load_selected_model(self, violation_type):
        """Loads the YOLO model based on the selected violation type."""
        model_filename = MODEL_MAPPING.get(violation_type)
        if not model_filename:
            messagebox.showerror("Model Error", f"No model file defined for folder: {violation_type}")
            return None

        # CONSTRUCT THE FULL PATH TO THE MODEL
        model_file_path = os.path.join(MODEL_DIR, model_filename)

        try:
            # Check if the desired model is already loaded
            if self.current_yolo_model and self.current_yolo_model.ckpt_path == model_file_path:
                return self.current_yolo_model

            # Load the new model
            model = YOLO(model_file_path)
            self.current_yolo_model = model
            return model

        except Exception as e:
            messagebox.showerror("Model Error", f"Cannot load model from path: {model_file_path}\nError: {e}")
            return None

    # =====================================================================
    # IMAGE HANDLING (methods remain the same)
    # =====================================================================
    def load_and_display(self, path):
        img = Image.open(path).resize((350, 350))
        self.image_path = path

        self.photo = ImageTk.PhotoImage(img)
        self.image_canvas.delete("all")
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.photo)

        try:
            self.placeholder_label.destroy()
        except:
            pass

        self.predict_button.config(state=tk.NORMAL)
        self.clear_graph()

    def upload_image(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if file:
            self.load_and_display(file)

    def get_random_image(self):
        folder = self.violation_combo.get()

        if folder == "No Folders Found":
            messagebox.showerror("Error", "No image folders found in the 'images' directory.")
            return

        if not folder or folder not in self.violation_folders:
            messagebox.showerror("Error", "Please select a valid violation folder.")
            return

        folder_path = os.path.join(DATASET_PATH, folder)

        imgs = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

        if not imgs:
            messagebox.showerror("Error", f"No images in the folder: {folder}")
            return

        selected = random.choice(imgs)
        full_path = os.path.join(folder_path, selected)
        self.load_and_display(full_path)

    # =====================================================================
    # YOLO PREDICTION (method remains the same, but uses the updated model loader)
    # =====================================================================
    def clear_graph(self):
        self.ax.clear()
        self.ax.set_title("Prediction Confidence")
        self.canvas_mpl.draw()

    def predict_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload or select a random image first.")
            return

        selected_violation = self.violation_combo.get()
        # This will now load the model from the 'models/' directory
        yolo_model = self.load_selected_model(selected_violation)

        if not yolo_model:
            return

        try:
            label_names_dict = yolo_model.names
            label_names = [label_names_dict[i] for i in sorted(label_names_dict.keys())]
        except Exception as e:
            messagebox.showerror("Model Info Error", f"Could not retrieve class names from model: {e}")
            label_names = []

        # ---------------- RUN PREDICTION ----------------
        try:
            results = yolo_model.predict(self.image_path, save=False, conf=0.25)[0]
        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred during prediction: {e}")
            return

        boxes = results.boxes

        predicted_label = "No Object Detected"
        confidence = 0
        probs = np.zeros(len(label_names))

        # ---------------- SHOW ANNOTATED IMAGE ----------------
        try:
            annotated_np = results.plot()
            annotated_np = annotated_np[..., ::-1]
            annotated_pil = Image.fromarray(annotated_np)
            annotated_pil = annotated_pil.resize((350, 350), Image.LANCZOS)

            self.annotated_photo = ImageTk.PhotoImage(annotated_pil)
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.annotated_photo)

        except Exception as e:
            print("ANNOTATION ERROR:", e)
            messagebox.showwarning("Annotation Warning", "Could not annotate image. Displaying raw image.")

        # ---------------- PROCESS YOLO PREDICTION ----------------
        if boxes and len(boxes) > 0:
            best_idx = boxes.conf.argmax()
            cls = int(boxes.cls[best_idx])

            if cls < len(label_names):
                predicted_label = label_names[cls]
                confidence = float(boxes.conf[best_idx]) * 100
                probs[cls] = confidence / 100
            else:
                predicted_label = f"Class ID {cls} (Unknown for this model)"

        # ------- Update UI -------
        model_used = os.path.join(MODEL_DIR, MODEL_MAPPING.get(selected_violation, 'N/A'))
        self.result_label.config(
            text=f"Prediction Result ({selected_violation.replace('_', ' ').title()}): {predicted_label}")
        self.confidence_label.config(text=f"Confidence: {confidence:.2f}%")

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Model Path Used: {model_used}\n"
                                      f"Source Folder: {selected_violation}\n\n"
                                      f"Highest Predicted Class: {predicted_label}")

        # ------- Graph Update -------
        self.ax.clear()

        if len(label_names) > 0:
            self.ax.bar(label_names, probs, color="#307FE2")
            self.ax.set_ylim(0, 1)
            self.ax.set_title(f"Confidence for {selected_violation}")
            if len(label_names) > 5:
                self.ax.tick_params(axis='x', rotation=45)
            self.fig.tight_layout()
        else:
            self.ax.text(0.5, 0.5, "No class data available for the graph.",
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax.transAxes)

        self.canvas_mpl.draw()


# ======================== RUN APP =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficViolationPredictorApp(root)
    root.mainloop()