import socket
import pickle

# Пример данных на сервере
car_data = {
    '1': {"brand": "Toyota", "model": "Camry", "cost": 25000},
    '2': {"brand": "Honda", "model": "Accord", "cost": 22000},
}


def handle_command(command, *params):
    global car_data

    if command == '-':
        key = params[0]
        if key in car_data:
            del car_data[key]
            response = "Record deleted successfully."
        else:
            response = "Record not found."

    elif command == 'n':
        response = f"Number of records: {len(car_data)}"

    elif command == 'all':
        sorted_data = sorted(car_data.items(), key=lambda x: x[1]['cost'])
        response = sorted_data

    elif command == '+':
        key, brand, model, cost = params

        car_data[key] = {"brand": brand, "model": model, "cost": int(cost)}
        response = "Record added successfully."


    else:
        response = "Unknown command."
    response = pickle.dumps(response)
    return response


def main():
    server_address = ('localhost', 10025)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    print('Server listening on {}:{}'.format(*server_address))

    while True:
        data, client_address = sock.recvfrom(1024)
        command, *params = data.decode('UTF-8').split(',')
        response = handle_command(command, *params)
        sock.sendto(response, client_address)


if __name__ == "__main__":
    main()
