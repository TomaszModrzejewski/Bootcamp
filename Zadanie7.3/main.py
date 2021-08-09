import random
from faker import Faker
from businessCard import BaseContact, BusinessContact

#----------------------------------------------------------------
def generate_business_card(quantity=1):
    business_cards = list()
    fake = Faker('pl_PL')

    for _ in range(quantity):
        bcard = BaseContact(    fake.first_name(),
                                fake.last_name(),
                                fake.phone_number(),
                                fake.email() ) 

        business_cards.append(bcard)

    return business_cards

#----------------------------------------------------------------
def create_contacts(quantity=1):
    fake = Faker('pl_PL')

    for _ in range(quantity):
        if random.randrange(2) == 0:
            yield BaseContact(  fake.email(),
                                fake.first_name(),
                                fake.last_name(),
                                fake.phone_number() )
        else:
            yield BusinessContact(  fake.company(),
                                    fake.job(),
                                    fake.phone_number(),
                                    fake.email(),
                                    fake.first_name(),
                                    fake.last_name(),
                                    fake.phone_number() )
                                        
#================================================================
if __name__ == "__main__":
    first_name      = 'Natan'
    last_name       = 'Bodych'
    email           = 'natan78@gmail.com'
    phone_number    = '+48 32 032 71 77'
    work_number     = '664 680 015'
    company         = 'Bojczuk s.c.'
    job             = 'Hutnik'

    base_contact        = BaseContact(  first_name=first_name, last_name=last_name, email=email, phone_number=phone_number  )

    business_contact    = BusinessContact(  first_name=first_name, last_name=last_name, company=company, job=job,
                                            email=email, phone_number=work_number, private_phone_number=phone_number    )

    base_contact.contact()
    business_contact.contact()

    print(base_contact.label_length)

    for element in create_contacts(3):
        print(element)
