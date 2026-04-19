"""Entry point for the crawler. Usage:

    python main.py init               # create the SQLite schema
    python main.py shell              # interactive CLI
    python main.py index <url> <k>    # one-shot crawl
    python main.py search <query>     # search indexed pages
    python main.py jobs               # list jobs
    python main.py pages <job_id>     # list pages for a job
    python main.py ui                 # launch the Flask web UI (needs flask)
"""

from __future__ import annotations

import sys

from src.cli.commands import (
    index_command,
    init_db_command,
    job_status_command,
    list_jobs_command,
    pages_command,
    search_command,
)
from src.cli.shell import run_shell


def _usage() -> int:
    print(__doc__)
    return 2


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return _usage()

    cmd = argv[1]

    if cmd == "init":
        init_db_command()
        return 0

    if cmd == "shell":
        run_shell()
        return 0

    if cmd == "index":
        if len(argv) != 4:
            print("Usage: python main.py index <url> <max_depth>")
            return 2
        index_command(argv[2], int(argv[3]))
        return 0

    if cmd == "search":
        if len(argv) < 3:
            print("Usage: python main.py search <query> [limit]")
            return 2
        limit = int(argv[-1]) if len(argv) >= 4 and argv[-1].isdigit() else 20
        query = " ".join(argv[2 : (-1 if limit != 20 or argv[-1].isdigit() else len(argv))])
        search_command(query or " ".join(argv[2:]), limit=limit)
        return 0

    if cmd == "jobs":
        list_jobs_command()
        return 0

    if cmd == "job":
        if len(argv) != 3:
            print("Usage: python main.py job <job_id>")
            return 2
        job_status_command(int(argv[2]))
        return 0

    if cmd == "pages":
        if len(argv) != 3:
            print("Usage: python main.py pages <job_id>")
            return 2
        pages_command(int(argv[2]))
        return 0

    if cmd == "ui":
        from src.web.app import run_ui
        run_ui()
        return 0

    return _usage()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
