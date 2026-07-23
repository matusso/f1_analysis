"""Console-script entry point: ``f1-analysis`` launches the Streamlit app."""

from __future__ import annotations

import sys
from pathlib import Path

from streamlit.web import cli as st_cli

_MAIN = Path(__file__).with_name("main.py")


def main() -> int:
    """Launch the Streamlit server for the app, forwarding extra CLI args."""
    sys.argv = ["streamlit", "run", str(_MAIN), *sys.argv[1:]]
    return st_cli.main()  # type: ignore[no-any-return]


if __name__ == "__main__":
    raise SystemExit(main())
