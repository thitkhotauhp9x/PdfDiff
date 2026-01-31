from abc import ABC, abstractmethod
from pathlib import Path


class BasePdf2Images(ABC):

    @abstractmethod
    def to_images(self, pdf_file: Path, output_dir: Path) -> None:
        pass
