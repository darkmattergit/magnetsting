"""
MAGNETSTING\n
v1.0.5\n
`MAGNETSTING` is a command line framework used to set up command line interpreters. The `readline` module is also
imported in order to provide shell behaviour.\n
The class `MagnetSting` is a simple command line builder, allowing the
user to construct a command line tool/program, with a start-up banner, a help banner, and adding command names that
run functions. It also provides command hints, incase the user does not know/mistypes the command.\n
The class `MagnetStingAdvanced` offers a wider range of capabilities compared to the `MagnetSting` class.
The `MagnetStingAdvanced` class gives the user to set three types commands:\n
- strict: strict commands have a command prefix and a tuple of accepted arguments. The command syntax for a strict-type
  command would be "`command name <argument>`" where the argument is one that is specified in the preset tuple. Any
  arguments outside the tuple will result in an error message informing the user that the argument does not exist in the
  tuple.\n
  A special `help` command exists for strict commands. The user can type "`help <command name>`" and it will list `all
  the available options` for that strict-type command.
- free: free commands also use a command prefix, however, it can take any argument. The command syntax for a `free-type`
  command would be "`command name <any argument>`".
- single: single commands are a single command name, these operate exactly like the commands in the MagnetSting class.
  The command syntax for a `single-type` command would be "`command name`"
- parser: parser commands use a command prefix like `strict-type` and `free-type` commands, however, rather than run
  a function, it runs a python file with `argparse` with the arguments you give it. The command syntax for a parser-type
  command would be "`command name <arguments>`"

When assigning functions to specific commands, two certain parameters must be given to the function you wish to execute
based on the type of command it is attached to:\n
- `strict-type commands`: any function attached to a strict-type command ***MUST*** have a parameter called
  `strict_function` ***AND*** `additional_data`. The `strict_function` parameter is for the command argument while the
  `additional_data` parameter is to send any additional data to the command's function. The `additional_data` parameter
  can be set as `None` if nothing extra is needed.
- `free-type commands`: any function attached to a free-type command ***MUST*** have a parameter called `free_function`
  ***AND*** `additional_data`. The `free_function` parameter is for the command argument while the `additional_data`
  parameter is to send any additional data to the command's function. The `additional_data` parameter can be set as
  `None` if nothing extra is needed.
- `single-type commands`: single-type commands ***MUST*** only have the `additional_data` parameter,
  as they only operate based on commands names. The `additional_data` parameter can be set as `None` if nothing extra is
  needed.
"""
import subprocess
import readline

# TODO: Add readline command completion to both MagnetSting and MagnetStingAdvanced classes


class MagnetSting:

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


