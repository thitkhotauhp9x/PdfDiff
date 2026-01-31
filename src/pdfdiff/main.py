import argparse

from src.pdfdiff.pdf_diff import PdfDiff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf1", required=True)
    parser.add_argument("--pdf2", required=True)
    parser.add_argument("--output-file", required=True)

    args = parser.parse_args()

    pdf_diff = PdfDiff()
    pdf_diff.diff(args.pdf1, args.pdf2, args.output_file)


if __name__ == "__main__":
    main()
