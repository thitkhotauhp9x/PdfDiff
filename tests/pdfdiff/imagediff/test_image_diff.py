import subprocess
import tempfile
from pathlib import Path

from hypothesis import given

from src.pdfdiff.imagediff.image_diff import ImageDiff
from tests.data.images import images


def append_images(image_files: list[Path], output_file: Path):
    subprocess.run([
        "magick",
        *[image.as_posix() for image in image_files],
        "+append",
        output_file.as_posix()
    ])


@given(image1=images(), image2=images())
def test_diff(image1: Path, image2: Path) -> None:
    image_diff = ImageDiff()
    with tempfile.NamedTemporaryFile(suffix=".png") as tp:
        output_path = Path(tp.name)
        image_diff.diff(image1, image2, output_path=output_path)

        result_path = Path("output.png")
        append_images([image1, image2, output_path], output_file=result_path)
        subprocess.run(["open", result_path.as_posix()])
