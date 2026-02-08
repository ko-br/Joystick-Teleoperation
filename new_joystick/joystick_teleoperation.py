import pygame 
import json
from pathlib import Path
from new_joystick.joystick_client import JoystickClient

class JoystickTeleoperation:
    def __init__(self, listener, *handlers):
        """
        Accepts any number of handler functions in order
        """
        self._handlers = list(handlers)
        self.listener = listener

        self._handler_map = {
            handler.__name__: handler for handler in self._handlers
        }


        self._button_count = 12
        self._button_map = {}

        self._map()

    
    def _map(self):
        self._button_count = self.listener._button_count
        button_start_index = 4

        for i in range(self._button_count):
            if i < button_start_index:
            # to ignore buttons 0-3 to avoid accidental triggers using the right stick
                self._button_map[i] = None
            elif i - button_start_index < len(self._handlers):
                self._button_map[i] = self._handlers[i - button_start_index]
            else:
                self._button_map[i] = None

        self.print_button_mapping()
    

    def run(self):
        """
        Main function to start data collection using the joystick
        """
        try:
            ok, events = self.listener.listen()
            if not ok:
                return

            for event in events:
                if event["type"] == "button" and event["pressed"]:
                    print(f"button pressed: {event["button"]}")
                    handler = self._button_map.get(event["button"]) #  get handlr
                    if handler:                     
                        handler() # call handler

        except Exception as e:
            print(f"Error running joystick teleoperation: {e}")
            return


    def print_button_mapping(self):
        # print out the button mapping
        print("Button Functions:")
        for button, handler in self._button_map.items():
            if handler:
                print(f"Button {button}: {handler.__name__}")
            else: 
                print(f"Button {button}: None")
            


