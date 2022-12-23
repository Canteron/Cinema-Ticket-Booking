from fpdf import FPDF
import random
import string
import sqlite3

class User:

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Compra el ticket si la tarjeta es valida"""
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user = self, price=seat.get_price(), seat_number=seat_id)
                ticket.to_pdf()
                return "Compra realizada!"
            else:
                return "Hubo un problema con su tarjeta"
        else:
            return "El sitio esta ocupado"

class Seat:
    """Representa un asiento de cine que puede ser comprado por un usuario"""

    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        """Obtiene el precio de un sitio determinado"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id"=?
        """, [self.seat_id])
        price = cursor.fetchall()[0][0]
        return price

    def is_free(self):
        """Comprueba si el sitio esta libre en la base de datos"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id"=?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]

        if result == 0:
            return True
        else:
            return False

    def occupy(self):
        """Cambia el valor de 0 a 1 para ocupar si el sitio esta libre"""
        if self.is_free():
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE "Seat" SET "taken"=1 WHERE "seat_id"=?
            """, [self.seat_id])
            connection.commit()
            connection.close()


class Card:
    """Representa la tarjeta"""

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.holder = holder
        self.cvc = cvc
        self.number = number
        self.type = type

    def validate(self, price):
        """Comprueba si la tarjeta es valida y tiene saldo suficiente.
        Le cobra el dinero de su balance
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "balance" FROM "Card" WHERE "number"=? and "cvc"=?
        """, [self.number, self.cvc])
        result = cursor.fetchall()

        if result:
            balance = result[0][0]
            if balance >= price:
                connection.execute("""
                UPDATE "Card" SET "balance"=? WHERE "number"=? and "cvc"=?
                 """, [balance - price, self.number, self.cvc])
                connection.commit()
                connection.close()
                return True


class Ticket:
    """Representa un ticket del cine adquirido por el usuario"""
    def __init__(self, user, price, seat_number):
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.seat_number = seat_number
        self.price = price
        self.user = user

    def to_pdf(self):
        """Crea un ticket en PDF"""
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Tu Ticket Digital", border=1, ln=1, align="C")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Nombre", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Ticket ID", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Precio", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Nª de asiento", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.seat_number), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output("sample.pdf", "F")


if __name__ == "__main__":

    name = input("Nombre completo: ")
    seat_id = input("Preferencia de asiento: ")
    card_type = input("Tipo de tarjeta: ")
    card_number = input("Número de tarjeta: ")
    card_cvc = input("Número CVC: ")
    card_holder = input("Nombre del titular: ")

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    print(user.buy(seat=seat, card=card))





