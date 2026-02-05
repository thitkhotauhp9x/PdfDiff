import logging
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from filecmp import dircmp
from typing import Generator

import tempfile
from pdfdiff.base_pdf_diff import BasePdfDiff
from pdfdiff.imagediff.base_image_diff import BaseImageDiff
from pdfdiff.imagediff.image_diff import ImageDiff
from pdfdiff.images2pdf.base_images_2_pdf import BaseImages2Pdf
from pdfdiff.images2pdf.images_2_pdf import Images2Pdf
from pdfdiff.magickcmdtools.magick_append_images import MagickAppendImages
from pdfdiff.magickcmdtools.magick_executor import MagicExecutor
from pdfdiff.pdf2images.base_pdf_2_images import BasePdf2Images
from pdfdiff.pdf2images.pdf_2_images_by_gs import Pdf2ImagesByGs


logger = logging.getLogger(__name__)


@contextmanager
def create_directory(suffix: str | None = None, directory: Path | None = None) -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory(suffix=suffix, dir=directory) as tmpdir:
        yield Path(tmpdir)


@dataclass
class PdfDiff(BasePdfDiff):
    pdf_2_image: BasePdf2Images = field(default_factory=Pdf2ImagesByGs)
    image_diff: BaseImageDiff = field(default_factory=ImageDiff)
    images_2_pdf: BaseImages2Pdf = field(default_factory=Images2Pdf)
    append_images_executor: MagicExecutor = field(default_factory=MagickAppendImages)

    def diff(self, pdf1: Path, pdf2: Path, output_file: Path) -> None:
        with ExitStack() as stack:
            working_dir = stack.enter_context(create_directory(suffix="working_dir"))
            output_dir_1 = stack.enter_context(create_directory(suffix="output_1", directory=working_dir))
            output_dir_2 = stack.enter_context(create_directory(suffix="output_2", directory=working_dir))

            with ThreadPoolExecutor(max_workers=2) as pool:
                results = pool.map(self.pdf_2_image.to_images,[pdf1, pdf2], [output_dir_1, output_dir_2])

                for result in results:
                    logger.debug("%s", result)

                cmp = dircmp(output_dir_1, output_dir_2)

                cmp_image_files = []

                images_1 = [output_dir_1 / common_file for common_file in cmp.common_files]
                images_2 = [output_dir_2 / common_file for common_file in cmp.common_files]

                def func(image_1, image_2):
                    return self.diff_image_core(cmp_image_files, image_1, image_2, working_dir)

                results = pool.map(func,  images_1, images_2)
                for result in results:
                    logger.debug("%s", result)

                self.images_2_pdf.to_pdf(cmp_image_files, pdf_file=output_file)

    def diff_image_core(self, cmp_image_files: list[Path], image1: Path, image2: Path, working_dir: Path):
        diff_image = working_dir / f"{image1.name}-{image2.name}.diff.png"

        self.image_diff.diff(image1, image2, diff_image)

        cmp_image_file = working_dir / f"{image1.name}-{image2.name}.result.png"

        self.append_images_executor.execute([image1, image2, diff_image], cmp_image_file)
        cmp_image_files.append(cmp_image_file)
