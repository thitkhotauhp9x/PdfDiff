import subprocess
from pathlib import Path

from pdfdiff.magickcmdtools.magick_executor import MagicExecutor


class MagickAppendImages(MagicExecutor):
    def execute(self, image_files: list[Path], output_file: Path) -> None:
        subprocess.run([
            "magick",
            *[image.as_posix() for image in image_files],
            "+append",
            output_file.as_posix()
        ])
