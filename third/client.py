from xmlrpc.client import ServerProxy


server = ServerProxy('http://127.0.0.1:7001')

def print_menu():
    print("\nМеню:")
    print("1. Добавить")
    print("2. Удалить запись")
    print("3. Вычислить дисперсию ")
    print("4. Сформировать отчет")
    print("5. Автобусы")
    print("6. Вывести подсказку")
    print("7. Выход")

while True:
    print_menu()
    choice = input("Введите номер операции: ")

    if choice == '1':
        number = input("Введите номер автобуса: ")
        brand = input("Введите марку автобуса: ")
        driver = input("Введите фамилию и инициалы водителя: ")
        mileage = int(input("Введите пробег автобуса в км: "))
        print(server.add_bus(number, brand, driver, mileage))

    elif choice == '2':
        number = input("Введите номер автобуса для удаления: ")
        print(server.delete_bus(number))

    elif choice == '3':
        print(server.calculate_variance())

    elif choice == '4':
        print(server.generate_report())



    elif choice == '5':
        print(server.get_all_buses())

    elif choice == '6':
        print("\nПодсказка:")
        print("1. Добавить новую запись: Добавляет данные об автобусе в базу.")
        print("2. Удалить запись с заданным ключом: Удаляет данные об автобусе по его номеру.")
        print("3. Вычислить дисперсию числового поля в таблице: Вычисляет дисперсию пробега автобусов.")
        print("4. Сформировать отчет – для каждой марки максимальный пробег: Выводит отчет о максимальных пробегах по маркам.")
        print("5. Вывести все данные об автобусах: Выводит все сохраненные данные об автобусах.")
        print("6. Вывести подсказку: Выводит это меню.")
        print("7. Выход: Завершает программу.")

    elif choice == '7':
        print("Программа завершена.")
        break

    else:
        print("Некорректный ввод. Пожалуйста, выберите операцию из меню.")
