# Joystick Teleoperation

A lightweight Python library for integrating game controllers into robotics projects. Map joystick buttons to custom functions with minimal setup.



## Features

- **Plug-and-play**: Automatically detects and connects to any joystick supported by `pygame`
- **Dynamic mapping**: Assign and reassign handler functions to buttons at runtime
- **Button identification**: Built-in tool to discover button indices on your specific controller
- **Handler-based architecture**: Separates input handling from application logic

## Project Structure

```
joystick-teleoperation/
├── src/
│   ├── joystick/
│   │   ├── __init__.py
│   │   └── joystick_teleoperation.py
│   └── tests/ 
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```
git clone https://github.com/ko-br/Joystick-Teleoperation
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

**Dependencies:**
- `pygame>=2.0.0` (for joystick/controller support)


## Quick Start

### Basic Usage
```
from modules.joystick_teleoperation import JoystickTeleoperation

# Define your handler functions
def move_forward():
    print("Moving forward")

def move_backward():
    print("Moving backward")

def emergency_stop():
    print("Emergency stop!")

# Initialize controller with handlers
# Handlers are auto-mapped to buttons 0, 1, 2, ...
controller = JoystickTeleoperation(
    move_forward,
    move_backward,
    emergency_stop
)

# Main loop
while True:
    controller.run()

```

### Dynamic Remapping

Change button assignments on the fly:
```
# Remap emergency_stop to button 5
controller.remap(5, emergency_stop)

# Button 2 is now unmapped, button 5 triggers emergency_stop
```

### Identifying Buttons

Don't know which button is which? Use the built-in identifier:

```
controller.identify_buttons()
# Press buttons on your controller to see their indices
# Output: "Button 3 pressed", "Button 7 pressed", etc.
# Press Ctrl+C to exit
````


## API Reference

### `JoystickTeleoperation(*handlers)`

**Constructor** - Initialize the joystick controller

**Parameters:**
- `*handlers` (callable): Variable number of handler functions. Automatically mapped to buttons 0, 1, 2, ... in order.

**Raises:**
- Prints "No Joystick Detected!" if no controller is connected

**Example:**
```
def jog_x():
    robot.jog('X', 0.01)

def jog_y():
    robot.jog('Y', 0.01)

controller = JoystickTeleoperation(jog_x, jog_y)
# jog_x is mapped to Button 0
# jog_y is mapped to Button 1

```

### `run()`

**Main execution loop** - Process joystick input and trigger handlers

Call this repeatedly (e.g., in a `while` loop) to detect button presses and execute associated handler functions.

**Returns:** None

**Example:**
```
while True:
    controller.run()
    time.sleep(0.01)  # Optional: small delay for CPU efficiency
```
---

### `remap(button, function)`

**Dynamically reassign a handler function to a different button**

**Parameters:**
- `button` (int): Button index to map to (0–11 on most controllers)
- `function` (callable): Handler function to assign

**Behavior:**
- Unmaps the function from its previous button (if assigned elsewhere)
- Assigns function to the new button
- Prints updated button mapping to console
- Raises error if button does not exist on connected joystick

**Example:**
```
# Move emergency_stop from button 2 to button 11
controller.remap(11, emergency_stop)

# Output:
# emergency_stop mapped to Button 11
# Button Functions:
# Button 0: jog_x
# Button 1: jog_y
# ...
# Button 11: emergency_stop'
```

---

### `identify_buttons()`

**Interactive tool to discover button indices on your controller**

Enters an infinite loop that prints the index of any button you press. Useful for understanding your specific controller's layout.

**Usage:**
```
controller.identify_buttons()
# Press buttons on your controller
# Console output:
# Click a button to identify:
# Button 3 pressed
#
# Click a button to identify:
# Button 7 pressed
# ...
# (Press Ctrl+C to exit)
```



## Testing

Run the included test script, which demonstrates handler mapping and button press detection:
```
cd src
python -m tests.joystick_teleop_test
```

---
## Controller Compatibility

**Should work with any controller recognized by pygame.joystick.**

### Finding Your Controller's Button Layout

If unsure about button numbers on your controller:
```
controller.identify_buttons()
```

Then press each button to see its index. Common layouts:

**PlayStation 2 Controller:**
- Triangle: 0
- Circle: 1
- X: 2
- Square: 3
- L1: 4
- R1: 5
- L2: 6
- R2: 7
- Select: 8
- Start: 9
- L3: 10
- R3: 11
- Mode: 12
---


## Roadmap

**Current Status:** Core functionality complete

**Planned Features:**
- [ ] D-pad support 
- [ ] `map_all()` method for bulk remapping
- [ ] Configuration file support (YAML/JSON to save/load button mappings)
- [ ] Button press duration tracking (detect hold vs tap)

---

