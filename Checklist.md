<!-- 
To Use: Start with dash (-), then copy white box or green check box icon for new line

Use the Emoji Table at the bottom to include status icons
-->
# Software Checklist

## Setup
- :white_check_mark: Create Raspian OS SD card
- :white_check_mark: Configure eth0
  - 192.168.1.50 (Pi)
  - 192.168.1.1 (PC)
- :white_check_mark: Configure WiFi
- :white_check_mark: Update system
- :white_check_mark: Install additional packages
  - :white_check_mark: Python
  - :white_check_mark: Camera drivers
  - :white_check_mark: Controller

## Development
- :white_check_mark: Get camera working from Pi to PC
- :white_check_mark: Get controller working on Pi
- :white_check_mark: Build Python code
  - lotsa things here
- :white_check_mark: Built PC code
  - main
  - camera_client

## Design Decisions
- :white_check_mark: No Arduinos
  - Thrusters connect to Pi
  - Need 6 PWM pins
- :bulb: Timezone
  - Should Pi and PC be set to timezone of competition location
- :question: How does PC display status from Pi?
  - Browser/Python/VNC?
- :question: What status data is needed on the PC?

# Emoji Codes
| Emoji | Code                     | Meaning |
|--------|--------------------------|-|
| :black_square_button: | `:black_square_button:`|To Do|
| ✅     | `:white_check_mark:`     |Complete|
| ❌     | `:x:`                    |Won't Do / No|
| :question: | `:question:` | Question |
| 🐛     | `:bug:`                  |Problem/Bug|
| 🔥     | `:fire:`                 |Hot Item / Priority|
| 💡     | `:bulb:`                 |Idea / Need Input|
| 👀     | `:eyes:`                 |Need Help|
