
from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFilter
import cv2
import os
import shutil

PROJECT_DIR = Path(__file__).parent
MODEL_PATH = PROJECT_DIR / "best.pt"
BLUR_RADIUS = 42
BATCH_SIZE = 16

class Dehead: 
    """A class for deheading images using a specified threshold and options for output formatting."""
    def __init__(self,
        input_paths: list[Path],
        output_paths: list[Path] = None,
        threshold: float = 0.2,
        boxes: bool = False,
        mask_scale: float = 1.2,
        solid_mask: bool = False,
    ):
        self.input_paths = input_paths
        self.output_paths = output_paths
        self.threshold = threshold
        self.boxes = boxes
        self.mask_scale = mask_scale
        self.solid_mask = solid_mask

        if self.output_paths is None or len(self.output_paths) != len(self.input_paths):
            self.output_paths = [
                input_path.parent / (input_path.name.split(".")[0] + "-dehead" + input_path.suffix) for input_path in self.input_paths
            ]

    def preprocess(self):
        video_info: dict[(Path, Path), list[Path]] = {}
        new_input_paths = []
        new_output_paths = []
        for i, input_path in enumerate(self.input_paths):
            new_input_paths.append(input_path)
            new_output_paths.append(self.output_paths[i])

            if input_path.suffix.lower() in [".mp4", ".avi", ".mov"]:

                new_input_paths.pop()
                new_output_paths.pop()

                frames_input_path = input_path.parent / f"{input_path.stem}-frames"
                if frames_input_path.exists():
                    shutil.rmtree(frames_input_path)
                os.mkdir(frames_input_path)
                frames_output_path = self.output_paths[i].parent / f"{self.output_paths[i].stem}-frames"
                if frames_output_path.exists():
                    shutil.rmtree(frames_output_path)
                os.mkdir(frames_output_path)

                vidcap = cv2.VideoCapture(str(input_path))
                video_info[(input_path, self.output_paths[i])] = [frames_input_path, frames_output_path]

                success, image = vidcap.read()
                count = 0
                while success:
                    frame_path = frames_input_path / f"frame{count}.jpg"
                    frame_output_path = frames_output_path / f"frame{count}.jpg"
                    cv2.imwrite(str(frame_path), image)
                    self.input_paths.append(frame_path)
                    self.output_paths.append(frame_output_path)
                    success, image = vidcap.read()
                    count += 1

        self.input_paths = new_input_paths
        self.output_paths = new_output_paths
        return video_info

    def process_imgs(self):
        model = YOLO(MODEL_PATH)
        results = []

        for batch_start in range(0, len(self.input_paths), BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, len(self.input_paths))
            batch_input_paths = self.input_paths[batch_start:batch_end]
            batch_results = model.predict(
                batch_input_paths,
                conf=self.threshold,
            )
            results.extend(batch_results)

        for i, input_path in enumerate(self.input_paths):
            output_path = self.output_paths[i]

            with Image.open(input_path) as img:
                masks =  results[i].boxes.xywh.tolist()
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

    def process(self):
        video_info = self.preprocess()
        self.process_imgs()

        for input_path, output_path in video_info.keys():
            frames_input_path, frames_output_path = video_info[(input_path, output_path)]

            frame = cv2.imread(str(frames_output_path / "frame0.jpg"))
            height, width, _ = frame.shape
            output_video = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), 30, (width, height))

            count = len(list(frames_input_path.glob("frame*.jpg")))
            for i in range(count):
                frame = cv2.imread(str(frames_output_path / f"frame{i}.jpg"))
                output_video.write(frame)
                os.remove(frames_output_path / f"frame{i}.jpg")
            shutil.rmtree(frames_output_path)
            shutil.rmtree(frames_input_path)

            cv2.destroyAllWindows()
            output_video.release()

if __name__ == "__main__":
    Dehead(
        input_paths=[
            PROJECT_DIR / "demo/family.png", 
            PROJECT_DIR / "demo/demo-single-man.png",
            PROJECT_DIR / "demo/vid.mp4"],
        threshold=0.2,
        mask_scale=0.8,
        boxes=False,
        solid_mask=False,
    ).process()