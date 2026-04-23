
# DEHEAD: Anonymization by head detection

`dehead` is a simple command-line tool for automatic anonymization in videos or photos.
Inspired from [deface](https://github.com/ORB-HD/deface). Uses YOLO internally. 
Pretrained YOLO model sourced from [this project](https://github.com/Owen718/Head-Detection-Yolov8).
If pretrained model is not available there, you can [download it here (community-hosted mirror)](https://github.com/degD/dehead/releases/tag/v0.1.0) as well. 
Download `best.pt` and place it under project root.

This project is created for edge cases, where tools like `deface` fail to
anonymize side views or back views of heads.

## Demo videos

### Original:
https://github.com/user-attachments/assets/cc244aa2-a66c-4439-b1ef-166a8874919e

### Deface:
https://github.com/user-attachments/assets/79d284c1-3016-482a-84ac-dfa37d1d4992

### Dehead:
https://github.com/user-attachments/assets/3b53d6c4-7ead-41d2-9f9d-88a68a25c87f

## Installation (using `uv`)

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone the repo: `git clone https://github.com/degD/dehead && cd dehead`.
3. Make sure `python3.12` or newer is installed.
4. Install dependencies with `uv sync`.
5. Add `bin/` subdirectory to path.
6. Download and place model weights. See releases.
7. Run `dehead`.

## Usage

### Quick start

If you want to try out anonymizing a video using the default settings, 
you just need to supply the path to it. 
For example, if the path to your test video is `myvideos/vid1.mp4`, run:

    $ dehead myvideos/vid1.mp4

This will write the output to the file `myvideos/vid1-dehead.mp4`.

### CLI usage and options summary

To get an overview of usage and available options, run:

    $ dehead -h

```
usage: dehead [--output O] [--thresh T] [--boxes] [--mask-scale M]
              [--replacewith {blur,solid}] [--blur-radius R] 
              [--batch-size B]
              [--version] [--help] [input ...]

Video anonymization by head detection

positional arguments:
  input                 File path(s). It is possible to pass multiple paths.

optional arguments:
  --output O, -o O      Output file name. Defaults to input path + postfix "-dehead".
  --thresh T, -t T      Detection threshold. Default: 0.2.
  --boxes               Use boxes instead of ellipse masks.
  --mask-scale M        Scale factor for face masks, to make sure that masks
                        cover the complete face. Default: 1.2.
  --replacewith {blur,solid}
                        Anonymization filter mode for face regions. "blur"
                        applies a strong gaussian blurring, "solid" draws a
                        solid black box.
  --blur-radius         Blur radius. Default: 15
  --batch-size          Number of images to be loaded into memory for parallel
                        processing. Increasing this number decreases the process
                        time, but increases memory consumption. Default: 16 
                        (3-4GB memory)
  --version, -v         Print version number and exit.
  --help, -h            Show this help message and exit.
```

## Known Issues

- Inputs must be files, passing directories is not supported. But you can pass videos and images together.
- Explicitly batches files for head detection, which might be slowing down the process slightly. 
- Video files are processed without keeping the audio.
- Generated video files are always re-encoded using `mp4v` at fixed 30 FPS, independent from source settings. This can increase file size and alter playback duration/speed for non-30 FPS inputs.
- Model weights are sourced from a different project, and could be removed in the future if requested. Also, it could perform bad in some cases, or could be too large for others. However, it is planned to train a new model in the future that will hopefully mitigate these problems.
- Progress display is missing.

## Credits

- This project is particularly inspired from [deface](https://github.com/ORB-HD/deface).
- The model weights file is sourced from [Head-Detection-Yolov8](https://github.com/Owen718/Head-Detection-Yolov8).

## License

MIT
