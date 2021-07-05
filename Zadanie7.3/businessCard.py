#================================================================
class BaseContact:
    def __init__(self, first_name, last_name, phone_number, email):
        self.first_name     = first_name
        self.last_name      = last_name
        self.phone_number   = phone_number
        self.email          = email
        
    @property
    def label_length(self):
        return len(self.first_name) + len(self.last_name) + 1

    #----------------------------------------------------------------
    def __repr__(self):
        return f"{self.first_name} {self.last_name} as BaseContact"

    def contact(self):
        print("Wybieram numer ", self.phone_number, "i dzwonię do", self.first_name, self.last_name)

#================================================================
class BusinessContact(BaseContact):
    def __init__(self, company, job, private_phone_number, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.company                = company
        self.job                    = job
        self.private_phone_number   = private_phone_number
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name} as BusinessContact"
