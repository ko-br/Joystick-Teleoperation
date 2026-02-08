import argparse
from joystick.joystick_teleoperation import JoystickTeleoperation

# test handlers
def jog():
    print("Jogging enabled")

def capture_input():
    print("Input data captured")

def capture_output():
    print("Output data captured")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--runtime",
        choices=["native", "wsl"],
        default="wsl"
    )

    args = parser.parse_args()

    runtime = args.runtime 

    if runtime == "wsl":
        from joystick.joystick_client import JoystickClient
        client = JoystickClient()
        joystick = JoystickTeleoperation(client, jog, capture_input, capture_output)

    else:
        joystick = JoystickTeleoperation(None, jog, capture_input, capture_output)

    joystick.configure()
    joystick.save_configuration("configurations/data_collection_config.json")

    try:
        print("Starting joystick teleoperation test")
        while True:
            joystick.run()

    except Exception as e:
        print(f"Test terminated: {e}")

#TODO: update readme

if __name__ == "__main__":
    main()