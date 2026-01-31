from abc import ABC, abstractmethod
from pathlib import Path


class BasePdfDiff(ABC):

    @abstractmethod
    def diff(self, pdf1: Path, pdf2: Path, output_file: Path):
        pass
