from ultralytics import YOLO

if __name__ == "__main__":
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO("yolov8n.pt")

    print("lol1")
    results = model.train(data="datasets\\tram_sim.v2\\data.yaml", epochs=60)

    print("lol2")
    results = model.val()
