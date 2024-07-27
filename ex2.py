from functools import wraps
import records

def input_error(handler):
    @wraps(handler)
    def inner(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError:
            return "No phone for this name."
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Invalid input. Please provide correct arguments."
    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except:
        print('Invalid input')
        return None, None


@input_error
def add_contact(args: list[str], book: records.AddressBook) -> str:
    name, phone = args
    record = book.find(name)
    if not record:
        record = records.Record(name)
        book.add_record(record)
    
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args: list[str], book: records.AddressBook) -> str:
    name, old_phone, new_phone = args
    record = book.find(name)
    
    if not record:
        return "Contact not found."
    else:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."    



@input_error
def add_birthday(args: list[str], book: records.AddressBook) -> str:
    name, birthday = args
    record = book.find(name)
    if not record:
        record = records.Record(name)
        book.add_record(record)
    
    record.add_birthday(birthday)
    return "Contact added."


@input_error
def show_phone(args: list[str], book: records.AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record:
        return 'No record found'
    else:
        return ','.join([p.value for p in record.phones])
    
@input_error
def show_birthday(args: list[str], book: records.AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record:
        return 'No record found'
    else:
        return record.birthday.value

@input_error
def show_all(book: records.AddressBook) -> str:
    data = []
    for record in book.values():
        for phone in record.phones:
            data.append(f"{record.name}: {phone.value}")
    return "\n".join(data)

@input_error
def show_birthdays(book: records.AddressBook) -> str:
    records = book.get_upcoming_birthdays()
    
    data = []
    for record in records:
        data.append(f"{record.name}: {record.birthday.value}")
    return "\n".join(data)



def main() -> None:
    book: records.AddressBook = records.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "birthdays":
            print(show_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
