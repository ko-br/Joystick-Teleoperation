from joystick.joystick_teleoperation import JoystickTeleoperation

# test handlers
def jog():
    print("Jogging enabled")

def capture_input():
    print("Input data captured")

def capture_output():
    print("Output data captured")


def main():
    joystick = JoystickTeleoperation(jog, capture_input, capture_output)

    joystick.configure()
    joystick.save_configuration("configurations/data_collection_config.json")

    try:
        print("Starting joystick teleoperation test")
        while True:
            joystick.run()

    except Exception as e:
        print(f"Test terminated: {e}")


if __name__ == "__main__":
    main()