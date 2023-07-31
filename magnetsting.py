"""
MAGNETSTING\n
v1.0.0\n
`MAGNETSTING` is a command line framework used to set up command line interpreters. The `readline` module is also
imported in order to provide shell behaviour
"""
import readline

# TODO: For commands with prefixes: add_command_strict(command_name, command_options, command_function)


class MagnetSting:

    def __init__(self, banner_decorators: str = "-=-", decorators_length: int = 12,
                 banner_identifiers: tuple = ("MAGNETSTING", "Identifiers Here",), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] - Exiting", help_spacers: int = 4, help_indent: int = 2,
                 command_hint_spacers: int = 2, confirm_list=None, break_list=None):
        """
        Initialize instance of `MAGNETSTING`
        :param banner_decorators: The `decorators` of the banner on start-up
        :param decorators_length: The `length` of the banner decorators
        :param banner_identifiers: A `tuple` of the information that will appear in the banner. This can include but is
        not limited to: name, version number, etc.
        :param cmd_prompt: The prompt of the input
        :param exit_message: The `message` that will be printed out upon exiting
        :param help_spacers: The `alignment spacers` between the command name and the command description of the help
        banner
        :param help_indent: The `number of spaces` the help banner is indented
        :param command_hint_spacers: The `number of spaces` between command hints when a user enters a command that does
        not exist
        :param confirm_list: A `list` of keywords that are used to confirm an action
        :param break_list: A `list` of keywords that are used to exit
        """

        if break_list is None:
            break_list = [
                "quit",
                "exit",
                "q",
            ]

        if confirm_list is None:
            confirm_list = [
                "confirm",
                "yes",
                "y",
            ]

        # Initialize dict that will hold command names and their functions
        self._commands_dict = {}
        # Initialize dict that will hold command names and some help context about them
        self._commands_help = {}

        self.banner_decorators = banner_decorators
        self.decorators_length = decorators_length
        self.banner_identifiers = banner_identifiers
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.help_spacers = help_spacers
        self.help_indent = help_indent
        self.command_help_spacers = command_hint_spacers
        self.break_list = break_list
        self.confirm_list = confirm_list

    def _help_command(self):
        """
        Print out the help banner
        :return: None
        """
        print()
        print(f"{' '*self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.help_spacers}}")
        print(f"{' '*self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.help_spacers}}")
        for commands in self._commands_help:
            print(f"{' '*self.help_indent}{commands :{self.help_spacers}} {self._commands_help[commands]}")

    def add_command(self, command_name: str = None, command_help: str = None, command_function: object = None):
        """
        Add a new command to the instance of MAGNETSTING
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function object` of the command
        :return: None
        """

        # Add command name and command help to command dict
        self._commands_help[command_name] = command_help
        self._commands_dict[command_name] = command_function

    def magnetsting_mainloop(self):
        """
        `MAGNETSTING` mainloop
        :return: None
        """
        # Add "help" command to the help banner
        self._commands_help["help"] = "print this help banner"
        # Add the first break keyword in the break list to the end of the help banner
        self._commands_help[self.break_list[0]] = "exit MAGNETSTING"

        # Add "help" command to commands dict
        self._commands_dict["help"] = self._help_command
        # Add the first break keyword in break_list so that it shows up in the command hints
        self._commands_dict[self.break_list[0]] = ""

        # Print out start-up banner
        print(self.banner_decorators*self.decorators_length)
        for identifiers in self.banner_identifiers:
            print(identifiers)
        print(self.banner_decorators*self.decorators_length)

        # Print out help banner on start
        self._help_command()

        while True:
            usr_input = str(input(self.cmd_prompt)).lower()
            if usr_input in self.break_list:
                print(self.exit_message)
                break

            elif usr_input in self._commands_dict:
                self._commands_dict[usr_input]()

            # Print out all possible commands that start with what the user entered
            else:
                possible_commands = ""
                print()
                for commands in self._commands_dict:
                    if commands.startswith(usr_input):
                        possible_commands += f"{commands}{' '*self.command_help_spacers}"
                print("[*] - Possible command(s): ")
                print(possible_commands)
