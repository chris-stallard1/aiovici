=================
Similar Projects
=================

vicivalve_
~~~~~~~~~~~~

:mod:`vicivalve` has support for more commands and operating modes than :mod:`aiovici`.
However, it lacks :mod:`asyncio` support and tends to run commands which aren't always supported without handling of invalid responses.
Additionally, it does not support custom naming for ports (a nice convenience feature)
You should definitely use :mod:`vicivalve` if you have RS232 or RS485 valves.
You should use :mod:`aiovici` for cases where parallelization (or controlling valves while running other code, such as pressure monitoring) is important.
Other than those use cases, however, the modules provide the same functionality and the choice is yours.

.. _vicivalve: https://pypi.org/project/vicivalve/
