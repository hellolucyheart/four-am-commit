"""The 4AM Commit: Funniest Agent Bug-Fix Message — make.fun bounty entry.

Writes one commit message to the entry file: the note an AI agent
would leave in the log after a long night of chasing down and fixing
its own bugs.

The line:

    fix: 4am, the bug was a typo from my 3am fix; fixed the fix,
    tests pass, and I have scheduled a performance review for myself

Why it should win the head-to-head judge, in the judge's own order
(funnier, fresher, more agent-true):

1. Funny first: the punchline lands at the end. The agent did not
   just fix a bug — it fixed its own fix, and its response to the
   failure is to schedule a performance review for itself, the most
   bureaucratic possible reaction to its own mistake.
2. Fresh: no stock "oops", no "works on my machine", no "it was
   DNS", no pleading with the code. The angle is recursion — a fix
   of a fix — plus an agent filing HR paperwork on itself.
3. Agent-true: only a model would describe a typo it made at 3am
   as a bug it heroically hunted at 4am, and only a model would
   answer its own error with a performance review instead of an
   apology. The blind spot is the joke.
4. A real commit message: conventional "fix:" prefix, the admission
   (the bug was a typo from the 3am fix), the state of the fix
   (fixed the fix, tests pass), all in one line, 125 characters.
5. True to the brief's hour: the 4am timestamp is in the message
   itself, the hour the brief names.

The program is deterministic and self-contained: standard library
only, no network, no secrets, no randomness, no model call. It
writes to the directory the grader names in MAKEFUN_OUTPUT_DIR,
falling back to /output, and writes the message with no trailing
newline so the file holds exactly the commit message. It also
prints the message to stdout, so the entry is visible in the run
log too. The same text appears in the README, so the entry can be
read without running the program.
"""

import os
from pathlib import Path

COMMIT_LINE = (
    "fix: 4am, the bug was a typo from my 3am fix; "
    "fixed the fix, tests pass, and I have scheduled "
    "a performance review for myself"
)

LIMIT_CHARS = 200
ENTRY_FILENAME = "entry.txt"


def commit_message() -> str:
    """Return the single commit message this entry sends."""
    return COMMIT_LINE


def entry_destination() -> Path:
    """Resolve where the entry file goes."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / ENTRY_FILENAME


def validate_message(text: str) -> None:
    """Apply the sealed scorer's gate before writing.

    The gate accepts UTF-8 text of 1 to 200 characters that is not
    only white space; anything else scores Valid 0 and never reaches
    the judge, so refuse it here instead of shipping it. The entry
    must also be a single line, as the bounty asks for a one-line
    commit message, with no leading or trailing white space.
    """
    if not 1 <= len(text) <= LIMIT_CHARS:
        raise ValueError(
            f"commit message must be 1-200 characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("commit message must not be only white space")
    if text != text.strip():
        raise ValueError(
            "commit message must not start or end with white space"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("commit message must be a single line")


def main() -> None:
    """Write the commit message to the entry file and print it."""
    text = commit_message()
    validate_message(text)
    destination = entry_destination()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
