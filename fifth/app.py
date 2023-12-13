from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Employee import Employee, Base
from datetime import datetime
app = Flask(__name__)

engine = create_engine('sqlite:///employees.db', echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def init_data():
    # Проверяем, есть ли уже записи в базе данных
    if session.query(Employee).count() == 0:
        # Добавляем начальные данные
        employees_data = [
            {'name': 'Иванов Иван Иванович', 'position': 'Менеджер', 'department': 'Отдел продаж',
             'birthday': '01.01.1990', 'number': '123456789'},
            {'name': 'Петров Петр Петрович', 'position': 'Разработчик', 'department': 'Отдел разработки',
             'birthday': '02.02.1991', 'number': '987654321'},
            # Добавьте еще записей
        ]

        for data in employees_data:
            employee = Employee(**data)
            session.add(employee)

        session.commit()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_birthday = request.form.get('search_birthday')
        filter_by_name = request.form.get('filter_by_name')
        if search_birthday:
            employees = session.query(Employee).filter_by(birthday=search_birthday).all()
            return render_template('index.html', num_employees=len(employees), employees=employees)
        if filter_by_name:
            employees = session.query(Employee).filter(Employee.name.startswith(filter_by_name)).all()
            return render_template('index.html', num_employees=len(employees), employees=employees)
        if 'sort_by_position' in request.form:
            employees = session.query(Employee).order_by(Employee.position).all()
            return render_template('index.html', num_employees=len(employees), employees=employees)
        if 'add' in request.form:
            # Обработка формы для создания нового сотрудника
            name = request.form['name']
            position = request.form['position']
            department = request.form['department']
            birthday = request.form['birthday']
            number = request.form['number']
            new_employee = Employee(name=name, position=position, department=department, birthday=birthday, number=number)
            session.add(new_employee)
            session.commit()
        elif 'delete' in request.form:
            # Обработка формы для удаления сотрудника
            employee_id = request.form['employee_id']
            employee_to_delete = session.query(Employee).filter_by(id=employee_id).first()
            session.delete(employee_to_delete)
            session.commit()
        elif 'edit' in request.form:
            # Обработка формы для редактирования сотрудника
            employee_id = request.form['employee_id']
            if employee_id:
                return redirect(url_for('edit', employee_id=employee_id))
    sort_option = request.args.get('sort')
    if sort_option == 'position':
        employees = session.query(Employee).order_by(Employee.position).all()
    else:
        employees = session.query(Employee).all()

    num_employees = len(employees)
    return render_template('index.html', num_employees=num_employees, employees=employees)

    num_employees = session.query(Employee).count()
    employees = session.query(Employee).all()
    return render_template('index.html', num_employees=num_employees, employees=employees)

@app.route("/edit/<int:employee_id>", methods=['GET', 'POST'])
def edit(employee_id):
    employee_to_edit = session.query(Employee).filter_by(id=employee_id).first()

    if request.method == 'POST':
        # Обработка формы для редактирования сотрудника
        employee_to_edit.name = request.form['name']
        employee_to_edit.position = request.form['position']
        employee_to_edit.department = request.form['department']
        employee_to_edit.birthday = request.form['birthday']
        employee_to_edit.number = request.form['number']
        session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee_to_edit)

    num_employees = session.query(Employee).count()
    employees = session.query(Employee).all()
    return render_template('index.html', num_employees=num_employees, employees=employees)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    init_data()
    app.run(debug=True)
