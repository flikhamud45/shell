import abc
from typing import List, Optional, Tuple
import time
import os

EXIT = "exit"


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
        args_seen = set()
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


COMMANDS = {c.name: c for c in Command.__subclasses__()}


def parse_command(line: str) -> Tuple[str, List[str]]:
    """parse line of command args and return a tuple of command and list og args."""
    line = line.strip()
    if not line:
        return "", []
    parts = line.split()
    return parts[0], parts[1:]


def run_shell() -> None:
    try:
        while True:
            line = input(">>> ")
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
