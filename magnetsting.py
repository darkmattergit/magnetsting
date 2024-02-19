"""
**MAGNETSTING**\n
v1.0.7\n
Create command-line projects with ease.
"""
import subprocess
import readline
import json
import os


class MagnetSting:
    """
    `MagnetSting` is a framework that simplifies the creation of command-line projects. `MagnetSting` comes with many
    capabilities built into it, such as help banner creation, command suggestions, command aliasing and more.
    The framework allows you to create three types of commands: `single`, `free` and `parser`.\n
    - `single`-type commands are commands that consist only of the command name. Anything typed after the command name
      will not be passed onto the function assigned to the command.
    - `free`-type commands allow for the use of arguments. For example, if the command name is `"foo"`, then you can
      call it by adding an argument (in this case "bar") to the command: `">> foo bar"`. This would then pass `"bar"`
      to the function associated with the command `"foo"`.
    - `parser`-type commands, rather than executing functions associated to command names like `single-` and `free-type`
      commands, instead executes Python files associated with the command name, specifically, Python files using the
      `argparse` module. For example, the command name `"foo"` has the file `"bar.py"` associated with it. You can then
      call the file by typing `"foo - -help"`. The `"- -help"` is then passed to the `"bar.py"` file, which takes the
      arguments and executes them, and in this case, would display the "help" output.
    - Additionally, commands can be grouped together using `command groups`. Command groups are, as the name suggests,
      a way to organize commands into a specific group. Commands assigned to a command group do not show up in the
      help banner, rather, the command group name does instead. To view all commands within a group, call the command
      group's name. The syntax to call a command within a command group is `<command group name> <command name>
      <args (if free- or parser-type command)>`.
    **NOTE**\n
    Functions used by the `single`- and `free-type` commands **MUST** be created in a specific way inorder for
    `MagnetSting` to execute them.\n
    - `single-type`: The functions for `single-type` commands **MUST** have the following parameter:
      `additional_data: any`. The function cannot have any other parameters. The `additional_data` parameter allows
      you to pass other data such as strings, ints, objects, etc. to the function through a tuple.
    - `free-type`: The functions for `free-type` commands **MUST** have the following parameters:
      `free_function: str` **AND** `additional_data: any`. The function cannot have any other parameters. The
      `free_function` parameter is for the argument used with the command (recall from the `free-type` example above,
      this would be "bar"), while the `additional_data` parameter allows you to pass other data such as strings, ints,
      objects, etc. to the function using a tuple.
    **NOTE**\n
    The order in which the commands and command groups are created determines the order in which they appear in the help
    banner. The same applies for commands in command groups.
    """
    def __init__(self, exit_description: str = "exit MAGNETSTING",
                 banner: tuple | str = ("=" * 35, "MAGNETSTING", "Data here", "=" * 35), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] Exiting", break_keywords: tuple = ("q", "quit", "exit"),
                 alias_file: str = ".alias.json", verbose: bool = False):
        """
        Initialize instance of MagnetSting
        :param exit_description: The description of the exit command
        :param banner: A `tuple` of the information that will appear in the banner. This can include but is
                       not limited to: name, version number, etc. If you want to use a custom banner rather than the
                       one that the class creates using the tuple, use a `string` instead.
        :param cmd_prompt: The `prompt` of the input.
        :param exit_message: The `message` that will be printed out upon exiting.
        :param break_keywords: A `tuple` of keywords used to exit.
        :param alias_file: A JSON file that holds `command aliases`
        :param verbose: In the help banner, show command types next to the command descriptions. Having the parameter
                        set to `True` will show the command types while `False` will not.
        """

        # Initialize dicts for commands, command groups and command aliases
        self._commands_info = {}
        self._groups_dict = {}
        self._alias_dict = {}
        self.exit_description = exit_description
        self.banner_data = banner
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.break_keywords = break_keywords
        self.alias_file = alias_file
        self.verbose = verbose

        # Check if file is a JSON file
        if os.path.splitext(self.alias_file)[len(os.path.splitext(self.alias_file))-1] != ".json":
            raise ValueError("File is not a JSON file")
        else:
            pass

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
            print(f"{' '*2}{'Command':{spacing}} {'Description' :{spacing}}")
            print(f"{' '*2}{'-------':{spacing}} {'-----------' :{spacing}}")
            for commands in self._commands_info:
                print(f"{' '*2}{commands :{spacing}} {self._commands_info[commands]['help']}")

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
            print(f"{' '*2}{'Command' :{spacing}} {'Description' :{type_spacing}} "
                  f"{'Type'}")
            print(f"{' '*2}{'-------':{spacing}} {'-----------' :{type_spacing}} "
                  f"{'----' :{spacing}}")

            for commands in self._commands_info:
                print(f"{' '*2}{commands :{spacing}} "
                      f"{self._commands_info[commands]['help'] :{type_spacing}} "
                      f"{self._commands_info[commands]['type']}")

    def _specific_commands_help(self, command_name: str = None) -> None:
        """
        Print a help banner containing specific commands
        :param command_name: The name or partial name of the command(s) to look for
        :return: None
        """
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
        if command_spacer < 5:
            command_spacer = command_spacer + 12
        else:
            command_spacer = command_spacer + 5

        type_spacer = type_spacer + 5

        if len(command_help_dict) == 0:
            print("[!] No command(s) found")

        else:
            if self.verbose is False:
                print()
                print(f"{' '*2}{'Command':{command_spacer}} Description")
                print(f"{' '*2}{'-------':{command_spacer}} -----------")
                for command_help in command_help_dict:
                    print(f"{' '*2}{command_help:{command_spacer}} "
                          f"{self._commands_info[command_help]['help']}")

            else:
                print()
                print(f"{' '*2}{'Command' :{command_spacer}} {'Description' :{type_spacer}} "
                      f"{'Type'}")
                print(f"{' '*2}{'-------':{command_spacer}} {'-----------' :{type_spacer}} "
                      f"{'----' :{command_spacer}}")

                for commands in command_help_dict:
                    print(f"{' '*2}{commands :{command_spacer}} "
                          f"{self._commands_info[commands]['help'] :{type_spacer}} "
                          f"{self._commands_info[commands]['type']}")

    def _help_command_group(self, group_name: str = None) -> None:
        """
        Print a help banner for a specific command group
        :param group_name: The name of the group
        :return: None
        """
        # Calculate the amount of spacing needed between the commands and their help descriptions
        spacing = 0
        for commands in self._groups_dict[group_name]:
            if len(commands) > spacing:
                spacing = len(commands)
            else:
                pass

        # Add additional spacing to the len of the longest command name to make the columns more distinct and readable
        spacing = spacing + 5

        # Print commands and their help descriptions
        if self.verbose is False:
            print()
            print(f"{' '*2}{'Command':{spacing}} {'Description' :{spacing}}")
            print(f"{' '*2}{'-------':{spacing}} {'-----------' :{spacing}}")
            for commands in self._groups_dict[group_name]:
                print(f"{' '*2}{commands :{spacing}} {self._groups_dict[group_name][commands]['help']}")

        # Print commands, their help descriptions and the commands types
        else:
            # Calculate the amount of spacing needed between the command help descriptions and the types
            type_spacing = 0
            for command_types in self._groups_dict[group_name]:
                if len(self._groups_dict[group_name][command_types]["help"]) > type_spacing:
                    type_spacing = len(self._groups_dict[group_name][command_types]["help"])
                else:
                    pass

            # Add additional spacing to the len of the longest command description to make the columns more distinct
            # and readable
            type_spacing = type_spacing + 5

            print()
            print(f"{' '*2}{'Command' :{spacing}} {'Description' :{type_spacing}} "
                  f"{'Type'}")
            print(f"{' '*2}{'-------':{spacing}} {'-----------' :{type_spacing}} "
                  f"{'----' :{spacing}}")

            for commands in self._groups_dict[group_name]:
                print(f"{' '*2}{commands :{spacing}} "
                      f"{self._groups_dict[group_name][commands]['help'] :{type_spacing}} "
                      f"{self._groups_dict[group_name][commands]['type']}")

    def _possible_commands(self, command_name: str = None, command_group: str = None) -> None:
        """
        Pretty print possible command names that start with the user input should the input not be in the commands_info
        dict. The output is displayed in columns, similar to how it would look if using the 'column' tool on UNIX/Linux
        systems.
        :param command_name: The input from the user
        :param command_group: The name of the command group if checking commands in a group. If left as None, it will
                              look through the "self._commands_info" dict instead.
        :return: None
        """

        # Initialize list that will hold the commands that start with the user input
        if command_group is None:
            possible_commands_list = [commands for commands in self._commands_info if commands.startswith(command_name)]
        else:
            possible_commands_list = [commands for commands in self._groups_dict[command_group] if
                                      commands.startswith(command_name)]

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

    def _alias_command(self, alias_list: list = None) -> None:
        """
        Method to create and edit, remove and view command aliases
        :param alias_list: The contents of the JSON file that have been decoded into a Python dict
        :return: None
        """
        if len(alias_list) < 2:
            print("[*] Use 'alias add <alias name> <command>' to add/edit aliases or 'alias remove <alias name>' to "
                  "remove aliases")
            spacer = 0
            for aliases in self._alias_dict:
                if len(aliases) > spacer:
                    spacer = len(aliases)

                else:
                    pass

            # Add different amount of additional spacing depending on the value of "spacer" to avoid misaligned columns
            if spacer <= 5:
                spacer = spacer + 12
            else:
                spacer = spacer + 5

            print()
            print(f"  {'Alias':{spacer}} Full Command")
            print(f"  {'-----':{spacer}} ------------")
            for commands in self._alias_dict:
                print(f"  {commands:{spacer}} {self._alias_dict[commands]}")

        else:
            # Add a command alias
            if alias_list[1] == "add" and len(alias_list) >= 4:

                if alias_list[2] in self._commands_info:
                    print(f"[!] Cannot create alias, '{alias_list[2]}' is already in use as a command name")

                elif alias_list[3] not in self._commands_info:
                    print(f"[!] Cannot create alias, the command '{alias_list[3]}' does not exist")

                else:
                    command_str = " ".join(alias_list[3:])
                    self._alias_dict[alias_list[2]] = command_str
                    print(f"[+] Added alias '{alias_list[2]}'")

            # Remove a command alias
            elif alias_list[1] == "remove" and len(alias_list) == 3:
                try:
                    del(self._alias_dict[alias_list[2]])

                except KeyError:
                    print(f"[*] Alias '{alias_list[2]}' does not exist")

                else:
                    print(f"[-] Removed alias '{alias_list[2]}'")

            else:
                print("[!] Invalid alias command")

    def add_command_free(self, command_name: str = None, command_help: str = None, command_group: str = None,
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
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any group
        :param command_function: The `function` assigned to the command
        :param additional_data: 'Additional data' that gets sent over to the command's function
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name] = {
                "type": "free",
                "function": command_function,
                "help": command_help,
                "additional": additional_data,
            }

        else:
            if command_group in self._groups_dict:
                self._groups_dict[command_group][command_name] = {
                    "type": "free",
                    "function": command_function,
                    "help": command_help,
                    "additional": additional_data,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_single(self, command_name: str = None, command_help: str = None, command_group: str = None,
                           command_function: object = None, additional_data: tuple = None) -> None:
        """
        Add a `single-type` command to the dict of commands. A single-type command consists only of a command name that
        when called, executes the function assigned to it. Anything typed after the command name is not passed to the
        function assigned to the command. Functions used in single-type commands **MUST** have the following parameter:
        `additional_data: any`.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any group
        :param command_function: The `function` assigned to the command
        :param additional_data: `Additional data` that gets sent over to the command's function
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name] = {
                "type": "single",
                "function": command_function,
                "help": command_help,
                "additional": additional_data,
            }

        else:
            if command_group in self._groups_dict:
                self._groups_dict[command_group][command_name] = {
                    "type": "single",
                    "function": command_function,
                    "help": command_help,
                    "additional": additional_data,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_parser(self, command_name: str = None, command_help: str = None, command_group: str = None,
                           command_file: str = None) -> None:
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
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any group
        :param command_file: The `full or relative path` of the file assigned to the command
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name] = {
                "type": "parser",
                "file": command_file,
                "help": command_help,
            }

        else:
            if command_group in self._groups_dict:
                self._groups_dict[command_group][command_name] = {
                    "type": "parser",
                    "file": command_file,
                    "help": command_help,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_group(self, group_name: str = None, group_help: str = None) -> None:
        """
        Create a command group. A command group is, as the name suggests, a group of commands. Groups can be used to
        organize commands and to keep the main help banner from becoming too long and overwhelming. Any command can be
        assigned to a command group and commands within a group can also be aliased. Commands assigned to a group do not
        show up in the main help banner, rather, only the command group is shown. To see all commands assigned to a
        group, enter the group name and a  help banner containing only the commands in the group will be shown. The
        syntax to call a command in a command group is: <command group name> <command name>
        <args (if free or parser type)>.
        :param group_name: The `name` of the group
        :param group_help: A short `description` of the group
        :return: None
        """
        # Add group to groups dict
        self._groups_dict[group_name] = {}
        # Add group info to commands dict
        self._commands_info[group_name] = {
            "type": "group",
            "help": group_help,
        }

    def magnetsting_mainloop(self) -> None:
        """
        This method handles all `MagnetSting` operations. Call this method once all the commands and command
        groups have been created.
        :return: None
        """
        # Add built-in commands to commands dict
        self._commands_info["alias"] = {
            "type": "built-in",
            "help": "add, remove and view aliases",
        }

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
            "help": self.exit_description,
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

        try:
            # Open json file and load aliases into dict
            with open(self.alias_file, "r") as jr:
                json_alias = json.load(jr)
                self._alias_dict = json_alias

        except FileNotFoundError:
            pass

        while True:
            usr_input = str(input(self.cmd_prompt)).strip()
            split_command = usr_input.split(" ")

            if split_command[0] in self.break_keywords:
                # Write aliases to json file
                with open(self.alias_file, "w") as jw:
                    json.dump(self._alias_dict, jw)

                print(self.exit_message)
                break

            # Print help banner containing specific commands
            elif len(split_command) > 1 and split_command[0] == "help":
                self._specific_commands_help(command_name=split_command[1])

            # Print help banner
            elif split_command[0] == "help":
                self._help_command()

            # Clear the command line
            elif split_command[0] == "clear":
                subprocess.run("clear", shell=True)

            # Add command aliases
            elif split_command[0] == "alias":
                self._alias_command(alias_list=split_command)

            elif len(split_command) == 1 and split_command[0] in self._groups_dict:
                self._help_command_group(group_name=split_command[0])

            else:
                # Get the name of the command
                check_name = split_command[0]

                if check_name in self._commands_info or check_name in self._alias_dict or check_name in \
                        self._groups_dict:
                    # Initialize list to hold full command after determining if it is an alias or an actual command name
                    full_command_list = None
                    # Initialize dict to hold specific command info
                    command_dict = {}

                    # Check if command is a command name or a group name
                    if check_name in self._commands_info and self._commands_info[check_name]["type"] != "group":
                        full_command_list = split_command
                        command_dict[check_name] = self._commands_info[check_name]

                    elif check_name in self._commands_info and self._commands_info[check_name]["type"] == "group":
                        try:
                            full_command_list = split_command[1:]
                            command_dict[split_command[1]] = self._groups_dict[check_name][split_command[1]]

                        except KeyError:
                            self._possible_commands(command_name=split_command[1], command_group=check_name)
                            continue

                    # Check if command is an alias
                    elif check_name in self._alias_dict:
                        alias_list = f"{self._alias_dict[check_name]} {' '.join(split_command[1:])}".split()

                        # Check if name is a group name
                        if self._commands_info[alias_list[0]]["type"] == "group":
                            command_dict[alias_list[1]] = self._groups_dict[alias_list[0]][alias_list[1]]
                            full_command_list = alias_list[1:]

                        else:
                            full_command_list = f"{self._alias_dict[check_name]} {' '.join(split_command[1:])}".split()
                            command_dict[alias_list[0]] = self._commands_info[alias_list[0]]

                    # === Free Commands ===
                    if command_dict[full_command_list[0]]["type"] == "free":
                        if len(full_command_list) == 1 or full_command_list[1].isspace() or full_command_list[1] == "":
                            print("[!] Argument required")

                        else:
                            get_arg = full_command_list[1:]
                            command_dict[full_command_list[0]]["function"](free_function=get_arg,
                                                                           additional_data=command_dict
                                                                           [full_command_list[0]]["additional"])

                    # === Single Commands ===
                    elif self._commands_info[full_command_list[0]]["type"] == "single":
                        self._commands_info[full_command_list[0]]["function"](additional_data=self._commands_info
                                                                              [full_command_list[0]]["additional"])

                    # === Parser Commands ===
                    elif self._commands_info[full_command_list[0]]["type"] == "parser":
                        parser_args = " ".join(full_command_list[1:])
                        subprocess.run(f"python3 {command_dict[full_command_list[0]]['file']} {parser_args}",
                                       shell=True)

                else:
                    if usr_input == "" or usr_input.isspace():
                        pass
                    else:
                        self._possible_commands(command_name=check_name)
