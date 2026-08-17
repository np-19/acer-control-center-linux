#!/usr/bin/env python3

import sys
import time
import signal
import threading

LED_PATH = "/sys/class/leds/rgb:kbd_backlight/multi_intensity"
BRIGHTNESS_PATH = "/sys/class/leds/rgb:kbd_backlight/brightness"

last_color = (255, 255, 255)


def write_file(path, value):
    with open(path, "w") as f:
        f.write(str(value))


def set_color(r, g, b):
    global last_color

    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    write_file(
        LED_PATH,
        f"{r} {g} {b}"
    )

    last_color = (r, g, b)


def set_brightness(value):
    value = max(0, min(255, int(value)))
    write_file(BRIGHTNESS_PATH, value)


def turn_off():
    set_color(0, 0, 0)


def restore_white():
    set_color(255, 255, 255)


def rainbow(stop_event=None):
    colors = [
        (255, 0, 0),       # Red
        (255, 80, 0),      # Orange
        (255, 255, 0),     # Yellow
        (0, 255, 0),       # Green
        (0, 255, 255),     # Cyan
        (0, 0, 255),       # Blue
        (128, 0, 255),     # Purple
        (255, 0, 255),     # Magenta
    ]

    def stopped():
        return stop_event is not None and stop_event.is_set()

    while not stopped():

        for color in colors:

            if stopped():
                return

            # Set the new colour while the keyboard is dim
            set_color(*color)

            # Brighten up
            for brightness in range(20, 256, 5):
                if stopped():
                    return

                set_brightness(brightness)
                time.sleep(0.025)

            # Stay bright for a moment
            time.sleep(0.4)

            # Dim down smoothly
            for brightness in range(255, 19, -5):
                if stopped():
                    return

                set_brightness(brightness)
                time.sleep(0.025)

            # Small pause before changing colour
            time.sleep(0.2)


def breathing_purple(stop_event=None):

    while stop_event is None or not stop_event.is_set():

        # Fade in
        for brightness in range(10, 256, 5):

            if stop_event is not None and stop_event.is_set():
                return

            set_color(
                int(brightness * 0.55),
                0,
                brightness
            )

            time.sleep(0.025)

        # Fade out
        for brightness in range(255, 9, -5):

            if stop_event is not None and stop_event.is_set():
                return

            set_color(
                int(brightness * 0.55),
                0,
                brightness
            )

            time.sleep(0.025)


def cleanup(signum=None, frame=None):
    try:
        restore_white()
    except Exception:
        pass

    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def menu():

    print()
    print("Acer RGB Keyboard")
    print("-----------------")
    print("1. Red")
    print("2. Green")
    print("3. Blue")
    print("4. Purple")
    print("5. White")
    print("6. Orange")
    print("7. Cyan")
    print("8. Yellow")
    print("9. Magenta")
    print("10. Rainbow")
    print("11. Breathing Purple")
    print("12. Off")
    print("0. Exit")
    print()

    choice = input("Choose: ").strip()

    if choice == "1":
        set_color(255, 0, 0)

    elif choice == "2":
        set_color(0, 255, 0)

    elif choice == "3":
        set_color(0, 0, 255)

    elif choice == "4":
        set_color(128, 0, 255)

    elif choice == "5":
        set_color(255, 255, 255)

    elif choice == "6":
        set_color(255, 80, 0)

    elif choice == "7":
        set_color(0, 255, 255)

    elif choice == "8":
        set_color(255, 255, 0)

    elif choice == "9":
        set_color(255, 0, 255)

    elif choice == "10":
        rainbow()

    elif choice == "11":
        breathing_purple()

    elif choice == "12":
        turn_off()

    elif choice == "0":
        return

    else:
        print("Invalid choice.")


if __name__ == "__main__":

    try:
        menu()

    except KeyboardInterrupt:
        cleanup()
