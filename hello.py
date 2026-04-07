"""Dump all environment variables to console and a text file."""

from pathlib import Path
import os
import sys


def collect_env_vars() -> list[tuple[str, str]]:
    """Return a sorted list of (key, value) environment variable pairs."""
    return sorted(os.environ.items())


def write_env_file(env_vars: list[tuple[str, str]], path: Path) -> None:
    """Write environment variables to a text file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for key, value in env_vars:
            f.write(f"{key}={value}\n")


def main() -> None:
    output_path = Path("/tmp/all_env_vars.txt")

    env_vars = collect_env_vars()

    if not env_vars:
        print("No environment variables found.", file=sys.stderr)
        sys.exit(1)

    for key, value in env_vars:
        print(f"{key}={value}")

    write_env_file(env_vars, output_path)

    print(f"\n--- Total: {len(env_vars)} environment variables ---")
    print(f"Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
