import abc
from functools import wraps
from typing import Callable, List, Optional, Set, Tuple
import time
import os
import inspect

EXIT = "exit"
commands_hostory: List[str] = []
MAX_HISTORY_SIZE = 100
env_variables: dict[str, str] = {}
aliases: dict[str, str] = {}


def add_to_history(command: str) -> None:
    """Add a command to the history, maintaining a maximum size."""
    commands_hostory.append(command)
    if len(commands_hostory) > MAX_HISTORY_SIZE:
        commands_hostory.pop(0)  # Remove the oldest command if history exceeds max size


class Command(abc.ABC):
    """To add new command, implemant this class"""

    name: str
    doc: str
    usage: str

    @staticmethod
    def run(*args) -> None:
        pass


class Echo(Command):
    name: str = "echo"
    doc: str = "Echo the arguments passed to the command."
    usage: str = "[args...]"

    @staticmethod
    def run(*args) -> None:
        print(" ".join(args))


class Man(Command):
    name: str = "man"
    doc: str = "Display the manual for a command."
    usage: str = "<command_name>"

    @staticmethod
    def run(command_name: str) -> None:
        command = COMMANDS.get(command_name)
        if command is None:
            print(f"No manual entry for '{command_name}'")
            return
        print(f"{command.name}: {command.doc}")


class Upper(Command):
    name: str = "upper"
    doc: str = "Convert the arguments to uppercase."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(arg.upper() for arg in args))


class Lower(Command):
    name: str = "lower"
    doc: str = "Convert the arguments to lowercase."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(arg.lower() for arg in args))


class Rev(Command):
    name: str = "rev"
    doc: str = "Reverse the order of the arguments passed to the command."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(reversed(args)))


class Len(Command):
    name: str = "len"
    doc: str = "Display the length of each argument."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(str(len(arg)) for arg in args))


class Uniq(Command):
    name: str = "uniq"
    doc: str = "Remove duplicate arguments."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        args_seen: Set[str] = set()
        for arg in args:
            if arg not in args_seen:
                print(arg, end=" ")
                args_seen.add(arg)
        print()


class count(Command):
    name: str = "count"
    doc: str = "Count the number of arguments."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(len(args))


class sort(Command):
    name: str = "sort"
    doc: str = "Sort the arguments."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(sorted(args)))


class Reverse(Command):
    name: str = "reverse"
    doc: str = "Reverse the order of the arguments."
    usage: str = "[args...]"

    @staticmethod
    def run(*args: str) -> None:
        print(" ".join(reversed(args)))


class sleep(Command):
    name: str = "sleep"
    doc: str = "Sleep for a specified number of seconds."
    usage: str = "<seconds>"

    @staticmethod
    def run(seconds: str) -> None:
        try:
            time.sleep(float(seconds))
        except ValueError:
            print("Invalid number of seconds.")


class pwd(Command):
    name: str = "pwd"
    doc: str = "Print the current working directory."
    usage: str = ""

    @staticmethod
    def run() -> None:
        print(os.getcwd())


