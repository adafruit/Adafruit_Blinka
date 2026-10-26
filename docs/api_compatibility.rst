.. SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
..
.. SPDX-License-Identifier: MIT

Checking CircuitPython API compatibility
========================================

Blinka aims to let CircuitPython libraries run on Python and MicroPython without
maintaining separate library implementations. The development-only API checker
compares Blinka's public interface with CircuitPython's typing stubs to help
identify missing APIs and changes to function signatures.

This builds on `elpekenin's prototype in pull request #884
<https://github.com/adafruit/Adafruit_Blinka/pull/884>`_, proposed in
`issue #881 <https://github.com/adafruit/Adafruit_Blinka/issues/881>`_.

Running the checker
-------------------

From the repository root, install the development requirements into a virtual
environment and run the checker::

    python -m pip install -r requirements-api.txt
    python scripts/check_circuitpython_api.py

``requirements-api.txt`` pins ``circuitpython-stubs==10.3.1`` and
``mypy==2.4.0``. These are tooling dependencies, not Blinka runtime requirements.
The current reference matches the official
`CircuitPython 10.3.1 stable release
<https://github.com/adafruit/circuitpython/releases/tag/10.3.1>`_.

Each API-check run in CI queries GitHub for CircuitPython's latest stable release
and passes that tag through ``--stable-release``. If it differs from the pinned
reference, the check fails until the matching stubs are updated and the baseline
is reviewed. This failure cannot be accepted into the baseline.

Local runs use the explicit pin without a network lookup. After independently
verifying the latest stable tag, it can also be supplied locally::

    python scripts/check_circuitpython_api.py --stable-release 10.3.1

This argument compares the supplied tag with the pin; it does not fetch or
verify the release itself.

Optional reports can be written as JSON or Markdown::

    python scripts/check_circuitpython_api.py --json /tmp/blinka-api.json --markdown /tmp/blinka-api.md

The console summarizes the inventory and current discrepancy count, followed by
any errors, new observations and resolved observations. The report files include
the complete inventory and all current stub discrepancies.

What is checked
---------------

The checker starts from the stub modules, rather than only the modules already
present in Blinka. Its inventory distinguishes:

* ``missing``: no implementation identified in this repository.
* ``not_checked``: source is present, but is not checked on this target.
* ``separate_package``: functionality supplied by an identified external package.
* ``host_provided``: a CPython module whose API equivalence is not checked.
* ``checked``: selected for the OS-agnostic API comparison.

Separately packaged functionality is not automatically a missing implementation
or a request to add it to Blinka. For example,
`Adafruit-Blinka-Displayio
<https://github.com/adafruit/Adafruit_Blinka_Displayio>`_ supplies ``displayio``,
``fontio``, ``terminalio``, ``vectorio`` and display-bus modules. Classifying these
modules does not install or check that optional package.

API comparison uses the OS-agnostic target and an explicit safe-module allowlist.
Hardware-specific and unsafe modules are inventoried without being imported for
comparison. No hardware drivers are constructed, and automatic dependency
installation is disabled. The reports identify modules that were not checked;
an unchecked module is not evidence of compatibility or incompatibility.

The checks can find missing public classes, functions and attributes, as well as
signature differences such as parameter names, defaults and keyword-only
arguments. They do not establish equivalent behavior, return values, timing,
electrical operation, or compatibility on every supported board. Those still
need focused tests and, where appropriate, hardware testing.

Reviewing the baseline
----------------------

Existing diagnostics are recorded in a baseline so that the checker can be used
without first changing every API. The baseline is
``scripts/circuitpython_api_baseline.json`` and records both the module inventory
states and the exact stub diagnostics. An ordinary run reports existing, new and
resolved discrepancies. Both new and resolved differences fail the check: a fix
must remove its old entry rather than silently leaving stale exceptions behind.
Inventory changes also require review. Import failures and tooling failures
cannot be recorded as accepted baseline diagnostics.

Exit status ``0`` means the observations match the baseline, not that Blinka has
no discrepancies. Exit status ``1`` indicates new or resolved observations;
``2`` indicates a checker or import failure.

After inspecting the report and making any intended changes, explicitly update
the baseline::

    python scripts/check_circuitpython_api.py --update-baseline

Review the resulting diff before committing it. A baseline entry records a
known discrepancy, not a confirmed Blinka defect or a promise to implement a
feature. The stubs can also be wrong or represent an API imperfectly; context
manager ``__exit__`` typing is one example that needs interpretation.

Upgrade the pinned stubs deliberately and review the resulting changes. When a
diagnostic is disputed, compare the stubs with the corresponding CircuitPython
source and public API documentation before changing Blinka. Keep compatibility
fixes separate from this tooling when they need their own behavioral or hardware
validation.
