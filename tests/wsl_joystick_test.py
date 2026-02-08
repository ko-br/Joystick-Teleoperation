from joystick.joystick_client import JoystickClient

def main():
    client = JoystickClient()

    while True:
        ok, data = client.listen()


if __name__ == "__main__":
    main()