
from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFilter

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

    def process(self):
        model = YOLO(MODEL_PATH)
        for i, input_path in enumerate(self.input_paths):
                
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

                        # TODO: Refactor needed to avoid code duplication
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

                    img.save(self.output_paths[i])

if __name__ == "__main__":
    Dehead(
        input_paths=[PROJECT_DIR / "demo/family.png"],
        output_paths=[PROJECT_DIR / "demo/family-dehead.png"],
        mask_scale=0.8,
        boxes=False,
        solid_mask=False,
    ).process()