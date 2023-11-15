import pickle
import socket


def send_command(command, data):
    server_address = ('localhost', 10024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        message = f"{command},{data}"
        sock.sendto(message.encode('utf-8'), server_address)
        response, _ = sock.recvfrom(1024)
        decoded_response = pickle.loads(response)
        print(decoded_response)

    finally:
        sock.close()


def main():
    while True:
        print("Available commands:")
        print("1. Delete record (Command: -)")
        print("2. Count records (Command: n)")
        print("3. Generate report (Command: all)")
        print("4. Add new record (Command: +)")
        print("5. Exit (Command: q)")

        user_input = input("Enter command: ").lower()

        if user_input == 'q':
            break

        elif user_input == '-':
            key = input("Enter record key: ")
            send_command(user_input, key)

        elif user_input == 'n':
            send_command(user_input, '')

        elif user_input == 'all':
            send_command(user_input, '')

        elif user_input == '+':
            key = input("Enter record key: ")
            brand = input("Enter brand: ")
            model = input("Enter model: ")
            cost = input("Enter cost: ")
            send_command(user_input, f"{key},{brand},{model},{cost}")

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
