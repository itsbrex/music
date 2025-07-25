"""Download and configure the eCantorix engine."""

import os
import subprocess
from .perform import sing

here = os.path.abspath(os.path.dirname(__file__))
ECANTORIXDIR = here + '/ecantorix'


def get_engine():
    """Return path to the local eCantorix engine."""
    if not os.path.exists(ECANTORIXDIR):
        raise RuntimeError(
            "eCantorix engine not found. Run 'setup_engine()' to install it."
        )
    return ECANTORIXDIR


def setup_engine(method="http"):
    """Clone the eCantorix repository for local usage."""
    if os.path.exists(ECANTORIXDIR):
        return

    if method == "http":
        repo_url = 'https://github.com/ttm/ecantorix'
    elif method == "ssh":
        repo_url = 'git@github.com:ttm/ecantorix.git'
    else:
        raise ValueError('method not understood')

    try:
        subprocess.run(['git', 'clone', repo_url, ECANTORIXDIR], check=True)
    except Exception as exc:
        raise RuntimeError(f'Failed to clone repository: {exc}') from exc
    return ECANTORIXDIR


def make_test_song():
    t = 1
    t2 = .5
    t4 = .25
    text = "hey ma bro, why fly while dive?"
    notes = 7, 0, 5, 7, 11, 12, 7, 0
    durs = t2, t2, t4, t4, t, t4, t2
    sing(text, notes, durs)
