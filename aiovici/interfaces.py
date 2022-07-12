import aioserial
import serial
from asyncinit import asyncinit
from typing import Union
import logging
from aiovici.bases import ViciCommon, ViciABC

@asyncinit
class ViciSelectorAsync(ViciCommon, ViciABC):
    """
    Async implementation of selector interface. All functions (including instantiation) must be ``await`` ed. See ViciABC for documentation.
    """
    async def __init__(self, port, valve_type, baud=9600, port_labels=None):
        super().__init__(valve_type, port_labels)
        self.serialport = aioserial.AioSerial(port, baudrate=baud, timeout=0.5)

        ask_type = await self.send_command('AM')
        if ask_type == '':
            ask_type = await self.test_baudrates()
        assert ask_type != '', "Did not get a reply from the selector... is the port, baudrate correct?  Is it turned on and plugged in?"

        if ord(ask_type[2]) != 0x31:
            response = (await self.send_command('NP'))[self.num_pos_loc[0]:self.num_pos_loc[1]]
            self.npositions = self.handle_np_response(response)

        if self.port_labels is None:
            self.port_labels = {str(i): i for i in range(1, self.npositions + 1)}

        self.current_port = None
        await self.get_port()
        self.updated = True

    async def send_command(self, cmd, response=True, questionmarkOK=False, timeout=-1):
        cmd += "\r"
        await self.serialport.write_async(bytes(cmd, 'utf8'))
        if response:
            prev_timeout = self.serialport.timeout
            if timeout != -1:
                self.serialport.timeout = timeout
            answer = ViciCommon.handle_answer((await self.serialport.readline_async()), questionmarkOK)
            self.serialport.timeout = prev_timeout
            return answer

    async def test_baudrates(self):
        for rate in [9600, 19200, 38400, 57600, 115200]:
            self.serialport.baudrate = rate
            asktype = await self.send_command('AM')
            if asktype != '':
                logging.info(f"Baudrate Correction: {str(self)}")
                return asktype
        logging.warning(f"No baudrates found for {self.serialport.port}")
        return ''

    async def select_port(self, port, direction=None):
        port_num = self.get_port_num(port)
        assert port_num <= self.npositions, "That port doesn't exist."
        command = ViciCommon.get_select_cmd(port_num, direction)
        await self.send_command(command, response=False)
        self.updated = True

    async def get_port(self, hard=True, as_str=False):
        if hard or self.updated:
            self.current_port = int((await self.send_command('CP'))[self.pos_loc[0]:self.pos_loc[1]]) if hard else self.current_port
            self.updated = False
        if as_str:
            return self.num_to_label(self.current_port)
        return self.current_port

    def __str__(self):
        return f"{self.valve_type} on {self.serialport.port} @ {self.serialport.baudrate} baud"

class ViciSelector(ViciCommon, ViciABC):
    """
    Synchronous implementation of selector interface. See ViciABC for documentation.
    """
    def __init__(self, port, valve_type, baud=9600, port_labels=None):
        super().__init__(valve_type, port_labels)
        self.serialport = serial.Serial(port, baudrate=baud, timeout=0.5)

        ask_type = self.send_command('AM')
        if ask_type == '':
            ask_type = self.test_baudrates()
        assert ask_type != '', "Did not get a reply from the selector... is the port, baudrate correct?  Is it turned on and plugged in?"

        if ord(ask_type[2]) != 0x31:
            response = self.send_command('NP')[self.num_pos_loc[0]:self.num_pos_loc[1]]
            self.npositions = self.handle_np_response(response)

        if self.port_labels is None:
            self.port_labels = {str(i): i for i in range(1, self.npositions + 1)}

        self.current_port = None
        self.get_port()
        self.updated = True

    def send_command(self, cmd, response=True, questionmarkOK=False, timeout=-1):
        cmd += "\r"
        self.serialport.write(bytes(cmd, 'utf8'))
        if response:
            prev_timeout = self.serialport.timeout
            if timeout != -1:
                self.serialport.timeout = timeout
            answer = ViciCommon.handle_answer(self.serialport.readline(), questionmarkOK)
            self.serialport.timeout = prev_timeout
            return answer

    def test_baudrates(self):
        for rate in [9600, 19200, 38400, 57600, 115200]:
            self.serialport.baudrate = rate
            asktype = self.send_command('AM')
            if asktype != '':
                logging.debug(f"Baudrate Correction: {str(self)}")
                return asktype
        logging.warning(f"No baudrates found for {self.serialport.port}")
        return ''

    def select_port(self, port, direction=None):
        port_num = self.get_port_num(port)
        assert port_num <= self.npositions, "That port doesn't exist."
        command = ViciCommon.get_select_cmd(port_num, direction)
        self.send_command(command, response=False)
        self.updated = True

    def get_port(self, hard=True, as_str=False):
        if hard or self.updated:
            self.current_port = int(self.send_command('CP')[self.pos_loc[0]:self.pos_loc[1]]) if hard else self.current_port
            self.updated = False
        if as_str:
            return self.num_to_label(self.current_port)
        return self.current_port

    def __str__(self):
        return f"{self.valve_type} on {self.serialport.port} @ {self.serialport.baudrate} baud"
