# Pico Thermometer

![Pico Thermometer](assets/device.jpg)

This project turns a Raspberry Pi Pico with a Pimoroni Pico Display into a smart, dual-function thermometer. It displays the local room temperature using its onboard sensor and can show a pre-set "outside" temperature with the press of a button.

---

## Features

* **Room Thermometer:** Displays the current room temperature in both Celsius and Fahrenheit.
* **Static Outside Temperature:** Pressing the 'A' button shows a pre-defined placeholder temperature for "Outside" for 5 seconds.
* **Graphical Interface:** A visually appealing thermometer graphic fills up and changes color from a cool blue/green to a hot red based on the room's temperature.
* **Fully Offline:** The device does not require any internet connection to function.
* **Modular Code:** The project is split into `main.py` and `a.py` to keep the code clean and easy to understand.

---

## Hardware Requirements

* **Raspberry Pi Pico** (or Pico W)
* **Pimoroni Pico Display Pack**
* **Micro USB Cable** for power and programming

---

## Software & Setup

This project runs on MicroPython.

### 1. Install MicroPython

First, you need to install the Pimoroni-flavored MicroPython firmware on your Pico.
* Download the latest `.uf2` file from their GitHub page: [Pimoroni Pico MicroPython Releases](https://github.com/pimoroni/pimoroni-pico/releases)
* Hold down the **BOOTSEL** button on your Pico while plugging it into your computer. It will appear as a drive called **RPI-RP2**.
* Drag and drop the downloaded `.uf2` file onto the drive. The Pico will automatically restart with MicroPython installed.

### 2. Set Up Project Files

Using an editor like [Thonny](https://thonny.org/), connect to your Pico and create the following two files using the code you have.

#### `a.py`
This module is responsible for displaying the "Outside Temperature" screen when called from `main.py`.

#### `main.py`
This is the main application that runs the room thermometer display and listens for the 'A' button press.

Your Pico's file structure should look like this:

/
├── main.py
└── a.py

---

## How to Use

Once the files are saved to your Pico, it will automatically start displaying the room thermometer.

* **View Room Temperature:** The main screen shows the temperature of the room where the device is located.
* **View "Outside" Temperature:** Press the **'A' button** on the Pico Display. The screen will switch to show the static temperature for Revere, MA (15.5°C) for 5 seconds before returning to the room thermometer.