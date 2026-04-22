
from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw

PROJECT_DIR = Path(__file__).parent
MODEL_PATH = PROJECT_DIR / "best.pt"

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
                input_path + "-dehead" + input_path.suffix for input_path in self.input_paths
            ]

    def process(self):
        model = YOLO(MODEL_PATH)
        for i, input_path in enumerate(self.input_paths):
            results = model(input_path)
            for result in results:

                box = list(result.boxes.xyxy.tolist()[0])
                with Image.open(input_path) as img:
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(box, fill="black")
                
                img.save(self.output_paths[i])

if __name__ == "__main__":
    Dehead(
        input_paths=[PROJECT_DIR / "demo/demo-single-man.png"],
        output_paths=[PROJECT_DIR / "demo/demo-single-man-dehead.png"],
    ).process()