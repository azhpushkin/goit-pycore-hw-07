from datetime import datetime, timedelta
from collections import UserDict
from typing import Optional


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone_number, new_phone_number):
        phone = self.find_phone(old_phone_number)
        if phone:
            phone.value = new_phone_number

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"
    
    def __repr__(self):
        return self.__str__()


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name) -> Optional[Record]:
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, today=None) -> list[Record]:
        today = today or datetime.today()
        if isinstance(today, datetime):
            today = today.date()
            
        upcoming_birthdays = []
        
        for name, record in self.data.items():
            if not record.birthday:
                continue

            birthday = record.birthday.value
            
            this_year_birthday = birthday.replace(year=today.year)
            days_until_birthday = (this_year_birthday - today).days

            if 0 <= days_until_birthday <= 7:
                if this_year_birthday.weekday() in (5, 6):
                    # If birthday is on a weekend then congrat of Monday
                    days_to_add = 7 - this_year_birthday.weekday()
                    this_year_birthday += timedelta(days=days_to_add)
                
                upcoming_birthdays.append(record)
        
        return upcoming_birthdays


if __name__ == '__main__':

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John Doe")
    john_record.add_phone("1234567890")
    john_record.add_birthday("23.01.1985")

    # Створення запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    john_record.add_birthday("27.01.1990")


    book.add_record(john_record)
    book.add_record(jane_record)


    test_today = datetime(year=2024, month=1, day=22).date()
    upcoming_birthdays = book.get_upcoming_birthdays(today=test_today)
    print("Список привітань на цьому тижні:", upcoming_birthdays)
