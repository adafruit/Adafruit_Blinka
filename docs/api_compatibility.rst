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
`Pull request #1150 <https://github.com/adafruit/Adafruit_Blinka/pull/1150>`_
supersedes that prototype with guarded reporting and a revision-based regression
check. This tooling does not change Blinka's runtime APIs. Signature alignment
belongs in separate, module-focused pull requests with appropriate validation.

Running the checker
-------------------

From the repository root, install the development requirements into a virtual
environment and run the checker::

    python -m pip install -r requirements-api.txt
    python scripts/check_circuitpython_api.py

``requirements-api.txt`` pins ``circuitpython-stubs==10.3.1`` and
``mypy==2.4.0``. These are tooling dependencies, not Blinka runtime requirements.
The local default is the known-stable
`CircuitPython 10.3.1 stable release
<https://github.com/adafruit/circuitpython/releases/tag/10.3.1>`_.

An ordinary run checks all twelve audited modules and inventories all modules in
the installed stubs. To investigate one module, use ``--module``; repeat it to
check several audited modules::

    python scripts/check_circuitpython_api.py --module busio
    python scripts/check_circuitpython_api.py --module busio --module digitalio

Standalone runs inspect the working tree, including uncommitted edits. Exit
status ``0`` means no API discrepancies were found in the selected modules;
``1`` means discrepancies were found; ``2`` indicates a checker or import
failure. Inventory categories such as missing or separately packaged modules do
not by themselves fail a run.

Optional reports can be written as JSON or Markdown::

    python scripts/check_circuitpython_api.py --json /tmp/blinka-api.json --markdown /tmp/blinka-api.md

The console summarizes the inventory and current discrepancy count. Reports
include the complete head inventory, current diagnostics, checked modules, source
references and the reason those modules were selected. Revision comparisons also
include base diagnostics and new and resolved differences.

Comparing a pull request
------------------------

To check only API regressions introduced by committed changes, compare ``HEAD``
with its merge base with the target branch::

    python scripts/check_circuitpython_api.py --base main

The target branch must be available locally; the checker does not fetch it.
This mode reads committed source from ``HEAD`` and
``git merge-base main HEAD``, not uncommitted edits. It automatically selects
audited modules affected by the diff. Changes to shared helpers, backends, the
checker or its configuration trigger a full audited-module comparison;
documentation-only and test-only changes skip the dynamic API comparison.
``--module`` can explicitly select audited modules for a focused comparison.

Both source revisions run through the same current, trusted guarded checker,
using the same installed CircuitPython stubs and checking tools. The base
revision's checker is not executed. This compares the pull request's effects
against one reference, so an unrelated upstream API change does not become a new
regression merely because it differs from Blinka on both revisions.

Only new head diagnostics fail the regression check. Existing discrepancies
remain visible, and resolved discrepancies pass without updating a stored
snapshot. Deleting a selected module that was implemented in the base revision
is also a regression. Missing modules elsewhere in the inventory, separately
packaged modules and unchecked modules remain informational.

In comparison mode, exit status ``0`` means no new API regressions were found,
not that Blinka has no discrepancies. Exit status ``1`` indicates a regression;
``2`` indicates a checker or import failure. Tooling and import failures cannot
be treated as accepted API differences.

Choosing the stub reference
--------------------------

Each API-check run in CI queries the official CircuitPython releases for the
latest stable release, installs matching ``circuitpython-stubs`` and passes the
tag through ``--stable-release``. Both revisions use that same installed
reference. If the release lookup or matching-stub download is unavailable, CI
emits a notice and retains the pinned reference. Reports always identify the
actual installed version; a fallback is not reported as the latest stable
release. Checker and import failures still fail the job.

Local runs use the installed stubs without a network lookup. After independently
verifying a stable release tag and installing its matching stubs, validate the
reference explicitly::

    python scripts/check_circuitpython_api.py --stable-release 10.3.1

This argument checks that the installed stub version matches the supplied tag;
it does not require the default pin, fetch a release, install dependencies or
verify that the tag is the latest stable release. The checker itself never
installs packages or fetches network resources.

What is checked
---------------

The checker starts from the stub modules, rather than only the modules already
present in Blinka. Its inventory distinguishes:

* ``missing``: no implementation identified in this repository.
* ``not_checked``: source is present, but is not checked on this target.
* ``not_selected``: an audited module outside this comparison's selected scope.
* ``separate_package``: functionality supplied by an identified external package.
* ``host_provided``: a CPython module whose API equivalence is not checked.
* ``checked``: selected for the OS-agnostic API comparison.

Audited modules absent from the installed reference are explicitly listed as
unreferenced, rather than claimed to have been compared against CircuitPython.

Separately packaged functionality is not automatically a missing implementation
or a request to add it to Blinka. For example,
`Adafruit-Blinka-Displayio
<https://github.com/adafruit/Adafruit_Blinka_Displayio>`_ supplies ``displayio``,
``fontio``, ``terminalio``, ``vectorio`` and display-bus modules. Classifying these
modules does not install or check that optional package.

API comparison uses the OS-agnostic target and an explicit safe-module allowlist.
The audited modules are ``analogio``, ``bitbangio``, ``board``, ``busio``,
``digitalio``, ``keypad``, ``microcontroller``, ``micropython``,
``neopixel_write``, ``onewireio``, ``pwmio`` and ``rainbowio``. ``--module`` does
not enable imports outside this allowlist.
Hardware-specific and unsafe modules are inventoried without being imported for
comparison. No hardware drivers are constructed, and automatic dependency
installation is disabled. The reports identify modules that were not checked;
an unchecked module is not evidence of compatibility or incompatibility.
The import guards are defense in depth for this audited profile, not a sandbox
for malicious source. Only compare trusted revisions.

The checks can find missing public classes, functions and attributes, as well as
signature differences such as parameter names, defaults and keyword-only
arguments. They do not establish equivalent behavior, return values, timing,
electrical operation, or compatibility on every supported board. Those still
need focused tests and, where appropriate, hardware testing.

Interpreting discrepancies
-------------------------

A diagnostic records an observed difference, not a confirmed Blinka defect or a
promise to implement a feature. The stubs can be wrong or represent an API
imperfectly; context manager ``__exit__`` typing is one example that needs
interpretation. An importable placeholder, such as ``onewireio``, is not evidence
that its hardware functionality is implemented.

When a diagnostic is disputed, compare the stubs with the corresponding
CircuitPython source and public API documentation before changing Blinka. Use
the full or per-module standalone report to plan signature fixes in separate,
module-focused pull requests, including behavioral or hardware validation where
needed. The regression gate does not require unrelated existing APIs to be
changed in every pull request.
