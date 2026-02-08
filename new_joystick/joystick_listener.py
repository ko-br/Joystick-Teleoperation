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
                    
            events = {}
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








