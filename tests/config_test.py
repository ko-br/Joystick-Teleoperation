from joystick.joystick_teleoperation import JoystickTeleoperation

def random_function_1():
    print("Random function 1 triggered")

def random_function_2():
    print("Some other random function 2 triggered")

def random_function_3():
    print("Yet another random function 3 triggered")

def random_function_4():
    print("Completely different random function 4 triggered")



def main():
    print("\n--- Initializing joystick teleoperation ---\n")

    teleop = JoystickTeleoperation(
        random_function_1,
        random_function_2,
        random_function_3,
        random_function_4,
    )

    # print("\n--- Remapping buttons ---\n")

    # teleop.remap(5, random_function_3)
    # teleop.remap(7, random_function_1)
    # teleop.remap(2, random_function_4)
    # teleop.remap(3, random_function_2)

    teleop.configure()

    print("\n--- Saving configuration ---\n")

    teleop.save_configuration("configurations/test_config.json")
    # teleop.save_configuration()


    print("\n--- Clearing mappings ---\n")
    for button in teleop._button_map:
        teleop._button_map[button] = None

    teleop.print_button_mapping()

    print("\n--- Loading configuration ---\n")
    teleop.load_configuration("configurations/test_config.json")

    while True:
        teleop.run()

if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"Error: {e}")
