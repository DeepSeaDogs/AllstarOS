<!-- 
To Use: Start with dash (-), then copy white box or green check box icon for new line

Copy and paste green check box over white box to mark as 'done'
-->
# Software Checklist

## Setup
- :white_check_mark: Create Raspian OS SD card
- :white_check_mark: Configure eth0
  - 192.168.1.50 (Pi)
  - 192.168.1.1 (PC)
- :black_square_button: Configure WiFi
- :black_square_button: Update system
- :black_square_button: Install additional packages
  - ⬜ Python
  - ⬜ Camera drivers
  - ⬜ Controller

## Development
- :white_check_mark: Get camera working from Pi to PC
- ⬜ Get controller working on Pi
- ⬜ Build Python code
  - lotsa things here
- ⬜ Built PC code?
  - a few things here

## Design Decisions
- :white_check_mark: No Arduinos
  - Thrusters connect to Pi
  - Need 6 PWM pins
- :bulb: Timezone
  - Should Pi and PC be set to timezone of competition location
- ⬜ How does PC display status from Pi?
  - Browser/Python/VNC?
- ⬜ What status data is needed on the PC?

# Emoji Codes
| Emoji | Code                     | Meaning |
|--------|--------------------------|-|
| :black_square_button: | `:black_square_button:`|To Do|
| ✅     | `:white_check_mark:`     |Complete|
| ❌     | `:x:`                    |Won't Do / No|
| :question: | `:question:` | Question |
| 🚀     | `:rocket:`               ||
| 🐛     | `:bug:`                  |Problem/Bug|
| 🔥     | `:fire:`                 |Hot Item / Priority|
| 💡     | `:bulb:`                 |Idea / Need Input|
| 🛠️     | `:hammer_and_wrench:`   ||
| 📦     | `:package:`              ||
| 👀     | `:eyes:`                 |Need Help|
| 📝     | `:memo:`                 ||