def check_path_exist(pos: int = 0, name: str = "path") -> Callable:
    """Decorator factory to check if a file or directory exists before running the command."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = args[pos] if args else kwargs[name]
            if not os.path.exists(path):
                print(f"No such file or directory: {path}")
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_is_directory(pos: int = 0, name: str = "path") -> Callable:
    """Decorator factory to check if a path is a directory before running the command."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = args[pos] if args else kwargs[name]
            if not os.path.isdir(path):
                print(f"Not a directory: {path}")
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_is_file(pos: int = 0, name: str = "path") -> Callable:
    """Decorator factory to check if a path is a file before running the command."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = args[pos] if args else kwargs[name]
            if not os.path.isfile(path):
                print(f"Not a file: {path}")
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


class cd(Command):
    name: str = "cd"
    doc: str = "Change the current working directory."
    usage: str = "<directory>"

    @staticmethod
    @check_path_exist()
    @check_is_directory()
    def run(path: str) -> None:
        os.chdir(path)


def resolve_defualt(name: str = "path", pos: int = 0) -> Callable:
    """Decorator factory to resolve default values"""

    def decorator(func: Callable) -> Callable:

        # resolve default using inspect
        signature = inspect.signature(func)
        print(signature.parameters)
        default_value = signature.parameters[name].default

        @wraps(func)
        def wrapper(*args, **kwargs):
            if name not in kwargs and len(args) <= pos:
                kwargs[name] = default_value
            return func(*args, **kwargs)

        return wrapper

    return decorator


class ls(Command):
    name: str = "ls"
    doc: str = "List files in the current directory."
    usage: str = "[directory]"

    @staticmethod
    @resolve_defualt(name="path", pos=0)
    @check_path_exist()
    @check_is_directory()
    def run(path: str = ".") -> None:
        files = os.listdir(path)
        print(" ".join(files))


class mkdir(Command):
    name: str = "mkdir"
    doc: str = "Create a new directory."
    usage: str = "<directory_name>"

    @staticmethod
    def run(path: str) -> None:
        if os.path.exists(path):
            print(f"Directory already exists: {path}")
            return
        os.mkdir(path)


class rmdir(Command):
    name: str = "rmdir"
    doc: str = "Remove an empty directory."
    usage: str = "<directory_name>"

    @staticmethod
    @check_path_exist()
    @check_is_directory()
    def run(path: str) -> None:
        os.rmdir(path)


class touch(Command):
    name: str = "touch"
    doc: str = "Create a new file or update the timestamp of an existing file."
    usage: str = "<file_name>"

    @staticmethod
    def run(path: str) -> None:
        if os.path.exists(path):
            print(f"File already exists: {path}")
        else:
            with open(path, "w"):
                pass


class rm(Command):
    name: str = "rm"
    doc: str = "Remove a file."
    usage: str = "<file_name>"

    @staticmethod
    @check_path_exist()
    @check_is_file()
    def run(path: str) -> None:
        delete_confirmation = input(
            f"Are you sure you want to delete '{path}'? (y/[n]): "
        )
        if delete_confirmation.lower() == "y":
            os.remove(path)
            print(f"File '{path}' deleted.")
        else:
            print("Deletion cancelled.")


class cat(Command):
    name: str = "cat"
    doc: str = "Display the contents of a file."
    usage: str = "<file_name>"

    @staticmethod
    def run(*file_names: str) -> None:
        for file_name in file_names:
            if not os.path.exists(file_name):
                print(f"No such file: {file_name}")
                continue
            if not os.path.isfile(file_name):
                print(f"{file_name} is not a file.")
                continue
            print(f"{file_name}:")
            try:
                with open(file_name, "r") as f:
                    print(f.read(), end="")
            except PermissionError:
                print(f"Permission denied: {file_name}")


class head(Command):
    name: str = "head"
    doc: str = "Display the first few lines of a file."
    usage: str = "<number_of_lines> <file_name>"

    @staticmethod
    @check_path_exist(pos=1, name="file_name")
    @check_is_file(pos=1, name="file_name")
    def run(number_of_lines: str, file_name: str) -> None:
        try:
            num_lines = int(number_of_lines)
        except ValueError:
            print("Invalid number of lines.")
            return
        if num_lines < 0:
            print("Number of lines must be non-negative.")
            return
        with open(file_name, "r") as f:
            for _ in range(num_lines):
                line = f.readline()
                if not line:
                    break
                print(line, end="")


class tail(Command):
    name: str = "tail"
    doc: str = "Display the last few lines of a file."
    usage: str = "<number_of_lines> <file_name>"

    @staticmethod
    @check_is_file(pos=1, name="file_name")
    @check_path_exist(pos=1, name="file_name")
    def run(number_of_lines: str, file_name: str) -> None:
        try:
            num_lines = int(number_of_lines)
        except ValueError:
            print("Invalid number of lines.")
            return
        if num_lines < 0:
            print("Number of lines must be non-negative.")
            return
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines[-num_lines:]:
                print(line, end="")


class write(Command):
    name: str = "write"
    doc: str = "Write text to a file."
    usage: str = "<file_name> [text...]"

    @staticmethod
    def run(file_name: str, *text: str) -> None:
        if os.path.exists(file_name) and not os.path.isfile(file_name):
            print(f"{file_name} is not a file.")
            return
        with open(file_name, "a") as f:
            f.write(" ".join(text) + "\n")
        print(f"Text written to {file_name}")


def remove_quates(func: Callable) -> Callable:
    def wrapper(*args: str) -> None:
        new_args = []
        curr_arg = ""
        in_quotes = False
        for arg in args:
            if arg.startswith('"') and not in_quotes:
                in_quotes = True
                curr_arg = arg[1:]
            elif arg.endswith('"') and in_quotes:
                in_quotes = False
                curr_arg += " " + arg[:-1]
                new_args.append(curr_arg)
                curr_arg = ""
            elif in_quotes:
                curr_arg += " " + arg
            else:
                new_args.append(arg)
        if curr_arg:
            print("Unmatched quotes in arguments.")
            return
        return func(*new_args)

    return wrapper


class grep(Command):
    name: str = "grep"
    doc: str = "Search for a pattern in a file."
    usage: str = "<pattern> <file_name>"

    @staticmethod
    @remove_quates
    @check_path_exist(pos=1, name="file_name")
    @check_is_file(pos=1, name="file_name")
    def run(pattern: str, file_name: str) -> None:
        with open(file_name, "r") as f:
            for line in f:
                if pattern in line:
                    print(line, end="")


class history(Command):
    name: str = "history"
    doc: str = "Display the commands history."
    usage: str = ""

    @staticmethod
    def run() -> None:
        if not commands_hostory:
            print("No commands in history.")
            return
        for i, command in enumerate(commands_hostory, start=1):
            print(f"{i}: {command}")


class set(Command):
    name: str = "set"
    doc: str = "Set an environment variable."
    usage: str = "<variable_name> <value>"

    @staticmethod
    @remove_quates
    def run(variable_name: str, value: str) -> None:
        if not variable_name.isidentifier():
            print(f"Invalid variable name: {variable_name}")
            return
        env_variables[variable_name] = value


class unset(Command):
    name: str = "unset"
    doc: str = "Unset an environment variable."
    usage: str = "<variable_name>"

    @staticmethod
    def run(variable_name: str) -> None:
        if variable_name in env_variables:
            del env_variables[variable_name]
        else:
            print(f"Variable '{variable_name}' not set.")


class env(Command):
    name: str = "env"
    doc: str = "Display all environment variables."
    usage: str = ""

    @staticmethod
    def run() -> None:
        if not env_variables:
            print("No environment variables set.")
            return
        for var, value in env_variables.items():
            print(f"{var}: {value}")


class alias(Command):
    name: str = "alias"
    doc: str = "Create an alias for a command."
    usage: str = "<alias_name> <command>"

    @staticmethod
    @remove_quates
    def run(alias_name: str, command: str) -> None:
        if not alias_name.isidentifier():
            print(f"Invalid alias name: {alias_name}")
            return
        aliases[alias_name] = command


class unalias(Command):
    name: str = "unalias"
    doc: str = "Remove an alias."
    usage: str = "<alias_name>"

    @staticmethod
    def run(alias_name: str) -> None:
        if alias_name in aliases:
            del aliases[alias_name]
        else:
            print(f"Alias '{alias_name}' not found.")


COMMANDS = {c.name: c for c in Command.__subclasses__()}


def parse_command(line: str) -> Tuple[str, List[str]]:
    """parse line of command args and return a tuple of command and list og args."""
    line = line.strip()
    if not line:
        return "", []
    parts = line.split()
    if any(part.startswith("$") for part in parts):
        for i in range(len(parts)):
            if parts[i].startswith("$"):
                last_dolar = parts[i].rfind("$")
                parts[i] = parts[i][:last_dolar] + env_variables.get(
                    parts[i][last_dolar + 1 :], ""
                )
        return parse_command(" ".join(parts))

    command_name = parts[0]
    args = parts[1:]

    if command_name in aliases:
        command_name = aliases[command_name]
        return parse_command(command_name + " " + " ".join(args))

    return command_name, args


def run_shell() -> None:
    try:
        while True:
            line = input(">>> ")
            add_to_history(line)
            command_name, args = parse_command(line)
            if command_name == EXIT:
                break
            command = COMMANDS.get(command_name)

            if command is None:
                print(f"Unknown command: {command_name}")
                continue

            try:
                command.run(*args)
            except TypeError:
                print(f"Usage: {command.name} {command.usage}")
            except KeyboardInterrupt:
                print("\nInterrupted by user.")
            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"Usage: {command.name} {command.usage}")
    except KeyboardInterrupt:
        pass
    print("Exiting shell.")


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
