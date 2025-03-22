def input_error(func):
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ValueError:
      return "Give me name and phone please."
    except IndexError:
      return "Give me name please."
    except KeyError:
      return "Contact not found."

  return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args

    if name in contacts:
        return "Contact with this name already exist."

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args

    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    
    raise KeyError()

@input_error
def show_phone(args, contacts):
    name = args[0]
    return f"{name}'s phone number is {contacts[name]}."


def show_all(contacts):
    if not contacts:
        return "No contacts found."

    contact_list = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
    return contact_list


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()