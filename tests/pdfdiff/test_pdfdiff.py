import subprocess
from contextlib import ExitStack
from typing import Any

import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from tests.data.pdfs.create_pdf import create_pdf, Font


@pytest.mark.parametrize("n1, n2",[
    [1, 1],
    [2, 2],
    [1, 2],
    [2, 1],
    [100, 1],
    [1, 100],
])
def test_pdfdiff(n1, n2) -> None:
    with ExitStack[Any]() as stack:
        p1 = stack.enter_context(NamedTemporaryFile(suffix="1.pdf"))
        p2 = stack.enter_context(NamedTemporaryFile(suffix="2.pdf"))

        pdf1 = Path(p1.name)
        pdf2 = Path(p2.name)

        create_pdf(n1, Font.TIMES_ROMAN, pdf1)
        create_pdf(n2, Font.TIMES_ROMAN, pdf2)

        output_file = "output.pdf"

        subprocess.run([
            "poetry", "run", "pdfdiff",
            "--pdf1", pdf1.as_posix(),
            "--pdf2", pdf2.as_posix(),
            "--output-file", output_file
        ])
