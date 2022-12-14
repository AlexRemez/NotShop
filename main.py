from models import Users, Tickets, Orders, Products
from datetime import datetime

print()
print(' Добро пожаловать в "не магазин" '.center(39, '='))
print('\nЗдесь вы можете обменивать тикеты для того,'
        ' чтобы приобретать товары\n')
while True:
    print('Для взаимодействия'
          ' используйте команды:\n> Товары\n> Зарегистрироваться'
          '\n> Войти')
    user_comand = input()
    initialization = False


    if user_comand.lower() == 'товары':
        Products.show_products()
        print('\nДля взаимодействия используйте команды:\n\n> Главное меню\n' )
        while True:
            choose = input()
            if choose.lower() == 'главное меню':
                break
            else:
                print('Введите корректный запрос!')
                continue
        continue


    if user_comand.lower() == 'зарегистрироваться':
        while True:
            login: str = input('Введите логин > ')
            if Users.is_exist(login):
                print('Пользователь с таким ником уже есть!')
                continue
            else:
                password: str = input('Введите пароль > ')
                Users.create(username=login, password=password)
                initialization = True
                break


    if user_comand.lower() == 'войти':
        while True:
            login: str = input('Введите логин > ')
            password: str = input('Введите пароль > ')
            if Users.is_exist_user(username=login, password=password):
                print("Вы успешно авторизованы!\n")
                initialization = True
                break
            else:
                print("Неверный логин или пароль!")
                continue


    if initialization:
        print(' Добро пожаловать в "не магазин" '.center(39, '='))
        print('\nЗдесь вы можете обменивать тикеты для того,'
                ' чтобы приобретать товары\n')
        while True:
            order = False
            print(
                  'Для взаимодействия'
                  ' используйте команды:\n> Товары\n> Купить'
                  '\n> Профиль\n> Тикет'
            )

            user_comand = input()


            if user_comand.lower() == 'товары':
                Products.show_products()
                print()
                continue


            if user_comand.lower().startswith('тикет'):
                    try:
                        ticket_uuid = user_comand.split()[1]
                    except IndexError:
                        print("Неверный Тикет")
                        continue
                    else:
                        if Tickets.valid_ticket(ticket_uuid=ticket_uuid):
                            Tickets.not_available(ticket_uuid=ticket_uuid)
                            Users.add_point(Users.get(Users.username == login))
                            print(f'Вы успешно обменяли тикет на 20 поинтов!'
                                  f'\nТеперь у вас - {Users.show_points(login=login)} поинтов')
                        else:
                            print("Что-то пошло не так!")


            if (user_comand.lower().startswith('купить') or order == True) and len(user_comand.split()) == 3:
                product_id, count = user_comand.split()[1], user_comand.split()[2]
                # Проверяем возможность оформления заказа (кол-во и поинты)
                if Orders.valid_order(count=count, username=login, product_id=product_id):
                    product = Products.select().where(Products.id == product_id).execute()
                    for i in product:
                        product_name = i.name
                    # Добавляем в таблицу Orders ID товара, кол-во и время покупки
                    Orders.make_order(
                        username=login,
                        product_id=product_id,
                        count=count
                    )
                    print(f'Вы "успешно купили {product_name}" в количестве: {count}')
                    print(f'У вас осталось - {Users.show_points(login=login)} поинтов')
                else:
                    print("Введите корректный запрос!")

            if user_comand.lower() == 'профиль':
                print(Users.info(login))
                continue