class MagnetStingAdvanced:
    def __init__(self, framework_name: str = "MAGNETSTING", banner_decorators: str = "-=-", decorator_length: int = 12,
                 banner_identifiers: tuple = ("MAGNETSTING", "Identifiers here"), cmd_prompt: str = "\n>> ",
                 exit_message: str = "[*] - Exiting", help_spacers: int = 4, help_indent: int = 2,
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

        # Command types:
        #     - strict: command prefix with an arg specified in a list (ex. "use arg1" works only if arg1 is
        #               in the tuple of accepted args)
        #     - free: command prefix with any arg allowed
        #     - single: just a regular command

        # strict, free or single
        self._command_type = {}
        # strict command options
        self._command_options = {}
        # command names and their functions
        self._commands_dict = {}
        # command help context
        self._commands_help = {}
        # Every possible command for use by readline completion ***IN DEVELOPMENT***
        self._full_commands = []
        # Additional data to be sent over to the command function, can be anything (str, int, float, object, etc.)
        self._additional_data = {}

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
        if self.verbose is False:
            print()
            print(f"{' '*self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.help_spacers}}")
            print(f"{' '*self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.help_spacers}}")
            for commands in self._commands_help:
                print(f"{' '*self.help_indent}{commands :{self.help_spacers}} {self._commands_help[commands]}")
        else:
            print()
            print(f"{' ' * self.help_indent}{'Command' :{self.help_spacers}} {'Description' :{self.type_spacer}} "
                  f"{'Type'}")
            print(f"{' ' * self.help_indent}{'-------':{self.help_spacers}} {'-----------' :{self.type_spacer}} "
                  f"{'----' :{self.help_spacers}}")

            for commands, types in zip(self._commands_help, self._command_type):
                print(f"{' '*self.help_indent}{commands :{self.help_spacers}} "
                      f"{self._commands_help[commands] :{self.type_spacer}} {self._command_type[types]}")

    def add_command_strict(self, command_name: str = None, command_help: str = None,
                           command_options: tuple | list = None, command_function: object = None,
                           additional_data: any = None) -> None:
        """
        Add a `strict-type` command to the dict of commands. A strict-type command operates with a command prefix and
        an argument. A strict command has preset arguments that it can take. If an argument is not within the tuple,
        it will not run the command. All functions attached to a strict-type command ***MUST*** have a parameter called
        `strict_command`, which is a command argument that is passed to the assigned function.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_options: A `tuple` of preset command arguments/options
        :param command_function: The `function` assigned to the command
        :param additional_data: `Additional data` that gets sent over to the command's function
        :return: None
        """
        self._command_type[command_name] = "strict"
        self._commands_dict[command_name] = command_function
        self._commands_help[command_name] = command_help
        self._command_options[command_name] = command_options
        self._additional_data[command_name] = additional_data

    def add_command_free(self, command_name: str = None, command_help: str = None,
                         command_function: object = None, additional_data: any = None) -> None:
        """
        Add a `free-type` command to the dict of commands. A free-type command is similar to a strict-type command. It
        has a command prefix and takes an argument. However, where it differs from a strict-type command is that the
        argument can be anything, whereas with a strict-type command, it will only accept a predefined set of arguments.
        Additionally, all functions attached to a free-type command ***MUST*** have a parameter called `free_function`,
        which is a command argument that is passed to the assigned function.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function` assigned to the command
        :param additional_data: 'Additional data' that gets sent over to the command's function
        :return: None
        """
        self._command_type[command_name] = "free"
        self._commands_dict[command_name] = command_function
        self._commands_help[command_name] = command_help
        self._additional_data[command_name] = additional_data

    def add_command_single(self, command_name: str = None, command_help: str = None, command_function: object = None,
                           additional_data: any = None):
        """
        Add a `single-type` command to the dict of commands. A single-type command is just a command name. Whereas the
        strict-type and free-type commands take a command prefix and argument, a single-command is just that, a
        single-command name with no extra stuff, unless the `additional_data` parameter is used, of course.
        :param command_name: The `name` of the command
        :param command_help: A short `descriptor` about what the command does
        :param command_function: The `function` assigned to the command
        :param additional_data: `Additional data` that gets sent over to the command's function
        :return: None
        """
        self._command_type[command_name] = "single"
        self._commands_dict[command_name] = command_function
        self._commands_help[command_name] = command_help
        self._additional_data[command_name] = additional_data

    def add_command_parser(self, command_name: str = None, command_help: str = None, command_file: str = None):
        """
        Add a 'parser-type' command to the dict of commands. A parser-type command is different from all the other
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
        self._command_type[command_name] = "parser"
        self._commands_dict[command_name] = command_file
        self._commands_help[command_name] = command_help

    def magnetstingadvanced_mainloop(self):
        # Add the "help" and "quit" commands to the help banner and command type dict
        self._commands_help["help"] = "print this help banner"
        self._commands_help[f"{self.break_keywords[0]}"] = f"exit {self.framework_name}"
        self._command_type["help"] = "built-in"
        self._command_type[f"{self.break_keywords[0]}"] = "built-in"

        # Add the "help" command to the commands dict
        self._commands_dict["help"] = self._help_command
        self._commands_dict[f"{self.break_keywords[0]}"] = ""

        # Add "clear" command
        self._commands_help["clear"] = "clear the command line"
        self._command_type["clear"] = "built-in"

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

            elif usr_input == "clear":
                subprocess.run("clear", shell=True)

            else:
                # Split command to parse and check for command type and args
                check_command = usr_input.split(" ")
                # Check the type of command (strict, free, single)
                if check_command[0] in self._command_type:
                    command_type = self._command_type[check_command[0]]

                    # -=-=-=- strict-type command -=-=-=-
                    if command_type == "strict":
                        # Try to check if the command argument is in the command's specified tuple
                        try:
                            # Run function with command argument
                            if check_command[1] in self._command_options[check_command[0]]:
                                self._commands_dict[check_command[0]](strict_function=check_command[1])
                            # Print out possible options of command based on user input
                            else:
                                possible_strict_options = ""
                                for options in self._command_options[check_command[0]]:
                                    if options.startswith(check_command[1]):
                                        possible_strict_options += f"{options}  "
                                    else:
                                        pass
                                print(f"[*] - Possible options for `{check_command[0]}`")
                                print(possible_strict_options)
                        # IndexError exception if command is missing an argument
                        except IndexError:
                            print("[!] - Index error, missing argument for a 'strict'-type command")
                        else:
                            pass

                    # -=-=-=- free-type command -=-=-=-
                    elif command_type == "free":
                        # Check if split input contains two objects, indicating a command and an argument
                        if len(check_command) == 2:
                            if check_command[0] in self._commands_dict:
                                self._commands_dict[check_command[0]](free_function=check_command[1],
                                                                      additional_data=self._additional_data
                                                                      [check_command[0]])
                            else:
                                pass
                        # Print error message if command is missing an argument
                        else:
                            print("[!] - Missing argument for a 'free'-type command")

                    # -=-=-=- single-type command -=-=-=-
                    elif command_type == "single":
                        if usr_input in self._commands_dict:
                            self._commands_dict[usr_input](additional_data=self._additional_data[usr_input])
                        else:
                            pass

                    # -=-=-=- parser-type command -=-=-=-
                    elif command_type == "parser":
                        if check_command[0] in self._commands_dict:
                            args = usr_input[len(check_command[0]):]
                            subprocess.run(f"python3 {self._commands_dict[check_command[0]]} {args}", shell=True)

                # A special help command for strict-type commands. By typing "help <command name>", it will display
                # all the options available to that strict-type command name
                elif len(check_command) == 2 and check_command[0] == "help":
                    if check_command[1] in self._command_type:
                        get_help_command = self._command_type[check_command[1]]
                        if get_help_command == "strict":
                            print(f"[*] - Options for {check_command[1]}\n")
                            for help_options in self._command_options[check_command[1]]:
                                print(f"[+] - {help_options}")
                        else:
                            pass

                # Give the user possible command suggestions based on the input
                else:
                    possible_commands = ""
                    for commands in self._commands_dict:
                        if commands.startswith(check_command[0]):
                            possible_commands += f"{commands}  "
                        else:
                            pass
                    print("[*] - Possible command(s): ")
                    print(possible_commands)
