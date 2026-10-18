from src.model.vacation_model import VacationModel
from src.model.employee_model import EmployeeModel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime


class VacationController(QObject):
    """Handles the logic between the VacationView and VacationModel."""

    vacation_added = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.view.controller = self
        self.view.add_button.clicked.connect(self.add_vacation)
        self.load_employees()
        self.load_vacations()

    def load_employees(self):
        """Loads employee data and populates the view's employee combo box."""
        employees = EmployeeModel.get_all()
        self.view.set_employee_list(employees)

    def load_vacations(self):
        """Loads vacation data and populates the view's table."""
        vacations = VacationModel.get_all_vacations()
        self.view.display_vacations(vacations)

    def add_vacation(self):
        """Gets vacation details from the form and adds a new record to the database."""
        emp_index = self.view.employee_combo.currentIndex()
        if emp_index == -1:
            msg_box = QMessageBox(self.view)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Please select an employee.")
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1f2937;
                    color: #f8fafc;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #374151;
                    color: #f8fafc;
                    padding: 6px 14px;
                    border-radius: 6px;
                    font-weight: 600;
                }
                QPushButton:hover { background-color: #2563eb; }
                QPushButton:pressed { background-color: #1d4ed8; }
            """)
            msg_box.exec_()
            return

        start_date = self.view.start_date_input.date()
        end_date = self.view.end_date_input.date()
        if start_date > end_date:
            msg_box = QMessageBox(
                QMessageBox.Warning,
                "Invalid Dates",
                "The end date cannot be before the start date.",
                QMessageBox.Ok,
                self.view,
            )
            msg_box.button(QMessageBox.Ok).setText("OK")
            msg_box.exec_()
            return

        emp_id = self.view.employee_combo.itemData(emp_index)
        start_date_str = start_date.toString("yyyy-MM-dd")
        end_date_str = end_date.toString("yyyy-MM-dd")

        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
        new_vac_days = (end_dt - start_dt).days + 1

        emp = EmployeeModel.get_by_id(emp_id)
        total_credit = emp["last_year_remaining"] + emp["vacation_credit"]

        vacations = VacationModel.get_all_vacations()
        used_days = 0
        for vac in vacations:
            if vac["employee_id"] == emp_id:
                vac_start = datetime.strptime(vac["start_date"], "%Y-%m-%d")
                vac_end = datetime.strptime(vac["end_date"], "%Y-%m-%d")
                used_days += (vac_end - vac_start).days + 1
        total_used = used_days + new_vac_days

        if total_used > total_credit:
            msg_box = QMessageBox(self.view)
            msg_box.setWindowTitle("Vacation Allowance Exceeded")
            msg_box.setText(
                f"The employee does not have enough vacation allowance.\n"
                f"Total allowance: {total_credit} days\n"
                f"Requested after addition: {total_used} days"
            )
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.button(QMessageBox.Ok).setText("OK")
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1f2937;
                    color: #f8fafc;
                    font-size: 15px;
                }
                QPushButton {
                    background-color: #2563eb;
                    color: #f8fafc;
                    padding: 8px 18px;
                    border-radius: 8px;
                    font-weight: 600;
                }
                QPushButton:hover { background-color: #1d4ed8; }
                QPushButton:pressed { background-color: #1e40af; }
            """)
            msg_box.exec_()
            return

        VacationModel.add(emp_id, start_date_str, end_date_str, "")

        EmployeeModel.update_vacation_used(emp_id, total_used)

        self.load_vacations()
        self.vacation_added.emit()

        if hasattr(self.view, "parent") and hasattr(self.view.parent(), "emp_controller"):
            self.view.parent().emp_controller.load_employees()

    def delete_vacation(self, vac_ids):
        """Deletes one or more vacation requests by ID and reloads the view."""
        VacationModel.delete(vac_ids)
        self.load_vacations()