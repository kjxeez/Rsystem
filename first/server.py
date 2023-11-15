import socket
import pickle

# Пример данных на сервере
car_data = {
    '1': {"brand": "Toyota", "model": "Camry", "cost": 25000},
    '2': {"brand": "Honda", "model": "Accord", "cost": 22000},
    # Добавьте другие данные по необходимости
}

def handle_command(command, data):
    global car_data

    if command == "-":
        key = data
        if key in car_data:
            del car_data[key]
            response = "Record deleted successfully."
        else:
            response = "Record not found."

    elif command == "n":
        response = f"Number of records: {len(car_data)}"

    elif command == "report":
        sorted_data = sorted(car_data.items(), key=lambda x: x[1]['cost'])
        response = pickle.dumps(sorted_data)

    else:
        response = "Unknown command."

    return response

def main():
    server_address = ('localhost', 10021)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    print('Server listening on {}:{}'.format(*server_address))

    while True:
        data, client_address = sock.recvfrom(1024)
        command, *params = data.decode().split(',')
        response = handle_command(command, *params)

        # Ensure that the response is pickled before sending
        sock.sendto(pickle.dumps(response), client_address)

if __name__ == "__main__":
    main()