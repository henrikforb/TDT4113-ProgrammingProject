"""
Docstring
"""

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


class LedBoard:
    """
    Docstring
    """

    def __init__(self):
        """
        Docstring
        """
        self.setup()

    pins = [18, 23, 24]

    pin_led_states = [
        [1, 0, -1],  # A
        [0, 1, -1],  # B
        [-1, 1, 0],  # C
        [-1, 0, 1],  # D
        [1, -1, 0],  # E
        [0, -1, 1]  # F
    ]

    def set_pin(self, pin_index, pin_state):
        """
        :param pin_index: which led are we looking at from the pins list
        :param pin_state: 0,1 or -1 where 0 meaning shutting of, 1 turning
        on and -1 is shutting down the circuit
        :return:
        """
        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def light_led(self, led_number):
        """
        :param led_number: which state from A-F
        :return:
        """
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)

    def turn_off(self):
        """turn of all the leds"""
        self.set_pin(0, -1)
        self.set_pin(1, -1)
        self.set_pin(2, -1)

    def setup(self):  # Set the proper mode via: GPIO.setmode(GPIO.BCM).
        """
        Docstring
        """
        self.turn_off()

    def flash_all_leds(self):
        """
        Docstring
        """
        for i in range(6):
            self.light_led(i)
            time.sleep(0.1)
            self.turn_off()

    def twinkle_all_leds(self):
        """blink"""
        for i in range(6):
            self.light_led(i)
            time.sleep(1)
            self.turn_off()


if __name__ == "__main__":
    HALLO = LedBoard()
    HALLO.twinkle_all_leds()
