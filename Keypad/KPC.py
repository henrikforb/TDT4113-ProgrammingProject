#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Keypad import Keypad
from LedBoard import LedBoard
from Rules import Rules
import time


class FSM:
    def __init__(self):
        """
        Docstring
        """
        self.Rules = []
        self.state_init = State("State-Init")
        self.state_read = State("State-Read")
        self.state_verify = State("State-Verify")
        self.state_active = State("State-Active")
        self.state_led = State("State-Led")
        self.state_time = State("State-time")
        self.state_read_new = State("State-read-new")
        self.stare_read_confirm = State("State-read-confirm")
        self.state_logout = State("State-logout")
        self.state_done = State("State-done")
        self.state_read1 = State("read1")
        self.state_read2 = State("read2")
        self.current_state = self.state_init

    # add a new rule to the end of the rule list.
    def add_rule(self, state1, state2, signal, action):
        """
        Docstring
        :param state1:
        :param state2:
        :param signal:
        :param action:
        :return:
        """
        new_rule = Rules(state1, state2, signal, action)
        self.Rules.append(new_rule)

    # def get_next_signal(self, agent):  # query the agent for the next signal.
    #
    #     if isinstance(agent, KPC):
    #         return agent.get_next_signal()
    #     else:
    #         print('Not instance of KPC')

    # go through the rule set, in order, applying each rule until one of the
    # Rules is fired.
    def active_menu(self):
        """
        Docstring
        """
        print()
        time.sleep(2)
        print("Press * to change passwords")
        print("Press # to log out")
        print("Press a number (0-5) to make a LED light up")
        #print("Trykk saa et nytt tall mellom 0 og 9, etterfulgt av stjerne for aa bestemme hvor lenge leden skal lyse")

    def run_Rules(self, agent):
        """
        Docstring
        """
        # print(agent.override_signal)

        if agent.override_signal == 'Y':
            self.current_state = self.state_active
            agent.override_signal = None
            # print(self.current_state.name)

        elif agent.override_signal == 'N':
            self.current_state = self.state_init
            agent.override_signal = None
            # print(self.current_state.name)

        if self.current_state == self.state_active:
            self.active_menu()
        elif self.current_state == self.state_done:
            print("Successfully logged out!\n")
            time.sleep(1.5)
            print("Press any button to log in\n")

        signal = agent.get_next_signal()
        for rule in self.Rules:
            if rule.match(self.current_state, signal):
                self.current_state = rule.next_state
                #print("Button pressed:", signal)
                #print("Just entered state:", self.current_state.name)
                if rule.current_state == self.state_read and rule.next_state == self.state_read:
                    rule.action(signal)  # append new password digit
                elif rule.current_state == self.state_time and rule.next_state == self.state_time:
                    rule.action(signal)  # append next time digit
                elif rule.current_state == self.state_read1 and rule.next_state == self.state_read1:
                    rule.action(signal)
                elif rule.current_state == self.state_read2 and rule.current_state == self.state_read2:
                    rule.action(signal)
                else:
                    rule.action()
                break


class State:

    def __init__(self, name, final=False):
        """
        Docstring
        """
        self.name = name
        self.final = final


