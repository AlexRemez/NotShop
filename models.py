from peewee import *
from datetime import datetime

db = MySQLDatabase(database="online_shop", host="127.0.0.1", user="root", password="remak4kko")


class Users(db.Model):
    username = CharField(max_length=30, unique=True)
    password = CharField(max_length=30)
    points = IntegerField()

    @staticmethod
    def is_exist(username: str) -> bool:
        try:
            Users.get(Users.username == username)
        except Users.DoesNotExist:
            return False
        else:
            return True

    @staticmethod
    def is_exist_user(username: str, password: str) -> bool:
        try:
            Users.get(Users.username == username)
        except Users.DoesNotExist:
            return False
        else:
            user_id = Users.get(Users.username == username)
            user = Users.select().where(Users.id == user_id).execute()
            for i in user:
                if i.password == password:
                    return True
                else:
                    return False

    @staticmethod
    def add_point(user_id):
        user = Users.select().where(Users.id == user_id).execute()
        for i in user:
            i.points += 20
            i.save()

    @staticmethod
    def show_points(login):
        user = Users.select().where(Users.username == login).execute()
        for i in user:
            return i.points

    @staticmethod
    def orders(user_id) -> list:
        orders = Orders.select().where(Orders.user_id == user_id).execute()
        orders_list = [[str(i.order_datetime), i.count, i.product_id.cost * i.count, i.product_id.name] for i in orders]
        return orders_list


    @staticmethod
    def info(username):
        user = Users.select().where(Users.username == username).execute()
        for i in user:
            user_id = i.id
        orders = Users.orders(user_id=user_id)
        s = ''
        for x in orders:
            s += f'{x[0]:<22} {x[1]:<6} {x[2]:<6} {x[3]}\n'

        return (
            f"=== {username} ===\n"
            f"Поинтов: {Users.show_points(username)}\n\n"
            "Заказы:\n\n"
            f"{'Дата заказа':<22} {'Кол-во':<7}{'Сумма':<7}{'Название'}\n"
            f"{'-' * 47}\n"
            f"{s}"
        )


class Tickets(db.Model):
    uuid = CharField(max_length=36)
    available = BooleanField(default=True)
    user = ForeignKeyField(model=Users, field="id", null=True)

    @staticmethod
    def valid_ticket(ticket_uuid) -> bool:
        try:
            Tickets.get(Tickets.uuid == ticket_uuid)
        except Tickets.DoesNotExist:
            return False
        else:
            ticket = Tickets.select().where(Tickets.uuid == ticket_uuid).execute()
            for i in ticket:
                if i.available:
                    return True
                else:
                    return False

    @staticmethod
    def not_available(ticket_uuid) -> bool:
        ticket = Tickets.select().where(Tickets.uuid == ticket_uuid).execute()
        for i in ticket:
            i.available = False
            i.save()


class Products(db.Model):
    name = CharField(max_length=255, unique=True)
    cost = IntegerField()
    count = IntegerField()

    @staticmethod
    def show_products():
            print(f'{"ID":<4} {"Название":<10} {"Стоимость":<10} {"Кол-во":<2}')
            print(('=' * 37))
            for product in Products.select().execute():
                print(f'{product.id:<4} {product.name:<10} {product.cost:<10} {product.count:<2}')


class Orders(db.Model):
    user_id = ForeignKeyField(model=Users, field="id")
    product_id = ForeignKeyField(model=Products, field="id")
    count = IntegerField()
    order_datetime = DateTimeField()

    @staticmethod
    def make_order(username, product_id, count):
        user_id = Users.get(Users.username == username)
        Orders.create(
            user_id=user_id,
            product_id=product_id,
            count=count,
            order_datetime=datetime.now()
        )
        product = Products.select().where(Products.id == product_id).execute()
        for i in product:
            i.count -= int(count)
            i.save()
            cost = i.cost
        user = Users.select().where(Users.id == user_id).execute()
        for i in user:
            i.points -= cost * int(count)
            i.save()

    @staticmethod
    def valid_order(count, username, product_id):
        user = Users.select().where(Users.username == username).execute()
        for i in user:
            points = i.points
        product = Products.select().where(Products.id == product_id).execute()
        for i in product:
            product_cost = i.cost
            product_count = i.count
        if points < (product_cost * int(count)) or product_count < int(count) or int(count) <= 0 \
                or (product_cost * int(count)) <= 0:
            return False
        else:
            return True
