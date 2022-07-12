Basic Usage
================

Synchronous
~~~~~~~~~~~~

.. code-block:: pycon

  >>> from aiovici import ViciSelector
  >>> example = ViciSelector("COM8", valve_type="Vici low pressure multiport", baud=9600, port_labels={"closed": 0, "source A": 1, "source B": 2})
  >>> example.select_port(0)  # or example.select_port("closed")
  >>> print(example.get_port())
  0
  >>> print(example.get_port(as_str=True))
  closed

Asynchronous
~~~~~~~~~~~~

.. code-block:: pycon

  >>> import asyncio
  >>> from aiovici import ViciSelectorAsync
  >>> async def main():
  >>>     example = await ViciSelectorAsync("COM8", valve_type="Vici low pressure multiport", baud=9600, port_labels={"closed": 0, "source A": 1, "source B": 2})
  >>>     await example.select_port(0)
  >>>     print(await example.get_port())
  >>>     print(await example.get_port(as_str=True))
  >>> asyncio.run(main())
  0
  closed

Parallelization with async
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from aiovici import ViciSelectorAsync
   async def main():
       example = [(await ViciSelectorAsync(f"COM{i}", valve_type="Vici low pressure multiport")) for _ in range(5,9)]
       await asyncio.gather([valve.select_port(1) for valve in example])
       ports = await asyncio.gather([valve.get_port() for valve in example])
   asyncio.run(main())

| Output: ``[1, 1, 1, 1]``
