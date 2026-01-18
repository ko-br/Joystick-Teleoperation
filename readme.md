# Joystick Teleoperation

A lightweight Python library for integrating game controllers into robotics projects. Map joystick buttons to custom functions with minimal setup.



## Features

- **Plug-and-play**: Automatically detects and connects to any joystick supported by `pygame`
- **Dynamic mapping**: Assign and reassign handler functions to buttons at runtime
- **Button identification**: Built-in tool to discover button indices on your specific controller
- **Configuration persistence**: Save and load button mappings to JSON files
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

---

## Configuration Workflow

### Option 1: Interactive Configuration

Use the built-in configuration function to assign buttons interactively:

```
controller = JoystickTeleoperation(move_forward, move_backward, emergency_stop)

# Start interactive configuration
controller.configure()
# Console prompts:
# === Joystick Configuration Mode ===
# Press a button to assign it to each function.
# Press a button for: move_forward
# (press button 3)
# move_forward mapped to Button 3
# Press a button for: move_backward
# (press button 5)
# move_backward mapped to Button 5
# Configuration complete!
# Button Functions:
# Button 3: move_forward
# Button 5: move_backward
# Button 7: emergency_stop

# Save configuration for future use
controller.save_configuration()
# Configuration saved to configurations/button_configuration.json
```

### Option 2: Load Previous Configuration

Reload a saved configuration without reconfiguring:

```
controller = JoystickTeleoperation(move_forward, move_backward, emergency_stop)

# Load previously saved button mapping
controller.load_configuration("configurations/button_configuration.json")
# Configuration loaded from configurations/button_configuration.json
# Button Functions:
# Button 3: move_forward
# Button 5: move_backward
# Button 7: emergency_stop

# Now ready to use with saved mappings
while True:
    controller.run()
```


### Dynamic Remapping

Change button assignments on the fly:
```
# Remap emergency_stop to button 5
controller.remap(5, emergency_stop)
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

### `configure()`

**Interactive configuration wizard - Assign buttons step-by-step**

Enters an interactive mode that prompts you to press a button for each handler function. All previous mappings are cleared before configuration starts.

**Usage:**
```python
controller.configure()

# Console interaction:
# === Joystick Configuration Mode ===
# Press a button to assign it to each function.
# Press a button for: move_forward
# (you press button 5)
# move_forward mapped to Button 5
# Press a button for: move_backward
# (you press button 7)
# move_backward mapped to Button 7
# Configuration complete!
# Button Functions:
# Button 5: move_forward
# Button 7: move_backward
```

**Tip:** Run `configure()` once, then `save_configuration()` to avoid reconfiguring every time.

---

### `save_configuration(filename="configurations/button_configuration.json")`

**Save current button mapping to a JSON file**

**Parameters:**
- `filename` (str, optional): Path to save configuration file. Defaults to `"configurations/button_configuration.json"`.

**Behavior:**
- Creates `configurations/` directory if it doesn't exist
- Saves button-to-function mappings in JSON format
- Overwrites existing file if present

**Example:**
```python
# Save to default location
controller.save_configuration()
# Configuration saved to configurations/button_configuration.json

# Save to custom location
controller.save_configuration("my_custom_config.json")
# Configuration saved to my_custom_config.json
```

**Generated JSON format:**
```json
{
    "0": null,
    "1": null,
    "2": "move_forward",
    "3": "move_backward",
    "4": "emergency_stop"
}
```

---

### `load_configuration(filename)`

**Load button mapping from a saved JSON file**

**Parameters:**
- `filename` (str): Path to configuration file to load

**Behavior:**
- Reads JSON file and applies button mappings
- Skips buttons that don't exist on current joystick (with warning)
- Skips handler functions not provided to constructor (with warning)
- Prints updated button mapping to console

**Example:**
```python
# Load from default location
controller.load_configuration("configurations/button_configuration.json")

# Load from custom location
controller.load_configuration("my_custom_config.json")

# Output:
# Configuration loaded from my_custom_config.json
# Button Functions:
# Button 2: move_forward
# Button 3: move_backward
# Button 4: emergency_stop
```

**Error handling:**
- If file doesn't exist: prints error message, mapping unchanged
- If handler not found: prints warning, skips that button
- If button doesn't exist: prints warning, skips that mapping

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


