#!/usr/bin/env python3
import re
import sys

ALLOWED_PREFIXES = [
    "FEAT",
    "FIX",
    "DOCS",
    "STYLE",
    "REFACTOR",
    "TEST",
    "CHORE",
]


def main():
    """Check if the commit message follows the conventional commit format.

    :return: status code
    """
    commit_msg_file = sys.argv[1]

    with open(commit_msg_file, "r", encoding="utf-8") as f:
        commit_msg = f.readline().strip()

    pattern = r"^\[(" + "|".join(ALLOWED_PREFIXES) + r")\]\s.+"

    if not re.match(pattern, commit_msg):
        print(f'❌ Bad commit message format : "{commit_msg}"')
        print("✅ Expected format: type(scope?): message")
        print(f"🧪 Allowed types: {', '.join(ALLOWED_PREFIXES)}", flush=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
