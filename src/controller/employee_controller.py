# src/controller/employee_controller.py
from src.model.employee_model import EmployeeModel


class EmployeeController:
    """Controller for employee actions."""

    def __init__(self, view, home_view):
        self.view = view
        self.home_view = home_view
        self.view.controller = self  # Link view to controller

    def load_employees(self):
        employees = EmployeeModel.get_all()
        self.view.load_employees(employees)

    def add_employee(self, data):
        EmployeeModel.create(
            data["first_name"],
            data["last_name"],
            data.get("position", ""),
            data.get("vacation_credit", 22),
            data.get("last_year_remaining", 0),
        )
        self.load_employees()
        self.home_view.refresh_vacation_employees()

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

    def delete_employee(self, emp_id):
        EmployeeModel.delete(emp_id)
        self.load_employees()
