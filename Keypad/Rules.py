"""
Docstring
"""

# from inspect import isfunction (vi bruker ikke denne likevel. Avklart
# med studass)


class Rules:
    """
    Docstring
    """

    def __init__(self, current_state, next_state, signal, action):
        """
        Docstring
        """
        self.current_state = current_state
        self.next_state = next_state
        self.signal = signal
        self.action = action

    def match(self, state1, signal):
        """
        Docstring
        """
        return self.current_state == state1 and signal in self.signal

    def dummy(self):
        """
        Docstring
        """
        print(self.signal) # brukes ikke lol
