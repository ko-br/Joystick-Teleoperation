# to be run on WSL2 to receive joystick data from windows
import socket
import pickle
import struct

class JoystickClient:
    def __init__(self):
        self.host = '172.23.112.1'  # WSL can access Windows localhost
        self.port = 8001

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.data = b""
        self.header_size = struct.calcsize(">L")

        self._button_count = self._recv_button_count()

    def _recv_button_count(self):
        # read message size
        while len(self.data) < self.header_size:
            packet = self.sock.recv(4096)
            if not packet:
                raise ConnectionError("Socket closed while reading button count")
            self.data += packet

        packed_size = self.data[:self.header_size]
        self.data = self.data[self.header_size:]
        msg_size = struct.unpack(">L", packed_size)[0]

        # read the full message
        while len(self.data) < msg_size:
            packet = self.sock.recv(4096)
            if not packet:
                raise ConnectionError("Socket closed while reading intrinsics")
            self.data += packet

        msg_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        return pickle.loads(msg_data)

    def listen(self):
        while len(self.data) < self.header_size:
            packet = self.sock.recv(4096)
            if not packet:
                return False, None
            self.data += packet

        packed_size = self.data[:self.header_size]
        self.data = self.data[self.header_size:]
        header_size = struct.unpack(">L", packed_size)[0]

        while len(self.data) < header_size:
            packet = self.sock.recv(4096)
            if not packet:
                return False, None
            self.data += packet

        payload_data = self.data[:header_size]
        self.data = self.data[header_size:]

        joystick_data = pickle.loads(payload_data)
        return True, joystick_data


    def release(self):
        self.sock.close()