class KPC:
    def __init__(self):
        """
        Docstring
        """
        self.Keypad_pointer = Keypad()
        self.led_board_pointer = LedBoard()
        # pathname to the file holding the KPC's password
        self.password_file = 'password.txt'
        self.password_buffer = ""
        self.cache = ""
        # When the agent's decision is the next signal the FSM should receive
        self.override_signal = None
        self.led_id = None  # LED id (Lid)
        self.led_time = ""  # Lighting duration (Ldur)
        self.current_symbol = None

    def get_next_signal(self):  # Used by the FSM
        """
        Docstring
        """
        self.current_symbol = self.Keypad_pointer.get_next_signal()
        return self.current_symbol

    def init_password_entry(self):  # A1
        """
        Docstring
        """
        print("\nPlease enter the password:")
        self.start_action()  # Lightning pattern method in led_board
        self.password_buffer = ""

    def append_next_password_digit(self, digit):  # A2
        """
        Docstring
        """
        self.password_buffer += digit
        print("\r{}".format(self.password_buffer), end="")

    def verify_login(self):  # A3
        """
        Docstring
        """
        print("\n\nVerifying password...\n")
        with open(self.password_file) as file:
            password = file.readline()
            # print("Passordet er: {}".format(password))
            if self.password_buffer == password:
                self.override_signal = 'Y'
                self.twinkle_leds()  # Indicated correct password entered
                print("Correct password!")
            else:
                self.override_signal = 'N'
                self.flash_leds()  # Indicates wrong password entered
                self.password_buffer = ""
                print("Wrong password!\n")
                print("Press any button to try again.")

    def reset_agent(self):  # A4
        """
        Docstring
        """
        self.override_signal = None
        self.led_board_pointer.light_led(1)

    def fully_activate_agent(self):  # A5
        """
        Docstring
        """
        self.override_signal = None

    def refresh_agent(self):  # A6
        """
        Docstring
        """
        self.override_signal = None

    def init_new_password_entry(self):
        """
        Docstring
        """
        self.password_buffer = ""
        self.override_signal = None
        self.led_board_pointer.light_led(1)
        print("\nEnter a new password: ")

    def cache_password(self):  # A7
        """
        Docstring
        """
        self.cache = self.password_buffer
        self.password_buffer = ""
        print("\n\nEnter the new password again")

    def validate_password_change(self, a):  # A8
        """
        Docstring
        """
        print("\n\nComparing the two passwords...")
        if self.cache == self.password_buffer:
            with open(self.password_file, 'w') as file:
                file.write(self.password_buffer)
            self.twinkle_leds()
            print("\nSuccessfully updated password.")
            self.override_signal = 'Y'
        else:
            self.flash_leds()
            print("\nThe two passwords did not match.\n")
            print("You have been logged out. Press any button to log in again.")
            self.override_signal = 'N'

    def light_one_led(self):
        """
        Docstring
        """
        print("\n")
        print(
            "Lighting LED #{} for {} seconds is now lighting.".format(
                self.led_id,
                self.led_time))
        self.led_board_pointer.light_led(int(self.led_id))
        time.sleep(int(self.led_time))
        self.led_board_pointer.turn_off()
        self.led_time = ""

    def flash_leds(self):
        """
        Docstring
        """
        self.led_board_pointer.flash_all_leds()

    def twinkle_leds(self):
        """
        Docstring
        """
        self.led_board_pointer.twinkle_all_leds()

    def start_action(self):
        """
        Docstring
        """
        self.led_board_pointer.flash_all_leds()

    def exit_action(self):
        """
        Docstring
        """
        self.led_board_pointer.turn_off()  # Not written yet

    def log_out(self):
        """
        Docstring
        """
        print("\nPress again to log out :(\n")

    def confirm_logout(self):
        """
        Docstring
        """
        self.exit_action()

    def cache_led_id(self):
        """
        Docstring
        """
        print("\nLighting LED #" + self.current_symbol + " is chosen\n")
        self.led_id = self.current_symbol
        time.sleep(1.5)
        print("How many seconds do you want the LED to light?")
        # self.light_one_led(self.current_symbol)

    def append_next_time_digit(self):
        """
        Docstring
        """
        self.led_time += self.current_symbol
        print("\r{}".format(self.led_time), end="")


if __name__ == "__main__":
    agent = KPC()
    fsm = FSM()
    fsm.add_rule(
        fsm.state_init,
        fsm.state_read,
        "0123456789#",
        agent.init_password_entry)

    # Enter password (2 and 7)
    fsm.add_rule(
        fsm.state_read,
        fsm.state_read,
        "0123456789",
        agent.append_next_password_digit)

    # Completing password entry (2 and 7)
    fsm.add_rule(fsm.state_read, fsm.state_verify, '*', agent.verify_login)

    # Password Denied (2)
    fsm.add_rule(fsm.state_verify, fsm.state_init, 'N', agent.reset_agent)

    # Password Accepted (3 and 7)
    fsm.add_rule(
        fsm.state_verify,
        fsm.state_active,
        'Y',
        agent.fully_activate_agent)

    # Change password (4)
    fsm.add_rule(
        fsm.state_active,
        fsm.state_read1,
        '*',
        agent.init_new_password_entry)

    fsm.add_rule(
        fsm.state_read1,
        fsm.state_read1,
        '0123456789',
        agent.append_next_password_digit)

    fsm.add_rule(fsm.state_read1, fsm.state_read2, '*', agent.cache_password)

    fsm.add_rule(
        fsm.state_read2,
        fsm.state_read2,
        '0123456789',
        agent.append_next_password_digit)

    fsm.add_rule(
        fsm.state_read2,
        fsm.state_verify,
        '*',
        agent.validate_password_change)

    fsm.add_rule(
        fsm.state_verify,
        fsm.state_active,
        'Y',
        agent.fully_activate_agent)

    fsm.add_rule(
        fsm.state_verify,
        fsm.state_read1,
        'N',
        agent.init_new_password_entry)

    # Begin Logout (5 and 10)
    fsm.add_rule(fsm.state_active, fsm.state_logout, "#", agent.log_out)

    fsm.add_rule(fsm.state_logout, fsm.state_done, "#", agent.confirm_logout)

    fsm.add_rule(
        fsm.state_done,
        fsm.state_read,
        "0123456789",
        agent.init_password_entry)

    # Choose LED and lightning duration (8 and 9)
    fsm.add_rule(fsm.state_active, fsm.state_led, "012345", agent.cache_led_id)
    # fsm.add_rule(fsm.state_led, fsm.state_time, '*', agent.cache_led_id)  #
    # Confirm LED
    fsm.add_rule(
        fsm.state_led,
        fsm.state_led,
        "0123456789",
        agent.append_next_time_digit)
    fsm.add_rule(fsm.state_led, fsm.state_active, '*', agent.light_one_led)
    print("\n" * 20)
    print("Welcome to Haldis Carport AS!\n")
    print("Please press any button to start the system.")
    while True:
        fsm.run_Rules(agent)
