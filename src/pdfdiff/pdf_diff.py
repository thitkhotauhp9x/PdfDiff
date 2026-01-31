import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from filecmp import dircmp

from src.pdfdiff.base_pdf_diff import BasePdfDiff
from src.pdfdiff.imagediff.base_image_diff import BaseImageDiff
from src.pdfdiff.imagediff.image_diff import ImageDiff
from src.pdfdiff.images2pdf.base_images_2_pdf import BaseImages2Pdf
from src.pdfdiff.images2pdf.images_2_pdf import Images2Pdf
from src.pdfdiff.pdf2images.base_pdf_2_images import BasePdf2Images
from src.pdfdiff.pdf2images.pdf_2_images_by_gs import Pdf2ImagesByGs


@dataclass
class PdfDiff(BasePdfDiff):
    pdf_2_image: BasePdf2Images = field(default_factory=Pdf2ImagesByGs)
    image_diff: BaseImageDiff = field(default_factory=ImageDiff)
    images_2_pdf: BaseImages2Pdf = field(default_factory=Images2Pdf)

    def diff(self, pdf1: Path, pdf2: Path, output_file: Path) -> None:
        output_dir_1 = Path(TemporaryDirectory(delete=False).name)
        output_dir_2 = Path(TemporaryDirectory(delete=False).name)

        self.pdf_2_image.to_images(pdf1, output_dir=output_dir_1)
        self.pdf_2_image.to_images(pdf2, output_dir=output_dir_2)

        cmp = dircmp(output_dir_1, output_dir_2)

        cmp_image_files = []
        for comon_file in cmp.common_files:
            image1 = output_dir_1 / comon_file
            image2 = output_dir_2 / comon_file

            diff_image = Path(f"{image1.name}-{image2.name}.diff.png")

            self.image_diff.diff(image1, image2, diff_image)

            cmp_image_file = Path(f"{image1.name}-{image2.name}.result.png")
            self._append_images([image1, image2, diff_image], cmp_image_file)
            cmp_image_files.append(cmp_image_file)

        self.images_2_pdf.to_pdf(cmp_image_files, pdf_file=output_file)

    @staticmethod
    def _append_images(image_files: list[Path], output_file: Path):
        subprocess.run([
            "magick",
            *[image.as_posix() for image in image_files],
            "+append",
            output_file.as_posix()
        ])
