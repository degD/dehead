VERSION = "0.1.0"
HELP = """
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
                        solid black box. Default: "blur".
  --blur-radius         Blur radius. Default: 15
  --batch-size          Number of images to be loaded into memory for parallel
                        processing. Increasing this number decreases the process
                        time, but increases memory consumption. Default: 16 
                        (3-4GB memory)
  --version, -v         Print version number and exit.
  --help, -h            Show this help message and exit.
"""

import argparse
from pathlib import Path
from dehead import Dehead

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.format_help = lambda: HELP
    parser.add_argument("input_paths", nargs="*", metavar="input", help="File path(s). It is possible to pass multiple paths.")
    parser.add_argument("--output", "-o", dest="output_paths", nargs="+", help="Output file name. Defaults to input path + postfix '-dehead'.")
    parser.add_argument("--thresh", "-t", dest="threshold", type=float, default=0.2, help="Detection threshold. Default: 0.2.")
    parser.add_argument("--boxes", action="store_true", help="Use boxes instead of ellipse masks.")
    parser.add_argument("--mask-scale", dest="mask_scale", type=float, default=1.2, help="Scale factor for face masks, to make sure that masks cover the complete face. Default: 1.2.")
    parser.add_argument("--replacewith", choices=["blur", "solid"], default="blur", help="Anonymization filter mode for face regions.")
    parser.add_argument("--blur-radius", dest="blur_radius", type=int, default=15, help="Blur radius. Default: 15")
    parser.add_argument("--batch-size", dest="batch_size", type=int, default=16, help="Number of images to be loaded into memory for parallel processing. Increasing this number decreases the process time, but increases memory consumption. Default: 16 (3-4GB memory)")
    parser.add_argument("--version", "-v", action="version", version=f"{VERSION}")
    parser.add_argument("--help", "-h", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    if not args.input_paths:
      parser.print_help()
      return

    input_paths = [Path(path) for path in args.input_paths]
    output_paths = [Path(path) for path in args.output_paths] if args.output_paths else None
    solid_mask = args.replacewith == "solid" if args.replacewith == "solid" else False

    dehead = Dehead(
        input_paths=input_paths,
        output_paths=output_paths,
        threshold=args.threshold,
        boxes=args.boxes,
        mask_scale=args.mask_scale,
        solid_mask=solid_mask,
        blur_radius=args.blur_radius,
        batch_size=args.batch_size
    )
    dehead.process()

if __name__ == "__main__":
    main()