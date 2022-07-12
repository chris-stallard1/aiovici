from abc import ABC, abstractmethod
from typing import Union

class ViciABC(ABC):
    '''
    :param port: string describing the serial port the actuator is connected to
    :param baud: baudrate to use
    :param port_labels: dict for smart port naming, of the form ``{'sample':3, 'instrument':4, 'rinse':5, 'waste':6}``
    :param valve_type: one of "Vici low pressure multiport", "Vici high pressure multiport", or "Vici high pressure switch"

    | Connect to valve and query the number of positions
    | Confirm the valve type with command 'AM'
    | If the valve is a switch, set number of positions as 2
    | If the valve is a multiport, get the number of positions from the valve
    '''
    @abstractmethod
    def __init__(self, port: str, valve_type: str, baud: int=9600, port_labels:Union[dict, None]=None):
        pass

    @abstractmethod
    def send_command(self, cmd: str, response: bool=True, questionmarkOK: bool=False, timeout: float=-1):
        """
        :param cmd: The command to send
        :param response: Whether to wait for and return a response
        :param questionmarkOK: Whether a question mark in the response should raise an error (if True, it will not raise)
        :param timeout: Custom timeout to use for this request. If set to -1, will not change existing timeout.

        | Moves the selector to a port
        | If direction is set to either "CW" or "CCW" it moves the actuator in that direction.
        | If unset or other value, will move via most efficient route.
        """
        pass
    @abstractmethod
    def test_baudrates(self):
        """
        | Test a series of baudrates with the 'AM' command until a response is recieved.
        | Useful because Vici valves allow setting the baudrate and users may not know which rate their valve is running on
        """
        pass
    @abstractmethod
    def select_port(self, port: Union[int, str], direction: Union[str, None]=None):
        """
        :param port: Port to move to (either by number or by label in port labels)
        :param direction: Direction to move in, "CW" for clockwise, "CCW" for counterclockwise

        | Moves the selector to a port
        | If direction is set to either "CW" or "CCW" it moves the actuator in that direction.
        | If unset or other value, will move via most efficient route.
        """
    @abstractmethod
    def get_port(self, hard: bool=True, as_str: bool=False):
        '''
        :param hard: Whether to send a command requesting position or use the cached position
        :param as_str: Whether to return the "name" of the port (from port labels), if applicable

        Query the current selected position
        '''
        pass

class ViciCommon:
    """
    Functions and parameters common to sync and async implementations
    Stores valve type, port labels, and indexes of certain values in command responses
    """
    def __init__(self, valve_type: str, port_labels: Union[dict, None]):
        self.port_labels = port_labels
        self.valve_type = valve_type

        num_positions_location = {
                'Vici low pressure multiport':[2,4],
                'Vici high pressure multiport':[5,7],
                'Vici high pressure switch':[0,14]
        }
        position_location = {
            'Vici low pressure multiport': [2, 4],
            'Vici high pressure multiport': [15, 17],
            'Vici high pressure switch': [2, 3]
        }

        self.num_pos_loc = num_positions_location[valve_type]
        self.pos_loc = position_location[valve_type]
        self.rev_port_labels = {val: key for key, val in port_labels.items()}

    @staticmethod
    def handle_answer(answer: bytes, questionmarkOK: bool) -> str:
        """
        :param answer: Serial line response after sending a command
        :param questionmarkOK: Whether to ignore question marks in response

        :raises SerialException: If a question mark is in the response and ``questionmarkOK`` is ``False``

        :returns: Formatted serial output

        Handles a response from the valve
        """
        try:
            answer = answer.decode("utf-8")
        except UnicodeDecodeError:
            return 'invalid'
        if '?' in answer and not questionmarkOK:
            raise SerialException(f"{answer} invalid: contains question mark")
        return answer

    @staticmethod
    def get_select_cmd(port_num: int, direction: Union[str, None]) -> str:
        """
        :param port_num: The port number to move to
        :param direction: The direction to move

        :return: The command string to send to the valve to accomplish this move

        Formats a "select port" command based on the relevant parameters.
        """
        if direction == "CW":
            return "CW%02i" % port_num
        elif direction in ("CC", "CCW"):
            return "CC%02i" % port_num
        return "GO%02i" % port_num

    def handle_np_response(self, response) -> int:
        """
        :param response: returned by ``send_command()``

        :raises AssertionError: If there is no response

        :return: Number of ports

        Handles a response from a "NP" (get number of ports) command
        Accounts for the case when the command is called in a switch and returns invalid
        """
        if "Invalid" in response:
            self.port_labels = {'A':1, 'B':2}
            self.rev_port_labels = {1:'A', 2:'B'}
            return 2
        assert response != '', "Did not get a reply from the selector... is the port, baudrate correct?  Is it turned on and plugged in?"
        return int(response)

    def get_port_num(self, port):
        if type(port) == str:
            return self.num_to_label(port)
        return port

    def label_to_num(self, label):
        """
        Returns the port number associated with a label ``label``
        """
        return self.port_labels.get(label)

    def num_to_label(self, num):
        """
        Returns the label associated with a port number ``num``
        """
        return self.rev_port_labels.get(num)
