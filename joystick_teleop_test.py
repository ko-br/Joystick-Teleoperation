from joystick_teleoperation import JoystickTeleoperation


# test handlers
def jog():
    print("Jogging enabled")

def capture_input():
    print("Input data captured")

def capture_output():
    print("Output data captured")


def main():
    joystick = JoystickTeleoperation(jog, capture_input, capture_output)

    joystick.remap(7, capture_input)
    try:
        print("Starting joystick teleoperation test")
        while True:
            joystick.run()

    except Exception as e:
        print(f"Test terminated: {e}")


if __name__ == "__main__":
    main()