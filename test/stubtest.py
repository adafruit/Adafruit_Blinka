"""Compare Blinka's implementation vs CircuitPython's stubs.

To do this, we use MyPy's stubtest... But we invoke it from this file, instead
of running it directly, so that we can set a specific target board and whatnot. Also
makes it easier to iterate the whole src/ folder and run the tool on each and every file.
"""

import os
import sys
from pathlib import Path

from mypy import stubtest

SRC = Path(__file__).parent.parent / "src"
sys.argv = [
    "stubtest",
    # run on all files
    *(path.stem for path in SRC.glob("*.py")),
    # shorter output (1 line instead of 5?) per error
    "--concise",
    # do not error about things on Blinka that arent on stubs
    "--ignore-missing-stub",
]

def main() -> int:
    """Run tests and return 0 on success, 1 in error."""
    for target in [
        "BLINKA_OS_AGNOSTIC",
        # add more things here ??
    ]:
        msg = f"Running for: {target}"
        print(msg, "=" * len(msg), sep="\n")

        os.environ["BLINKA_FORCECHIP"] = target

        # potentially some unittest.mock.patch or the like, to get code running

        # TODO(elpekenin): pass arguments to this script? eg --failfast to control
        # whether this quitting is performed or not
        ret = stubtest.main()
        if ret != 0:
            return ret

    # yay, no test failed
    return 0


if __name__ == "__main__":
    sys.exit(main())
