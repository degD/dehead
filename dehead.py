
from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFilter
import cv2
import os
import shutil
import random

PROJECT_DIR = Path(__file__).parent
MODEL_PATH = PROJECT_DIR / "best.pt"
BLUR_RADIUS = 42

class Dehead: 
    """A class for deheading videos using a specified threshold and options for output formatting."""
    def __init__(self,
        input_paths: list[Path],
        output_paths: list[Path] = None,
        threshold: float = 0.2,
        boxes: bool = False,
        mask_scale: float = 1.2,
        solid_mask: bool = False,
        keep_audio: bool = False,
    ):
        self.input_paths = input_paths
        self.output_paths = output_paths
        self.threshold = threshold
        self.boxes = boxes
        self.mask_scale = mask_scale
        self.solid_mask = solid_mask
        self.keep_audio = keep_audio

        if self.output_paths is None or len(self.output_paths) != len(self.input_paths):
            self.output_paths = [
                input_path.parent / (input_path.name.split(".")[0] + "-dehead" + input_path.suffix) for input_path in self.input_paths
            ]

    def process_img(self, input_path: Path, output_path: Path = None):
        model = YOLO(MODEL_PATH)
        model.conf = self.threshold
        if output_path is None:
            try:
                output_path = self.output_paths[self.input_paths.index(input_path)]
            except ValueError:
                raise ValueError("Input path not found in the list of input paths. Please provide a valid output path.")

        with Image.open(input_path) as img:
            results = model(input_path)
            masks =  results[0].boxes.xywh.tolist()
            for mask in masks:

                box = [
                    int(mask[0] - mask[2] * self.mask_scale / 2),
                    int(mask[1] - mask[3] * self.mask_scale / 2),
                    int(mask[0] + mask[2] * self.mask_scale / 2),
                    int(mask[1] + mask[3] * self.mask_scale / 2),
                ]

                if self.solid_mask:
                    draw = ImageDraw.Draw(img)
                    if self.boxes:
                        draw.rectangle(box, fill="black")
                    else:
                        draw.ellipse(box, fill="black")
                else:
                    blur_mask = Image.new("L", img.size, 0)
                    blur_mask_draw = ImageDraw.Draw(blur_mask)
                    if self.boxes:
                        blur_mask_draw.rectangle(box, fill="white")
                    else:
                        blur_mask_draw.ellipse(box, fill="white")
                    blurred_img = img.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
                    img.paste(blurred_img, mask=blur_mask)

            img.save(output_path)

    def process_video(self, input_path: Path, output_path: Path = None):
        vidcap = cv2.VideoCapture(str(input_path))
        model = YOLO(MODEL_PATH)
        model.conf = self.threshold
        if output_path is None:
            try:
                output_path = self.output_paths[self.input_paths.index(input_path)]
            except ValueError:
                raise ValueError("Input path not found in the list of input paths. Please provide a valid output path.")
            
        frames_input_path = output_path.parent / f"{random.randint(0, 100000)}-frames"
        os.mkdir(frames_input_path)

        success, image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite(str(frames_input_path / f"frame{count}.jpg"), image)
            success, image = vidcap.read()
            count += 1

        frames_output_path = output_path.parent / f"{random.randint(0, 100000)}-frames-dehead"
        os.mkdir(frames_output_path)
        for i in range(count):
            self.process_img(frames_input_path / f"frame{i}.jpg", frames_output_path / f"frame{i}.jpg")
        shutil.rmtree(frames_input_path)

        frame = cv2.imread(str(frames_output_path / "frame0.jpg"))
        height, width, _ = frame.shape
        output_video =  cv2.VideoWriter(str(output_path), 0, 1, (width, height))

        for i in range(count):
            frame = cv2.imread(str(frames_output_path / f"frame{i}.jpg"))
            output_video.write(frame)
            os.remove(frames_output_path / f"frame{i}.jpg")
        shutil.rmtree(frames_output_path)

        cv2.destroyAllWindows()
        output_video.release()

    def process(self):
        if self.input_paths[0].suffix.lower() in [".jpg", ".jpeg", ".png"]:
            for i in range(len(self.input_paths)):
                self.process_img(self.input_paths[i])
        elif self.input_paths[0].suffix.lower() in [".mp4", ".avi", ".mov"]:
            for i in range(len(self.input_paths)):
                self.process_video(self.input_paths[i])
        else:
            raise ValueError("Unsupported file format. Supported formats are: .jpg, .jpeg, .png, .mp4, .avi, .mov")

if __name__ == "__main__":
    Dehead(
        input_paths=[PROJECT_DIR / "demo/vid.mp4"],
        output_paths=[PROJECT_DIR / "demo/family-dehead.mp4"],
        threshold=0.2,
        mask_scale=0.8,
        boxes=False,
        solid_mask=False,
    ).process()