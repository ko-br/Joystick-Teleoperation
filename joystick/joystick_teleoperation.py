import pygame 
import json
from pathlib import Path

class JoystickTeleoperation:
    def __init__(self, *handlers):
        """
        Accepts any number of handler functions in order
        """
        self._handlers = list(handlers)

        self._handler_map = {
            handler.__name__: handler for handler in self._handlers
        }


        self._joystick = None
        self._button_count = 12 # DEFAULT - WILL CHANGE WHEN JOYSTICK IS CONNECTED
        self._button_map = None

        self._connect()


    def run(self):
        """
        Main function to start data collection using the joystick
        """
        try:
            if not self._joystick:
                if not self._connect():
                    print("Quitting Joystick Teleoperation...")
                    return
                    
            for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = event.button
                        handler = self._button_map.get(button) #  get handlr
                        if handler:                     
                            handler() # call handler

        except Exception as e:
            print(f"Error running joystick teleoperation: {e}")
            return


    def remap(self, button, function):
        """
        Remap a button on a joystick to a specific function. 
        Button: Number of the button on the joystick
        Function: Function to be mapped to the button 
        """
        self._check_connection()

        try:
            if button in self._button_map:
                self._button_map[button] = function  
                print(f"{function.__name__} mapped to Button {button}")

                self.print_button_mapping()
            else:
                print(f"Button {button} does not exist on this joystick")

        except Exception as e:
            print(f"Error remapping: {e}")


    def configure(self):
        """
        Remap all functions to buttons
        """
        self._check_connection() 

        print("\n=== Joystick Configuration Mode ===")
        print("Press a button to assign it to each function.")

        # reset all mappings
        for button in self._button_map:
            self._button_map[button] = None 

        for handler in self._handlers:
            print(f"Press a button for: { handler.__name__}")

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = event.button

                        self._button_map[button] = handler

                        print(f"{handler.__name__} mapped to Button {button}")
                        break 
                else:
                    continue
                break


        print("Configuration complete!")
        self.print_button_mapping()       


    def identify_buttons(self):
        """
        Prints the index of any joystick button that is pressed.
        Used to identify button numbers for mapping.
        """
        self._check_connection()

        print("Click a button to identify:") 
        while True:

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    print(f"Button {button} pressed")
                    print()
                    print("Click a button to identify:")


    def save_configuration(self, filename = "configurations/button_configuration.json"):
        """
        Save current button mapping/joystick configuration to a file to load later
        """
        try:
            data = {
                str(button): (handler.__name__ if handler else None)
                for button, handler in self._button_map.items()
            }

            path = Path(filename)
            path.parent.mkdir(parents = True, exist_ok = True)

            with open(filename, "w") as file:
                json.dump(data, file, indent = 4)


            print(f"Configuration saved to {filename}")

        except Exception as e:
            print(f"Error saving configuration: {e}")


    def load_configuration(self, filename):
        """
        Load button mapping/joystick configuration from a file
        """
        try:
            if not Path(filename).exists():
                print(f"{filename} not found")
                return 
            
            with open(filename, "r") as file:
                data = json.load(file)

            for button_str, handler_name in data.items():
                button = int(button_str)

                if button not in self._button_map:
                    print(f"Warning: button {button} does not exist on this joystick")
                    continue

                if handler_name is None:
                    self._button_map[button] = None 
                else:
                    handler = self._handler_map.get(handler_name) # handler_map is a dict mapping string names to functions

                    if handler:
                        self._button_map[button] = handler
                    else:
                        print(f"Warning: '{handler_name}' not found")

            print(f"Configuration loaded from {filename}")
            self.print_button_mapping()

        except Exception as e:
            print(f"Error loading configuration: {e}")


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

                self._button_map = {}
                button_start_index = 4 # the number of buttons to avoid in default mapping (buttons 0-3)

                for i in range(self._button_count):
                    if i < button_start_index:
                    # to ignore buttons 0-3 to avoid accidental triggers using the right stick
                        self._button_map[i] = None
                    elif i - button_start_index < len(self._handlers):
                        self._button_map[i] = self._handlers[i - button_start_index]
                    else:
                        self._button_map[i] = None

                self.print_button_mapping()

                return True
            
        except Exception as e:
            print(f"Error Connecting to Joystick: {e}")
            return False

    def _check_connection(self):
        if not self._joystick:
            raise RuntimeError("No joystick detected")


    def print_button_mapping(self):
        # print out the button mapping
        print("Button Functions:")
        for button, handler in self._button_map.items():
            if handler:
                print(f"Button {button}: {handler.__name__}")
            else: 
                print(f"Button {button}: None")
            


