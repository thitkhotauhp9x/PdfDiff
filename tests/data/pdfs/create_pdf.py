import subprocess
import tempfile
from enum import StrEnum
from pathlib import Path


class Font(StrEnum):
    TIMES_ROMAN = "Times-Roman"
    HELVETICA = "Helvetica"


def create_pdf(page_number: int, font: Font, output_path: Path):
    content = f"""%!PS
/{font} findfont 24 scalefont setfont

1 1 {page_number} {{
  /i exch def
  72 720 moveto
  (Page ) show
  i 20 string cvs show
  showpage
}} for"""
    with tempfile.NamedTemporaryFile(suffix=".ps") as ps_file:

        ps_path = Path(ps_file.name)
        ps_path.write_text(content)

        subprocess.run(["ps2pdf", ps_path.as_posix(), output_path.as_posix()])
