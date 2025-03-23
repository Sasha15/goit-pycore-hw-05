import sys
import re
import functools
from pathlib import Path
from colorama import Fore, Style

BASE_DIR = Path(__file__).parent
CONTACTS_FILE = BASE_DIR / "contacts.txt"
contacts = {}

# Decorator to handle input errors
def input_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "❌ Error: Contact not found. Enter a valid name."
        except ValueError:
            return "⚠️ Error: Give me name and phone, please."
        except IndexError:
            return "⚠️ Error: Enter the argument for the commands. Type 'help' for command usage."
        except TypeError:
            return "⚠️ Error: Enter the argument for the command. Type 'help' for command usage."
    return inner

# Display message in a specific color
# Types: success (green), error (red), info (blue), warning (yellow)
def print_colored(text: str, msg_type: str = "info"):
    colors = {
        "success": Fore.GREEN + Style.BRIGHT,
        "error": Fore.RED + Style.BRIGHT,
        "info": Fore.BLUE + Style.BRIGHT,
        "warning": Fore.YELLOW + Style.BRIGHT
    }
    print(colors.get(msg_type, Fore.WHITE) + text + Style.RESET_ALL)

# Load contacts from file during startup
def load_contacts():
    if Path(CONTACTS_FILE).exists():
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name, phone = line.strip().split(",", maxsplit=1)
                contacts[name] = phone

# Save contacts to file before exiting
def save_contacts():
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        for name, phone in contacts.items():
            f.write(f"{name},{phone}\n")

# Handle exit and save contacts
def exit_handler():
    print_colored("\nSaving contacts... Good bye!", "warning")
    save_contacts()
    sys.exit(0)

# Prepare user input for command and arguments
def parse_input(user_input: str):
    user_input = user_input.strip().lower()
    command_array = user_input.split(" ")
    command = command_array[0]
    args = command_array[1:]

    return command, args

# Add a new contact to the dictionary with decorator
@input_error
def add_contact(name: str, phone: str):
    contacts[name] = phone
    return f"✅ Contact {name} added."

# Update contact phone number with decorator
@input_error
def change_contact(name: str, new_phone: str):
    # check that name contains only letters
    if not re.fullmatch(r"[A-Za-z ]+", name):
        return "❌ Error: Name must contain only letters."

    # check that phone contains only numbers, spaces, and special characters
    if not re.fullmatch(r"\+?[0-9 ()-]+", new_phone):
        return "❌ Error: Phone number contains invalid characters."
    
    if name not in contacts:
        return f"❌ Error: Contact {name} not found."

    contacts[name] = new_phone
    return f"🔄 Contact {name} updated."

# Show specific contact phone number or error message with decorator
@input_error
def show_phone(name: str):
    return contacts.get(name, f"❌ Error: Contact {name} not found.")

# Show all contacts with decorator
@input_error
def show_all():
    if not contacts:
        return "📭 No contacts saved."
    output = "📇 Contacts List:\n" + "\n".join([f"📌 {Fore.CYAN}{name}{Style.RESET_ALL}: {Fore.GREEN}{phone}" for name, phone in contacts.items()])
    return output

@input_error
def handle_command(command:str):
    command, args = parse_input(command)

    match command:
        case "hello":
            return "👋 How can I help you?"
        case "add":
            return add_contact(*args)
        case "change":
            return change_contact(*args)
        case "phone":
            return show_phone(*args)
        case "all":
            return show_all()
        case "help":
            return "ℹ️ Available commands: hello, add, change, phone, all, help, exit or close"
        case "exit" | "close":
            exit_handler()
        case _:
            return "❌ Invalid command. Type 'help' to see available commands."


def main():
    load_contacts()
    print_colored("Welcome to the assistant bot!", "info")
    try:
        while True:
            try:
                command = input(Fore.YELLOW + "Enter a command: " + Style.RESET_ALL)
                response = handle_command(command)
                if response:
                    print_colored(response, "success" if "✅" in response or "🔄" in response else "error" if "❌" in response else "info")
            except Exception as e:
                print_colored(f"Error: {e}", "error")
    except KeyboardInterrupt:
        exit_handler()

if __name__ == '__main__':
    main()