import socket
import pickle

# Пример данных на сервере
car_data = {
    "ABC123": {"brand": "Toyota", "model": "Camry", "cost": 25000},
    "XYZ789": {"brand": "Honda", "model": "Accord", "cost": 22000},
    # Добавьте другие данные по необходимости
}

def handle_command(command, data):
    global car_data

    if command == "delete":
        key = data
        if key in car_data:
            del car_data[key]
            return "Record deleted successfully."
        else:
            return "Record not found."

    elif command == "count":
        return f"Number of records: {len(car_data)}"

    elif command == "report":
        sorted_data = sorted(car_data.items(), key=lambda x: x[1]['cost'])
        return pickle.dumps(sorted_data)

    else:
        return "Unknown command."

def main():
    server_address = ('localhost', 10016)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    print('Server listening on {}:{}'.format(*server_address))

    while True:
        data, client_address = sock.recvfrom(1024)
        command, *params = data.decode().split(',')
        response = handle_command(command, *params)
        if isinstance(response, str):
            response = response.encode()
        sock.sendto(response, client_address)

if __name__ == "__main__":
    main()
