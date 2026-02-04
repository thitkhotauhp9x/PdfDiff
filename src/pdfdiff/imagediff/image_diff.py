import subprocess
from pathlib import Path

from pdfdiff.imagediff.base_image_diff import BaseImageDiff


class ImageDiff(BaseImageDiff):
    def diff(self, image1: Path, image2: Path, output_path: Path) -> None:
        subprocess.run([
            "magick",
            "compare",
            "-metric",
            "AE",
            image1.as_posix(),
            image2.as_posix(),
            output_path.as_posix(),
        ])
