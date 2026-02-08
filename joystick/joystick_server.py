import socket
import struct
import pickle
import pygame
import json
from pathlib import Path


class JoystickListener:
    def __init__(self):
        self._joystick = None

        self._button_count = 12 # DEFAULT - WILL CHANGE WHEN JOYSTICK IS CONNECTED

        self._connect()


    def listen(self):
        """
        Returns joystick events
        """
        try:
            if not self._joystick:
                if not self._connect():
                    print("Quitting Joystick Teleoperation...")
                    return
                    
            events = []
            for event in pygame.event.get():
                    events.append(event)

            return events
                    
        except Exception as e:
            print(f"Error running joystick teleoperation: {e}")
            return None
        

    def _connect(self):
        """
        Private function to establish connection with the joystick
        Returns: 0 if no joystick is detected,
                    1 if joystick is detected
        """
        try:
            pygame.init()
            pygame.joystick.init()

            if pygame.joystick.get_count() == 0:
                print("No Joystick Detected!")
                return False
            else:
                self._joystick = pygame.joystick.Joystick(0)
                self._joystick.init()

                print(f"Joystick Connected: {self._joystick.get_name()}")

                self._button_count = self._joystick.get_numbuttons()

                return True
            
        except Exception as e:
            print(f"Error Connecting to Joystick: {e}")
            return False


def serialize_event(event):
    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
        return {
            "type": "button",
            "button": event.button,
            "pressed": event.type == pygame.JOYBUTTONDOWN,
        }

    # only buttons are supported for now
    # elif event.type == pygame.JOYAXISMOTION:
    #     return {
    #         "type": "axis",
    #         "axis": event.axis,
    #         "value": float(event.value),
    #     }

    # elif event.type == pygame.JOYHATMOTION:
    #     return {
    #         "type": "hat",
    #         "hat": event.hat,
    #         "value": event.value,  
    #     }

    return None


HOST = '172.23.112.1'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print(f"Joystick Server listening on {HOST}:{PORT} ...")

listener = JoystickListener()
button_count = listener._button_count

conn = None  # so we can close it safely later

try:
    while True:
        print("Waiting for a client to connect...")
        conn, addr = s.accept()
        print(f"Client connected from {addr}")

        try:
            # send button count once
            count = pickle.dumps(button_count)
            conn.sendall(struct.pack(">L", len(count)) + count)

            while True:
                raw_events = listener.listen()
                
                events = []

                for e in raw_events:
                    serialized = serialize_event(e)
                    if serialized is not None:
                        events.append(serialized)

                data = pickle.dumps(events)
                conn.sendall(struct.pack(">L", len(data)) + data)

        except (ConnectionResetError, BrokenPipeError):
            print(f"Client {addr} disconnected")

        finally:
            if conn:
                conn.close()
                conn = None

except KeyboardInterrupt:
    print("\nShutting down server...")

finally:
    if conn:
        conn.close()
    s.close()
    print("Joystick Server shut down")

