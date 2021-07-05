import faker
import typing
import logging
import random

fake = faker.Faker()


class BaseContact:

    def __init__(self, name: str, surname: str, phone_number: str, email: str):
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.email = email

    def contact(self):
        print(f"Wybieram numer {self.phone_number} i dzwonię do {self.name} {self.surname}")

    @property
    def label_length(self) -> int:
        return len(self.name) + len(self.surname)


class BusinessContact(BaseContact):

    def __init__(self,
                 name: str,
                 surname: str,
                 phone_number: str,
                 email: str,
                 work_position: str,
                 company: str,
                 work_phone_number: str
                 ):
        super().__init__(name, surname, phone_number, email)
        self.work_position = work_position
        self.company = company
        self.work_phone_number = work_phone_number

    def contact(self):
        print(f"Wybieram numer {self.work_phone_number} i dzwonię do {self.name} {self.surname}")


def create_contacts(contact_type: typing.ClassVar, amount: int):
    contact_list = []

    for _ in range(amount):
        name, surname = fake.first_name(), fake.last_name()
        phone_number = fake.random_int(100000000, 999999999)
        email = fake.email()
        if contact_type == BusinessContact:
            work_position = fake.job()
            company = fake.company()
            work_phone_number = fake.random_int(100000000, 999999999)
            contact_list.append(
                BusinessContact(
                    name=name,
                    surname=surname,
                    phone_number=phone_number,
                    email=email,
                    company=company,
                    work_position=work_position,
                    work_phone_number=work_phone_number
                )
            )
        elif contact_type == BaseContact:
            contact_list.append(
                BaseContact(
                    name=name,
                    surname=surname,
                    phone_number=phone_number,
                    email=email
                )
            )
        else:
            logging.warning(
                f"Unsupported contact type: {contact_type}, valid types are: {BaseContact}, {BusinessContact}"
                            )

    return contact_list


if __name__ == "__main__":
    contacts = []
    contacts += create_contacts(BusinessContact, 15)
    contacts += create_contacts(BaseContact, 30)

    random.shuffle(contacts)

    for contact in contacts:
        print(contact.label_length, end=" ")
        contact.contact()
