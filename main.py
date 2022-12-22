import random
import string


class User:

    def __init__(self, name):
        self.name = name

    def buy(self,seat, card):
        pass


class Seat:

    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        pass

    def is_free(self):
        pass

    def occupy(self):
        pass


class Card:

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.holder = holder
        self.cvc = cvc
        self.number = number
        self.type = type

    def validate(self, price):
        pass


class Ticket:
    def __init__(self, user, price, seat_number, id):
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.seat_number = seat_number
        self.price = price
        self.user = user
        print(self.id)

    def to_pdf(self):
        pass
