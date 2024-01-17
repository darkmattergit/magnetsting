"""
**MAGNETSTING**\n
v1.0.7\n
Create command-line projects with ease.
"""
import subprocess
import readline


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
                 banner_data: tuple = ("MAGNETSTING", "Data Here",), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] Exiting", help_spacers: int = 4, help_indent: int = 2,
                 command_hint_spacers: int = 2, break_keywords: tuple = ("q", "quit", "exit")):
        """
        Initialize instance of `MAGNETSTING`
        :param banner_decorators: The `decorators` of the banner on start-up
        :param decorators_length: The `length` of the banner decorators
        :param banner_data: A `tuple` of the information that will appear in the banner. This can include but is
        not limited to: name, version number, etc.
        :param cmd_prompt: The prompt of the input
        :param exit_message: The `message` that will be printed out upon exiting
        :param help_spacers: The `alignment spacers` between the command name and the command description of the help
        banner
        :param help_indent: The `number of spaces` the help banner is indented
        :param command_hint_spacers: The `number of spaces` between command hints when a user enters a command that does
        not exist
        :param break_keywords: A `tuple` of keywords that are used to exit
        """

        self.banner_decorators = banner_decorators
        self.decorators_length = decorators_length
        self.banner_data = banner_data
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.help_spacers = help_spacers
        self.help_indent = help_indent
        self.command_help_spacers = command_hint_spacers
        self.break_keywords = break_keywords

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

    def _possible_commands(self, command_name: str = None) -> None:
        """
        Pretty print possible command names that start with the user input should the input not be in the commands_info
        dict. The output is displayed in columns, similar to how it would look if using the 'column' tool on UNIX/Linux
        systems.
        :param command_name: The input from the user
        :return: None
        """

        # Initialize list that will hold the commands that start with the user input
        possible_commands_list = [commands for commands in self._commands_dict if commands.startswith(command_name)]

        # Get the length of the longest command name
        longest_command = 0
        for commands in possible_commands_list:
            if len(commands) > longest_command:
                longest_command = len(commands)
            else:
                pass

        # Add extra spacing to the length of the longest command to be able to better see the commands
        block_spacers = longest_command + 12

        # Add blank padding if the number of commands in the list is not a multiple of 4
        if len(possible_commands_list) % 4 != 0:
            for _ in range(4 - (len(possible_commands_list) % 4)):
                possible_commands_list.append("")
        else:
            pass

        # Create a list that holds lists of 4 commands each
        start_counter = 0
        end_counter = 4
        command_blocks = []
        for _ in range(len(possible_commands_list) // 4):
            command_blocks.append(possible_commands_list[start_counter:end_counter])
            start_counter += 4
            end_counter += 4

        # Pretty print possible commands in 4 columns
        print("possible command(s):")
        for blocks in command_blocks:
            print(f"{blocks[0] :{block_spacers}}{blocks[1] :{block_spacers}}{blocks[2] :{block_spacers}}"
                  f"{blocks[3] :{block_spacers}}")

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
        self._commands_dict[self.break_keywords[0]] = {
            "help": "exit MAGNETSTING"
        }

        # Print out start-up banner
        print(self.banner_decorators*self.decorators_length)
        for data in self.banner_data:
            print(data)
        print(self.banner_decorators*self.decorators_length)

        # Print out help banner on start
        self._help_command()

        while True:
            usr_input = str(input(self.cmd_prompt)).lower()
            if usr_input in self.break_keywords:
                print(self.exit_message)
                break

            elif usr_input in self._commands_dict:
                self._commands_dict[usr_input]()

            # Print out all possible commands that start with what the user entered
            else:
                self._possible_commands(command_name=usr_input)


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
    def __init__(self, framework_name: str = "MAGNETSTING",
                 banner: tuple | str = ("=" * 35, "MAGNETSTING", "Data here", "=" * 35), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] Exiting", help_indent: int = 2, break_keywords: tuple = ("q", "quit", "exit"),
                 verbose: bool = False):
        """
        Initialize instance of MagnetStingAdvanced
        :param framework_name: The name of the framework.
        :param banner: A `tuple` of the information that will appear in the banner. This can include but is
                       not limited to: name, version number, etc. If you want to use a custom banner rather than the
                       one that the class creates using the tuple, use a string instead.
        :param cmd_prompt: The `prompt` of the input.
        :param exit_message: The `message` that will be printed out upon exiting.
        :param help_indent: The `number of spaces` the help banner is indented.
        :param break_keywords: A `tuple` of keywords used to exit.
        :param verbose: In the help banner, show command types next to the command descriptions. Having the parameter
                        set to `True` will show the command types while `False` will not.
        """

        # Initialize dict that will hold command names and their information
        self._commands_info = {}
        self.framework_name = framework_name
        self.banner_data = banner
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.help_indent = help_indent
        self.break_keywords = break_keywords
        self.verbose = verbose

    def _help_command(self):
        """
        Print out the help banner
        :return: None
        """
        # Calculate the amount of spacing needed between the commands and their help descriptions
        spacing = 0
        for commands in self._commands_info:
            if len(commands) > spacing:
                spacing = len(commands)
            else:
                pass

        # Add additional spacing to the len of the longest command name to make the columns more distinct and readable
        spacing = spacing + 5

        # Print commands and their help descriptions
        if self.verbose is False:
            print()
            print(f"{' '*self.help_indent}{'Command':{spacing}} {'Description' :{spacing}}")
            print(f"{' '*self.help_indent}{'-------':{spacing}} {'-----------' :{spacing}}")
            for commands in self._commands_info:
                print(f"{' '*self.help_indent}{commands :{spacing}} {self._commands_info[commands]['help']}")

        # Print commands, their help descriptions and the commands types
        else:
            # Calculate the amount of spacing needed between the command help descriptions and the types
            type_spacing = 0
            for command_types in self._commands_info:
                if len(self._commands_info[command_types]["help"]) > type_spacing:
                    type_spacing = len(self._commands_info[command_types]["help"])
                else:
                    pass

            # Add additional spacing to the len of the longest command description to make the columns more distinct
            # and readable
            type_spacing = type_spacing + 5

            print()
            print(f"{' ' * self.help_indent}{'Command' :{spacing}} {'Description' :{type_spacing}} "
                  f"{'Type'}")
            print(f"{' ' * self.help_indent}{'-------':{spacing}} {'-----------' :{type_spacing}} "
                  f"{'----' :{spacing}}")

            for commands in self._commands_info:
                print(f"{' '*self.help_indent}{commands :{spacing}} "
                      f"{self._commands_info[commands]['help'] :{type_spacing}} "
                      f"{self._commands_info[commands]['type']}")

    def _specific_commands_help(self, command_name: str = None) -> None:
        # Initialize dict to hold command names and their descriptions
        command_help_dict = {}
        # Initialize ints for calculating spacing
        command_spacer = 0
        type_spacer = 0

        for commands in self._commands_info:
            if commands.startswith(command_name):
                command_help_dict[commands] = self._commands_info[commands]["help"]

                # Calculate base spacing between commands names and descriptions
                if len(commands) > command_spacer:
                    command_spacer = len(commands)

                else:
                    pass

                # Calculate base spacing between command descriptions and types
                if len(self._commands_info[commands]['help']) > type_spacer:
                    type_spacer = len(self._commands_info[commands]['help'])

                else:
                    pass

            else:
                pass

        # Add additional spacing
        command_spacer = command_spacer + 5
        type_spacer = type_spacer + 5

        if len(command_help_dict) == 0:
            print("[!] No command(s) found")

        else:
            if self.verbose is False:
                print()
                print(f"{' '*self.help_indent}{'Command':{command_spacer}} Description")
                print(f"{' '*self.help_indent}{'-------':{command_spacer}} -----------")
                for command_help in command_help_dict:
                    print(f"{' '*self.help_indent}{command_help:{command_spacer}} "
                          f"{self._commands_info[command_help]['help']}")

            else:
                print()
                print(f"{' ' * self.help_indent}{'Command' :{command_spacer}} {'Description' :{type_spacer}} "
                      f"{'Type'}")
                print(f"{' ' * self.help_indent}{'-------':{command_spacer}} {'-----------' :{type_spacer}} "
                      f"{'----' :{command_spacer}}")

                for commands in command_help_dict:
                    print(f"{' ' * self.help_indent}{commands :{command_spacer}} "
                          f"{self._commands_info[commands]['help'] :{type_spacer}} "
                          f"{self._commands_info[commands]['type']}")

    def _possible_commands(self, command_name: str = None) -> None:
        """
        Pretty print possible command names that start with the user input should the input not be in the commands_info
        dict. The output is displayed in columns, similar to how it would look if using the 'column' tool on UNIX/Linux
        systems.
        :param command_name: The input from the user
        :return: None
        """

        # Initialize list that will hold the commands that start with the user input
        possible_commands_list = [commands for commands in self._commands_info if commands.startswith(command_name)]

        # Get the length of the longest command name
        longest_command = 0
        for commands in possible_commands_list:
            if len(commands) > longest_command:
                longest_command = len(commands)
            else:
                pass

        # Add extra spacing to the length of the longest command to be able to better see the commands
        block_spacers = longest_command + 12

        # Add blank padding if the number of commands in the list is not a multiple of 4
        if len(possible_commands_list) % 4 != 0:
            for _ in range(4 - (len(possible_commands_list) % 4)):
                possible_commands_list.append("")
        else:
            pass

        # Create a list that holds lists of 4 commands each
        start_counter = 0
        end_counter = 4
        command_blocks = []
        for _ in range(len(possible_commands_list) // 4):
            command_blocks.append(possible_commands_list[start_counter:end_counter])
            start_counter += 4
            end_counter += 4

        # Pretty print possible commands in rows of 4
        print("possible command(s):")
        for blocks in command_blocks:
            print(f"{blocks[0] :{block_spacers}}{blocks[1] :{block_spacers}}{blocks[2] :{block_spacers}}"
                  f"{blocks[3] :{block_spacers}}")

    def add_command_free(self, command_name: str = None, command_help: str = None,
                         command_function: object = None, additional_data: tuple = None) -> None:
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
                           additional_data: tuple = None) -> None:
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

        # Print custom banner
        if type(self.banner_data) is str:
            print(self.banner_data)
            self._help_command()

        # Print values from tuple
        else:
            for data in self.banner_data:
                print(data)
            self._help_command()

        while True:
            usr_input = str(input(self.cmd_prompt))
            split_command = usr_input.split(" ")

            if split_command[0] in self.break_keywords:
                print(self.exit_message)
                break

            # Print help banner
            elif split_command[0] == "help":
                self._help_command()

            # Print help banner containing specific commands
            elif len(split_command) > 1 and split_command[0] == "help":
                self._specific_commands_help(command_name=split_command[1])

            # Clear the command line
            elif split_command[0] == "clear":
                subprocess.run("clear", shell=True)

            else:
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
                    if usr_input == "" or usr_input.isspace():
                        pass
                    else:
                        self._possible_commands(command_name=get_name)
