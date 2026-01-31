from abc import ABC
from pathlib import Path


class BaseImages2Pdf(ABC):
    def to_pdf(self, image_files: list[Path], pdf_file: Path) -> None:
        pass
