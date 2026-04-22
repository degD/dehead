
# DEHEAD: Anonymization by head detection

`dehead` is a simple command-line tool for automatic anonymization in videos or photos.
Inspired from [deface](https://github.com/ORB-HD/deface). Uses YOLO internally. 
Pretrained YOLO model sourced from [this project](https://github.com/Owen718/Head-Detection-Yolov8).
If pretrained model is not available there, you can [download it here](WIP_LINK) as well.
This project is created for edge cases, where face detectors in tools like `deface` fail to
anonymize side views of faces in some high motion frames.

## Installation (using `uv`)

1. Clone the repo: `git clone repo_path_wip`.
2. Install dependencies with `uv sync`.
3. Add `bin/` subdirectory to path.
4. Run `dehead`.

## Installation (using `python virtual environments`)

1. Clone the repo: `git clone repo_path_wip`.
2. Create a virtual environment: `python3 -m venv .venv`.
3. Enable it: `source .venv/bin/activate`.
4. `pip3 install ultralytics`
5. Add `bin/` subdirectory to path.
6. Run `dehead`.

## Usage

### Quick start

If you want to try out anonymizing a video using the default settings, 
you just need to supply the path to it. 
For example, if the path to your test video is `myvideos/vid1.mp4`, run:

    $ deface myvideos/vid1.mp4

This will write the output to the file `myvideos/vid1_anonymized.mp4`.

### CLI usage and options summary

To get an overview of usage and available options, run:

    $ dehead -h

```
usage: dehead [--output O] [--thresh T] [--scale WxH] [--preview] [--boxes]
              [--draw-scores] [--mask-scale M]
              [--replacewith {blur,solid,none,img,mosaic}]
              [--replaceimg REPLACEIMG] [--mosaicsize width] [--keep-audio]
              [--ffmpeg-config FFMPEG_CONFIG] [--backend {auto,onnxrt,opencv}]
              [--execution-provider EP] [--version] [--help]
              [input ...]

Video anonymization by head detection

positional arguments:
  input                 File path(s). It is possible to pass multiple paths.
                        Alternatively, you can pass a directory as an input,
                        in which case all files in the directory will be used
                        as inputs. 

optional arguments:
  --output O, -o O      Output file name. Defaults to input path + postfix
                        "-dehead".
  --thresh T, -t T      Detection threshold. Default: 0.2.
  --boxes               Use boxes instead of ellipse masks.
  --mask-scale M        Scale factor for face masks, to make sure that masks
                        cover the complete face. Default: 1.3.
  --replacewith {blur,solid}
                        Anonymization filter mode for face regions. "blur"
                        applies a strong gaussian blurring, "solid" draws a
                        solid black box.
  --keep-audio, -k      Keep audio from video source file and copy it over to
                        the output (only applies to videos).
  --version             Print version number and exit.
  --help, -h            Show this help message and exit.
```



## Credits

- This project is particularly inspired from [deface](https://github.com/ORB-HD/deface).
- The model weights file is sourced from [Head-Detection-Yolov8](https://github.com/Owen718/Head-Detection-Yolov8).

## License

MIT