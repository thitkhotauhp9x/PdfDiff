from pathlib import Path
from subprocess import run
from src.pdfdiff.pdf2images.base_pdf_2_images import BasePdf2Images


class Pdf2ImagesByGs(BasePdf2Images):

    def to_images(self, pdf_file: Path, output_dir: Path) -> None:
        run([
            "gs",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=png16m",
            "-r300",
            f"-sOutputFile={output_dir.as_posix()}/out_%03d.png",
            pdf_file.as_posix(),
        ])
