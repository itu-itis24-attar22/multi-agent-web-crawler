import shlex

from src.cli.commands import (
    index_command,
    search_command,
    list_jobs_command,
    job_status_command,
    pages_command,
)
from src.core.background_jobs import BackgroundJobManager


def run_shell() -> None:
    manager = BackgroundJobManager()

    print("Interactive crawler shell")
    print("Type 'help' for commands, 'exit' to quit.\n")

    while True:
        try:
            raw = input("crawler> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting shell.")
            break

        if not raw:
            continue

        if raw in {"exit", "quit"}:
            print("Exiting shell.")
            break

        if raw == "help":
            print("Commands:")
            print("  index <origin_url> <max_depth>")
            print("  bg-index <origin_url> <max_depth>")
            print("  jobs")
            print("  job-status <job_id>")
            print("  pages <job_id>")
            print("  search <query> [--limit N] [--job-id ID]")
            print("  exit")
            print()
            continue

        try:
            parts = shlex.split(raw)
        except ValueError as e:
            print(f"Parse error: {e}")
            continue

        command = parts[0]

        try:
            if command == "index":
                if len(parts) != 3:
                    print("Usage: index <origin_url> <max_depth>")
                    continue

                origin_url = parts[1]
                max_depth = int(parts[2])
                index_command(origin_url, max_depth)

            elif command == "bg-index":
                if len(parts) != 3:
                    print("Usage: bg-index <origin_url> <max_depth>")
                    continue

                origin_url = parts[1]
                max_depth = int(parts[2])
                job_id = manager.start_index_job(origin_url, max_depth)
                print(f"Started background indexing job {job_id}")

            elif command == "jobs":
                list_jobs_command()

            elif command == "job-status":
                if len(parts) != 2:
                    print("Usage: job-status <job_id>")
                    continue

                job_status_command(int(parts[1]))

            elif command == "pages":
                if len(parts) != 2:
                    print("Usage: pages <job_id>")
                    continue

                pages_command(int(parts[1]))

            elif command == "search":
                if len(parts) < 2:
                    print("Usage: search <query> [--limit N] [--job-id ID]")
                    continue

                limit = 20
                job_id = None

                query_parts = []
                i = 1
                while i < len(parts):
                    if parts[i] == "--limit":
                        if i + 1 >= len(parts):
                            print("Usage: search <query> [--limit N] [--job-id ID]")
                            break
                        limit = int(parts[i + 1])
                        i += 2
                    elif parts[i] == "--job-id":
                        if i + 1 >= len(parts):
                            print("Usage: search <query> [--limit N] [--job-id ID]")
                            break
                        job_id = int(parts[i + 1])
                        i += 2
                    else:
                        query_parts.append(parts[i])
                        i += 1
                else:
                    query = " ".join(query_parts)
                    if not query:
                        print("Usage: search <query> [--limit N] [--job-id ID]")
                        continue
                    search_command(query, limit=limit, job_id=job_id)

            else:
                print(f"Unknown command: {command}")

        except Exception as e:
            print(f"Error: {e}")