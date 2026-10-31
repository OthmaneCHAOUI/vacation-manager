from src.model.vacation_model import VacationModel
from src.model.employee_model import EmployeeModel
from src.service.vacation_service import (
    total_used_days,
    used_vacation_days,
    vacation_date_strings,
)
from PyQt5.QtCore import QObject, pyqtSignal


class VacationController(QObject):
    """Handles the logic between the VacationView and VacationModel."""

    vacation_changed = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.view.controller = self
        self.view.add_button.clicked.connect(self.add_vacation)
        self.load_employees()
        self.load_vacations()

    def load_employees(self):
        """Loads employee data and populates the view's employee combo box."""
        employees = EmployeeModel.get_all_employees()
        self.view.set_employee_list(employees)

    def load_vacations(self):
        """Loads vacation data and populates the view's table."""
        vacations = VacationModel.get_all_vacations()
        self.view.display_vacations(vacations)

    def get_employees_with_vacation(self):
        """Return employees with vacation requests for the home view."""
        return VacationModel.get_all_employees_with_vacation()

    def get_latest_vacation_for_employee(self, emp_id):
        """Return the latest vacation for an employee."""
        vacations = VacationModel.get_vacations_for_employee_by_id(emp_id)
        return vacations[0] if vacations else None

    def get_latest_vacation_dates(self, emp_id):
        """Return the dates in the employee's latest vacation interval."""
        vacation = self.get_latest_vacation_for_employee(emp_id)
        if vacation is None:
            return []
        return vacation_date_strings(vacation["start_date"], vacation["end_date"])

    def add_vacation(self):
        """Gets vacation details from the form and adds a new record to the database."""
        emp_index = self.view.employee_combo.currentIndex()
        if emp_index == -1:
            self.view.show_error("Please select an employee.")
            return

        start_date = self.view.start_date_input.date()
        end_date = self.view.end_date_input.date()
        if start_date > end_date:
            self.view.show_warning(
                "Invalid Dates",
                "The end date cannot be before the start date.",
            )
            return

        emp_id = self.view.employee_combo.itemData(emp_index)
        start_date_str = start_date.toString("yyyy-MM-dd")
        end_date_str = end_date.toString("yyyy-MM-dd")

        emp = EmployeeModel.get_employee_by_id(emp_id)
        total_credit = emp["last_year_remaining"] + emp["vacation_credit"]

        vacations = VacationModel.get_vacations_for_employee_by_id(emp_id)
        total_used = total_used_days(vacations, start_date_str, end_date_str)

        if total_used > total_credit:
            self.view.show_warning(
                "Vacation Allowance Exceeded",
                f"The employee does not have enough vacation allowance.\n"
                f"Total allowance: {total_credit} days\n"
                f"Requested after addition: {total_used} days",
            )
            return

        VacationModel.add_vacation(emp_id, start_date_str, end_date_str, "")

        EmployeeModel.update_vacation_used(emp_id, total_used)

        self.load_vacations()
        self.vacation_changed.emit()

    def delete_vacation(self, vac_ids):
        """Deletes one or more vacation requests by ID and reloads the view."""
        employee_ids = VacationModel.get_employee_ids_for_vacations(vac_ids)
        VacationModel.remove_vacations(vac_ids)
        for emp_id in employee_ids:
            vacations = VacationModel.get_vacations_for_employee_by_id(emp_id)
            EmployeeModel.update_vacation_used(
                emp_id, used_vacation_days(vacations)
            )
        self.load_vacations()
        self.vacation_changed.emit()