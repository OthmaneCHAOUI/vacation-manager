from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt5.QtWidgets import QAbstractItemView


class EmployeeView(QWidget):
    """UI for managing employees (form + table)."""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title = QLabel("Employees")
        title.setObjectName("h1")
        layout.addWidget(title)

        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)

        lineedit_style = """
            QLineEdit {
                background-color: #1f2937;
                color: #e5e7eb;
                padding: 6px 10px;
                border: 2px solid #374151;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
                background-color: #111827;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
                font-style: italic;
            }
        """

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First name")
        self.first_name_input.setStyleSheet(lineedit_style)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last name")
        self.last_name_input.setStyleSheet(lineedit_style)

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Job title / Grade")
        self.position_input.setStyleSheet(lineedit_style)

        self.last_year_remaining_input = QLineEdit()
        self.last_year_remaining_input.setPlaceholderText("Carryover days")
        self.last_year_remaining_input.setStyleSheet(lineedit_style)

        self.vacation_credit_input = QLineEdit()
        self.vacation_credit_input.setPlaceholderText("Annual vacation allowance")
        self.vacation_credit_input.setStyleSheet(lineedit_style)

        self.vacation_used_input = QLineEdit()
        self.vacation_used_input.setPlaceholderText("Vacation days used")
        self.vacation_used_input.setStyleSheet(lineedit_style)

        self.add_button = QPushButton("Add Employee")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.setStyleSheet(
            """
            QPushButton {
                background-color: limegreen;
                color: white;
                padding: 6px 16px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1d4ed8; }
            QPushButton:pressed { background-color: #1e40af; }
            """
        )

        form_layout.addWidget(self.first_name_input)
        form_layout.addWidget(self.last_name_input)
        form_layout.addWidget(self.position_input)
        form_layout.addWidget(self.last_year_remaining_input)
        form_layout.addWidget(self.vacation_credit_input)
        form_layout.addWidget(self.vacation_used_input)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            [
                "First Name",
                "Last Name",
                "Job Title / Grade",
                "Carryover Days",
                "Annual Vacation Allowance",
                "Vacation Days Used",
                "Total Allowance",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #0b1220;
                color: #e5e7eb;
                gridline-color: #1f2937;
            }
            QHeaderView::section {
                background-color: #111827;
                color: #f8fafc;
                font-weight: 600;
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #2563eb;
                color: white;
            }
            """
        )
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table, 1)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 6px 16px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:pressed { background-color: #b91c1c; }
            """
        )
        layout.addWidget(self.delete_button)

        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.table.cellChanged.connect(self.on_cell_changed)
        self.add_button.clicked.connect(self.on_add_clicked)

        self.row_to_emp_id = {}

    def load_employees(self, employees):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.row_to_emp_id = {}
        for row, emp in enumerate(employees):
            self.table.insertRow(row)
            self.row_to_emp_id[row] = emp["id"]

            self.table.setItem(row, 0, QTableWidgetItem(emp["first_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(emp["last_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(emp["position"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(emp["last_year_remaining"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(emp["vacation_credit"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(emp["vacation_used"])))

            total_credit = emp["last_year_remaining"] + emp["vacation_credit"]
            item = QTableWidgetItem(str(total_credit))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 6, item)
        self.table.blockSignals(False)

    def confirm_delete(self, count: int) -> bool:
        """Show a confirmation dialog before deleting employees."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(f"Are you sure you want to delete {count} employee(s)?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Yes")
        msg.button(QMessageBox.No).setText("No")
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet(
            """
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
            """
        )
        return msg.exec_() == QMessageBox.Yes

    def on_delete_clicked(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows or not hasattr(self, "row_to_emp_id"):
            return

        if not self.confirm_delete(len(selected_rows)):
            return

        emp_ids = [
            self.row_to_emp_id[row]
            for row in selected_rows
            if row in self.row_to_emp_id
        ]
        if emp_ids:
            for emp_id in emp_ids:
                self.controller.delete_employee(emp_id)

    def on_cell_changed(self, row, column):
        # Only update editable columns (0-5)
        if column == 6:
            return

        if not hasattr(self, "row_to_emp_id"):
            return

        emp_id = self.row_to_emp_id.get(row)
        if emp_id is None:
            return

        def get_text(row, col):
            item = self.table.item(row, col)
            return item.text() if item else ""

        first_name = get_text(row, 0)
        last_name = get_text(row, 1)
        position = get_text(row, 2)
        try:
            last_year_remaining = int(get_text(row, 3))
            vacation_credit = int(get_text(row, 4))
            vacation_used = int(get_text(row, 5))
        except ValueError:
            return

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "position": position,
            "last_year_remaining": last_year_remaining,
            "vacation_credit": vacation_credit,
            "vacation_used": vacation_used,
        }

        self.controller.update_employee(emp_id, data)

    def on_add_clicked(self):
        data = {
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "position": self.position_input.text().strip(),
            "last_year_remaining": int(self.last_year_remaining_input.text() or 0),
            "vacation_credit": int(self.vacation_credit_input.text() or 0),
            "vacation_used": int(self.vacation_used_input.text() or 0),
        }
        if not data["first_name"] or not data["last_name"]:
            msg = QMessageBox(self)
            msg.setWindowTitle("Invalid Input")
            msg.setText("First and last name are required.")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.button(QMessageBox.Ok).setText("OK")
            msg.setStyleSheet(
                """
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
                """
            )
            msg.exec_()
            return
        self.controller.add_employee(data)
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.position_input.clear()
        self.last_year_remaining_input.clear()
        self.vacation_credit_input.clear()
        self.vacation_used_input.clear()
