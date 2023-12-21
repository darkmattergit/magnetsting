"""
**MAGNETSTING**\n
v1.0.6\n
Create command-line-based projects with ease.
"""
import subprocess
import readline

# TODO: Add readline command completion to both MagnetSting and MagnetStingAdvanced classes


class MagnetSting:
    """
    `MagnetSting` is a framework that can be used to build projects in the command line. MagnetSting allows you to
    create various commands and handles their execution, freeing you from the need of countless `if`, `elif` and `else`
    statements. The framework also handles creating an opening banner that displays everytime the project is run and
    also generates a handy command help banner, showing all the available commands and a short description of what they
    do. In case an unknown command is entered, MagnetSting helpfully suggests possible commands based on what was
    entered and checking if there are any commands that have a similar name. MagnetSting takes care of it all.
    """
    def __init__(self, banner_decorators: str = "-=-", decorators_length: int = 12,
                 banner_identifiers: tuple = ("MAGNETSTING", "Identifiers Here",), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] - Exiting", help_spacers: int = 4, help_indent: int = 2,
                 command_hint_spacers: int = 2, break_list=None):
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
        :param break_list: A `list` of keywords that are used to exit
        """

        if break_list is None:
            break_list = [
                "quit",
                "exit",
                "q",
            ]

        self.banner_decorators = banner_decorators
        self.decorators_length = decorators_length
        self.banner_identifiers = banner_identifiers
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.help_spacers = help_spacers
        self.help_indent = help_indent
        self.command_help_spacers = command_hint_spacers
        self.break_list = break_list

        # Initialize dict that will hold commands and their information
        self._commands_dict = {}

    def _help_command(self):
        """
        Print out the help banner
        :return: None
        """
        print()
        print(f"{' '*self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.help_spacers}}")
        print(f"{' '*self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.help_spacers}}")
        for commands in self._commands_dict:
            print(f"{' '*self.help_indent}{commands :{self.help_spacers}} {self._commands_dict[commands]['help']}")

    def add_command(self, command_name: str = None, command_help: str = None, command_function: object = None):
        """
        Add a new command to the instance of MAGNETSTING
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function object` of the command
        :return: None
        """

        # Add command name and command help to command dict
        self._commands_dict[command_name] = {
            "help": command_help,
            "function": command_function
        }

    def magnetsting_mainloop(self):
        """
        `MAGNETSTING` mainloop
        :return: None
        """

        # Add "help" command to the help banner
        self._commands_dict["help"] = {
            "help": "print this help banner"
        }
        # Add the first break keyword in the break list to the end of the help banner
        self._commands_dict[self.break_list[0]] = {
            "help": "exit MAGNETSTING"
        }

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


class MagnetStingAdvanced:
    """
    `MagnetStingAdvanced` is an improved framework based on `MagnetSting`. It allows for a wider range of customization
    and expands the types of commands that can be created. In this framework, the three types of commands that can be
    created are: `single`, `free` and `parser`.\n
    - `single`-type commands are the same as those in `MagnetSting`. Just type in the command name and the function
      associated with the command will be executed. Anything typed after the command name will not be passed to the
      function.
    - `free`-type commands allow for the use of arguments. For example, if the command name is `"foo"`, then you can
      call it by adding an argument (in this case "bar") to the command: `">> foo bar"`. This would then pass `"bar"`
      to the function associated with the command `"foo"`.
    - `parser`-type commands, rather than executing functions associated to command names like `single-` and `free-type`
      commands, instead executes Python files associated with the command name, specifically, Python files using the
      `argparse` module. For example, the command name `"foo"` has the file `"bar.py"` associated with it. You can then
      call the file by typing `"foo - -help"`. The `"- -help"` is then passed to the `"bar.py"` file, which takes the
      arguments and executes them, and in this case, would display the "help" output.
    **NOTE**\n
    Functions used by the `single`- and `free-type` commands **MUST** be created in a specific way inorder for
    `MagnetStingAdvanced` to execute them.\n
    - `single-type`: The functions for `single-type` commands **MUST** have the following parameter:
      `additional_data: any`. The function cannot have any other parameters. The `additional_data` parameter allows
      you to pass other data such as strings, ints, objects, etc. to the function, it can be anything else the
      function may need.
    - `free-type`: The functions for `free-type` commands **MUST** have the following parameters:
      `free_function: str` **AND** `additional_data: any`. The function cannot have any other parameters. The
      `free_function` parameter is for the argument used with the command (recall from the `free-type` example above,
      this would be "bar"), while the `additional_data` parameter allows you to pass other data such as strings, ints,
      objects, etc. to the function. It can be anything else the function may need to work the way you want it to.
    """
    def __init__(self, framework_name: str = "MAGNETSTING", banner_decorators: str = "-=-", decorator_length: int = 12,
                 banner_identifiers: tuple = ("MAGNETSTING", "Identifiers here"), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] Exiting", help_spacers: int = 4, help_indent: int = 2,
                 command_hint_spacers: int = 2, break_keywords: tuple = ("q", "quit", "exit"),
                 verbose: bool = False, type_spacer: int = 12, custom_banner: str = None):
        """
        Initialize instance of MagnetStingAdvanced
        :param framework_name: The name of the framework
        :param banner_decorators: The `decorators` of the banner on start-up
        :param decorator_length: The `length` of the banner decorators
        :param banner_identifiers: A `tuple` of the information that will appear in the banner. This can include but is
                                   not limited to: name, version number, etc.
        :param cmd_prompt: The `prompt` of the input
        :param exit_message: The `message` that will be printed out upon exiting
        :param help_spacers: The `alignment spacers` between the command name and the command description of the help
                             banner
        :param help_indent: The `number of spaces` the help banner is indented
        :param command_hint_spacers: The `number of spaces` between command hints when the user enters a command that
                                     does not exist
        :param break_keywords: A `tuple` of keywords used to exit
        :param verbose: In the help banner, show the command types of the command names. Having the parameter set to
                        `True` will show the command types while `False` will not
        :param type_spacer: The `spacing` between the command description and command type, if the verbose help banner
                            is used
        :param custom_banner: Use a custom banner rather than the one that is generated by the class
        """

        # Initialize dict that will hold command names and their information
        self._commands_info = {}

        self.framework_name = framework_name
        self.banner_decorators = banner_decorators
        self.decorator_length = decorator_length
        self.banner_identifiers = banner_identifiers
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.help_spacers = help_spacers
        self.help_indent = help_indent
        self.command_hint_spacers = command_hint_spacers
        self.break_keywords = break_keywords
        self.verbose = verbose
        self.type_spacer = type_spacer
        self.custom_banner = custom_banner

    def _help_command(self):
        """
        Print out the help banner
        :return: None
        """
        # Print commands and their help descriptions
        if self.verbose is False:
            print()
            print(f"{' '*self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.help_spacers}}")
            print(f"{' '*self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.help_spacers}}")
            for commands in self._commands_info:
                print(f"{' '*self.help_indent}{commands :{self.help_spacers}} {self._commands_info[commands]['help']}")

        # Print commands, their help descriptions and the commands types
        else:
            print()
            print(f"{' ' * self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.type_spacer}} "
                  f"{'Type'}")
            print(f"{' ' * self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.type_spacer}} "
                  f"{'----' :{self.help_spacers}}")

            for commands in self._commands_info:
                print(f"{' '*self.help_indent}{commands :{self.help_spacers}} "
                      f"{self._commands_info[commands]['help'] :{self.type_spacer}} "
                      f"{self._commands_info[commands]['type']}")

    def add_command_free(self, command_name: str = None, command_help: str = None,
                         command_function: object = None, additional_data: any = None) -> None:
        """
        Add a `free-type` command to the dictionary of commands. A free-type command differs from a `single-type`
        command by being able to take arguments after the command name. For example, if the command name is `foo`,
        then you can do: "foo bar baz", with "bar baz" being the argument(s). There are no limits on how long the
        arguments can be, they can be as long and as many as you would like. If you do not provide an argument to a
        free-type command, a message will be printed telling you that some form of an argument is required. Functions
        used in free-type commands **MUST** have the following function parameters: `free_function: str` **AND**
        `additional_data: any`.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function` assigned to the command
        :param additional_data: 'Additional data' that gets sent over to the command's function
        :return: None
        """

        self._commands_info[command_name] = {
            "type": "free",
            "function": command_function,
            "help": command_help,
            "additional": additional_data,
        }

    def add_command_single(self, command_name: str = None, command_help: str = None, command_function: object = None,
                           additional_data: any = None) -> None:
        """
        Add a `single-type` command to the dict of commands. A single-type command consists only of a command name that
        when called, executes the function assigned to it. Anything typed after the command name is not passed onto the
        function assigned to the command. Functions used in single-type commands **MUST** have the following parameter:
        `additional_data: any`.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function` assigned to the command
        :param additional_data: `Additional data` that gets sent over to the command's function
        :return: None
        """

        self._commands_info[command_name] = {
            "type": "single",
            "function": command_function,
            "help": command_help,
            "additional": additional_data,
        }

    def add_command_parser(self, command_name: str = None, command_help: str = None, command_file: str = None) -> None:
        """
        Add a 'parser-type' command to the dict of commands. A parser-type command is different from the other
        commands. Instead of running a function like the others, a parser-type command runs another python file, as
        specified in the `command_file` parameter. The python file must be an `argparse` type of script, as this type of
        command takes the arguments typed after the command name (ex. foo - -bar) and uses the `subprocess` module to
        run the assigned file with the arguments that were typed. For example, if you typed `foo - -help` with the file
        `bar.py` being assigned to the command name `foo`, then the subprocess module would run (bar.py - -help),
        which would print out the help banner. Since a file is being used here, there are ***NO*** specific parameters
        that need to be added when creating/using the file.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_file: The `full or relative path` of the file assigned to the command
        :return: None
        """

        self._commands_info[command_name] = {
            "type": "parser",
            "file": command_file,
            "help": command_help,
        }

    def magnetstingadvanced_mainloop(self):
        # Add built-in commands to commands dict
        self._commands_info["clear"] = {
            "type": "built-in",
            "help": "clear the screen",
        }

        self._commands_info["help"] = {
            "type": "built-in",
            "help": "print this help banner",
        }

        self._commands_info[self.break_keywords[0]] = {
            "type": "built-in",
            "help": f"exit {self.framework_name}",
        }

        # Print the class-generated opening banner and command help banner
        if self.custom_banner is None:
            print(self.banner_decorators*self.decorator_length)
            for identifiers in self.banner_identifiers:
                print(identifiers)
            print(self.banner_decorators*self.decorator_length)
            self._help_command()

        # Print custom banner and command help banner
        else:
            print(self.custom_banner)
            self._help_command()

        while True:
            usr_input = str(input(self.cmd_prompt))
            if usr_input in self.break_keywords:
                print(self.exit_message)
                break

            # Print out help banner
            elif usr_input == "help":
                self._help_command()

            # Clear the command line
            elif usr_input == "clear":
                subprocess.run("clear", shell=True)

            else:
                split_command = usr_input.split(" ")

                # Get the name of the command
                get_name = split_command[0]

                if get_name in self._commands_info:
                    # === Free Commands ===
                    if self._commands_info[get_name]["type"] == "free":
                        if len(split_command) == 1 or split_command[1].isspace() or split_command[1] == "":
                            print("[!] Argument required")

                        else:
                            get_arg = usr_input[len(get_name)+1:]
                            self._commands_info[get_name]["function"](free_function=get_arg,
                                                                      additional_data=self._commands_info[get_name]
                                                                      ["additional"])

                    # === Single Commands ===
                    elif self._commands_info[get_name]["type"] == "single":
                        self._commands_info[get_name]["function"](additional_data=self._commands_info[get_name]
                                                                  ["additional"])

                    # === Parser Commands ===
                    elif self._commands_info[get_name]["type"] == "parser":
                        parser_args = usr_input[len(get_name)+1:]
                        subprocess.run(f"python3 {self._commands_info[get_name]['file']} {parser_args}", shell=True)

                else:
                    # Initialize string that will hold command suggestions based on the user input
                    possible_commands = ""

                    # Loop through command dict and find any commands that start with the user input
                    for commands in self._commands_info:
                        if commands.startswith(get_name):
                            possible_commands += f"{commands}  "
                        else:
                            pass

                    # Print out string of possible commands
                    print("Possible command(s): ")
                    print(possible_commands)
