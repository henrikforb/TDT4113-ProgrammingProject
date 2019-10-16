"""
Docstring
"""


import time
import RPi.GPIO as GPIO



class Keypad:
    """
    Docstring
    """

    def __init__(self):
        """
        Docstring
        """
        self.keypad = [['1', '2', '3'],
                       ['4', '5', '6'],
                       ['7', '8', '9'],
                       ['*', '0', '#']]
        self.rows = [19, 13, 6, 5]  # list of pin numbers for row
        self.cols = [27, 17, 4]  # list of pin numbers of col

        self.setup()

    def setup(self):
        """
        Docstring
        """
        # Set the proper mode via: GPIO.setmode(GPIO.BCM). Also, use GPIO functions to
        # set the row pins as outputs and the column pins as inputs.
        GPIO.setmode(GPIO.BCM)
        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)
        for col in self.cols:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # - Use nested loops (discussed above) to determine the key currently being pressed
    def do_polling(self):
        """
        Docstring
        """
        self.reset_all_pins()
        for i in range(len(self.rows)):
            GPIO.output(self.rows[i], GPIO.HIGH)
            for j in range(len(self.cols)):
                if GPIO.input(self.cols[j]) == GPIO.HIGH:  # debouncing
                    time.sleep(0.01)
                    if GPIO.input(self.cols[j]) == GPIO.HIGH:  # debouncing
                        while GPIO.input(self.cols[j]) == GPIO.HIGH:
                            pass
                        return str(self.keypad[i][j])
            GPIO.output(self.rows[i], GPIO.LOW)
        return None

    # This is the main interface between the agent and the Keypad. It should
    def get_next_signal(self):
        """
        Docstring
        """
        # initiate repeated calls to do polling until a key press is detected.
        signal = self.do_polling()
        while signal is None:
            signal = self.do_polling()
        return signal

    def reset_all_pins(self):
        """
        Docstring
        """
        for row in self.rows:
            GPIO.output(row, GPIO.LOW)


if __name__ == "__main__":
    KEYPAD = Keypad()

    print(KEYPAD.get_next_signal())
