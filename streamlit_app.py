"""Repo-root launcher for Streamlit Community Cloud and `streamlit run`.

Streamlit Cloud looks for `streamlit_app.py` by default. Keeping the app logic
in the installable package (`src/f1_analysis`) means this file stays a one-liner.
"""

from f1_analysis.app.main import main

main()
