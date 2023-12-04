from __future__ import annotations

import argparse
import re
from typing import IO
from typing import Sequence

import git
REGEX_PATTERN = r'\b[A-Z]+-[0-9]+\b'


def fix_message(file_obj: IO[str]) -> int:
    repo = git.Repo()
    branch_name = repo.active_branch.name
    if not branch_name:
        return 0

    matches = re.findall(REGEX_PATTERN, branch_name)
    if len(matches) == 0:
        return 0

    prepend_msg = f"[{','.join(matches)}]"
    commit_msg = file_obj.read()
    if commit_msg.startswith(prepend_msg):
        return 0

    new_commit_msg = f'{prepend_msg} {commit_msg}'
    file_obj.seek(0)
    file_obj.write(new_commit_msg)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Commit message filename')
    args = parser.parse_args(argv)

    with open(args.filename, 'r+') as file_obj:
        retv = fix_message(file_obj)

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
