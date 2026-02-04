import argparse
from pathlib import Path

from pdfdiff.pdfdiff import PdfDiff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf1", required=True)
    parser.add_argument("--pdf2", required=True)
    parser.add_argument("--output-file", required=True)

    args = parser.parse_args()

    pdf_diff = PdfDiff()
    pdf_diff.diff(Path(args.pdf1), Path(args.pdf2), Path(args.output_file))


if __name__ == "__main__":
    main()
