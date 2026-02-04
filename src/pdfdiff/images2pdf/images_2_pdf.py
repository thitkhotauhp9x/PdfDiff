import subprocess
from pathlib import Path

from pdfdiff.images2pdf.base_images_2_pdf import BaseImages2Pdf


class Images2Pdf(BaseImages2Pdf):
    def to_pdf(self, image_files: list[Path], pdf_file: Path) -> None:
        subprocess.run([
            "magick",
            *[image.as_posix() for image in image_files],
            pdf_file.as_posix()
        ])
