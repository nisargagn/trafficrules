from ultralytics import YOLO
model=YOLO("best.pt")
model.predict(mode="predict", model="best.pt", show=True,conf=0.5, source="3722268869-preview.mp4")