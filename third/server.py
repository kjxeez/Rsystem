from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


bus_data = []


def add_bus(number, brand, driver, mileage):
    bus_data.append({'number': number, 'brand': brand, 'driver': driver, 'mileage': mileage})
    return "Запись добавлена успешно."


def delete_bus(number):
    deleted_buses = [bus for bus in bus_data if bus['number'] == number]
    bus_data[:] = [bus for bus in bus_data if bus['number'] != number]

    if deleted_buses:
        return f"Записи с номером {number} удалены."
    else:
        return f"Автобусы с номером {number} не найдены."


def calculate_variance():
    if not bus_data:
        return "Нет данных для вычисления дисперсии."

    total_mileage = sum(bus['mileage'] for bus in bus_data)
    mean_mileage = total_mileage / len(bus_data)

    variance = sum((bus['mileage'] - mean_mileage) ** 2 for bus in bus_data) / (len(bus_data) - 1)

    return f"Дисперсия пробега автобусов: {variance}"


def generate_report():
    if not bus_data:
        return "Нет данных для формирования отчета."

    report = {}
    for bus in bus_data:
        brand = bus['brand']
        mileage = bus['mileage']
        if brand not in report or mileage > report[brand]:
            report[brand] = mileage

    return report


def get_all_buses():
    return bus_data


server = SimpleXMLRPCServer(('127.0.0.1', 7001), requestHandler=RequestHandler)
server.register_introspection_functions()
server.register_function(add_bus, 'add_bus')
server.register_function(delete_bus, 'delete_bus')
server.register_function(calculate_variance, 'calculate_variance')
server.register_function(generate_report, 'generate_report')
server.register_function(get_all_buses, 'get_all_buses')

print("*** RPC сервер автобусного парка стартовал ***")
server.serve_forever()
