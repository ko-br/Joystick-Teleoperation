import pygame 

class JoystickTeleoperation:
    def __init__(self, *handlers):
        """
        Accepts any number of handler functions in order
        """
        self._handlers = list(handlers)
        self._joystick = None
        self._button_count = 12 # DEFAULT - WILL CHANGE WHEN JOYSTICK IS CONNECTED

        # # predefined button mapping. can be changed by running remap
        # self._button_map = {}
        # for i, handler in enumerate(self._handlers):
        #     self._button_map[i] = handler # assign buttons to handlers in order
        
        # self._print_button_map()


    def run(self):
        """
        Main function to start data collection using the joystick
        """
        try:
            if not self._joystick:
                if not self._connect():
                    print("Quitting Joystick Teleoperation...")
                    return
                    
            pygame.event.pump()
            for i in range(self._joystick.get_numbuttons()):
                if self._joystick.get_button(i): # if button pressed
                    handler = self._button_map.get(i) #  get handlr
                    if handler:                     
                        handler() # call handler

        except Exception as e:
            print(f"Error running joystick teleoperation: {e}")
            return


    def remap(self, button, function):
        """
        Remap a button on a joystick to a specific function. 
        Parameters: 
            Button: Number of the button on the joystick (check docs)
            Function: Function to be mapped to the button (should match name of handler function)
        """
        try:
            if button in self._button_map:
                self._button_map[button] = function  
                print(f"{function.__name__} mapped to Button {button}")

                self._print_button_map()
            else:
                print(f"Button {button} does not exist on this joystick")

        except Exception as e:
            print(f"Error remapping: {e}")


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
                for i in range(self._button_count):
                    if i < len(self._handlers):
                        self._button_map[i] = self._handlers[i]
                    else:
                        self._button_map[i] = None 

                self._print_button_map()

                return True
            
        except Exception as e:
            print(f"Error Connecting to Joystick: {e}")
            return False


    def _print_button_map(self):
        # print out the button mapping
        print("Button Functions:")
        for button, handler in self._button_map.items():
            if handler:
                print(f"Button {button}: {handler.__name__}")
            else: 
                print(f"Button {button}: None")
            


