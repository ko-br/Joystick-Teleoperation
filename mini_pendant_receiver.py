import bluetooth # placeholder -- replace with actual library


class MiniPendantReceiver:
    """
    Class to receive and process bluetooth signals from mini pendant
    """
    def __init__(self):
        self._server_sock = None 
        self._client_sock = None
        self._connected = False 


    def run(self):
        """
        Main function.
        Starts the connection, listens for signals, parses them, and returns the data
        (ONLY RUNS ONCE -- LOOP THIS FUNCTION)
        """
        self._start()



    def _start(self, port = 1):
        """
        Start the bluetooth receiver  

        Parameters:
            Port: Bluetooth RFCOMM channel number, 1 is the default

        Outputs:


        """
        try:
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_sock.bind(("", port))
            self.server_sock.listen(1)

            print("Starting Mini Pendant Receiver...")

            self._client_sock, address = self.server_sock.accept() # address is address of the device

            print(f"Connected to Mini Pendant at address: {address}")
            self._connected = True

        except Exception as e:
            print(f"Error connecting to Mini Pendant: {e}")
            self._connected = False 

    def _listen(self):
        """
        Listen for bluetooth signal and parse it

        Returns:
            Parsed command
        """

        raw_data = self._client_sock.recv









