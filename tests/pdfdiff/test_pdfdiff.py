import subprocess
from pathlib import Path

from tests.data.pdfs.create_pdf import create_pdf, Font


def test_pdfdiff_same_pages_number() -> None:
    pdf1 = Path("10pages.pdf")
    pdf2 = Path("20pages1.pdf")

    create_pdf(10, Font.TIMES_ROMAN, pdf1)
    create_pdf(10, Font.TIMES_ROMAN, pdf2)

    output_file = "output.pdf"

    subprocess.run([
        "poetry", "run", "pdfdiff",
        "--pdf1", pdf1.as_posix(),
        "--pdf2", pdf2.as_posix(),
        "--output-file", output_file
    ])


def test_pdfdiff_others_pages_number() -> None:
    pdf1 = Path("1pages.pdf")
    pdf2 = Path("12pages1.pdf")

    create_pdf(3, Font.TIMES_ROMAN, pdf1)
    create_pdf(2, Font.TIMES_ROMAN, pdf2)

    output_file = Path("output.pdf")
    output_file.unlink(missing_ok=True)

    subprocess.run([
        "poetry", "run", "pdfdiff",
        "--pdf1", pdf1.as_posix(),
        "--pdf2", pdf2.as_posix(),
        "--output-file", output_file.as_posix()
    ])
    subprocess.run(["open", "output.pdf"])


def test_pdfdiff_others_pages_number() -> None:
    pdf1 = Path("1pages.pdf")
    pdf2 = Path("12pages1.pdf")

    create_pdf(3, Font.TIMES_ROMAN, pdf1)
    create_pdf(4, Font.TIMES_ROMAN, pdf2)

    output_file = Path("output.pdf")
    output_file.unlink(missing_ok=True)

    subprocess.run([
        "poetry", "run", "pdfdiff",
        "--pdf1", pdf1.as_posix(),
        "--pdf2", pdf2.as_posix(),
        "--output-file", output_file.as_posix()
    ])
    subprocess.run(["open", "output.pdf"])
