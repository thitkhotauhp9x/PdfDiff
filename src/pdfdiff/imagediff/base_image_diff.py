from abc import ABC, abstractmethod
from pathlib import Path


class BaseImageDiff(ABC):

    @abstractmethod
    def diff(self, image1: Path, image2: Path, output_path: Path) -> None:
        pass
