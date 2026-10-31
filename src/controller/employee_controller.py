from PyQt5.QtCore import QObject, pyqtSignal

from src.model.employee_model import EmployeeModel


class EmployeeController(QObject):
    """Controller for employee actions."""

    employee_changed = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.view.controller = self

    def load_employees(self):
        employees = EmployeeModel.get_all_employees()
        self.view.load_employees(employees)

    def add_employee(self, data):
        EmployeeModel.add_employee(
            data["first_name"],
            data["last_name"],
            data.get("position", ""),
            data.get("vacation_credit", 22),
            data.get("last_year_remaining", 0),
        )
        self.load_employees()
        self.employee_changed.emit()

    def update_employee(self, emp_id, data):
        EmployeeModel.update(
            emp_id,
            data["first_name"],
            data["last_name"],
            data.get("position", ""),
            data.get("vacation_credit", 22),
            data.get("last_year_remaining", 0),
            data.get("vacation_used", 0),
        )
        self.load_employees()
        self.employee_changed.emit()

    def delete_employee(self, emp_id):
        EmployeeModel.remove_employee(emp_id)
        self.load_employees()
        self.employee_changed.emit()
