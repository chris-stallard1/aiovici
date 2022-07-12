========
aiovici
========
This library provides a wrapper around :mod:`pySerial` or :mod:`aioserial` objects to allow easier communication with
Vici multiposition selector and switch valves that use

.. _The VICI Universal Electric Actuator: https://www.vici.com/act/ua.php

It has both standard (synchronous) and :mod:`asyncio` (asynchronous) interfaces, for compatibility with a wide variety of applications.
Only a few commands are supported initially, as the command options vary widely across different models of valve.
However, calling custom commands is easy, using the ``send_command`` function directly.
This package is unofficial and not affiliated Valco Instruments Company Inc. (VICI).

|
| Install :mod:`aiovici` with

.. code-block:: console

   pip install aiovici

========
Contents
========
.. toctree::
   :maxdepth: 1

   Basic Usage <intro>
   API Documentation <aiovici>
   Similar Projects <similar>

* :ref:`genindex`
