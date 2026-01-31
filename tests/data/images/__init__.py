from pathlib import Path
from hypothesis.strategies import sampled_from, composite


@composite
def images(draw) -> Path:
    image_files = list(Path(__file__).parent.glob("*.png"))
    return draw(sampled_from(image_files))
