from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDateEdit,
    QComboBox,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QDate, QLocale
from PyQt5.QtGui import QColor


class VacationView(QWidget):
    """UI for managing vacations (form + table)."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title = QLabel("Vacations")
        title.setObjectName("h1")
        layout.addWidget(title)

        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)

        self.employee_combo = QComboBox()
        self.employee_combo.setMinimumWidth(150)
        self.employee_combo.setCursor(Qt.PointingHandCursor)
        self.employee_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #1f2937;
                color: #e5e7eb;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #2563eb;
                background-color: #111827;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 2px solid #374151;
                background: #111827;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox::down-arrow {
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: #0b1220;
                color: #f8fafc;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
                border-radius: 8px;
                font-size: 15px;
                padding: 4px 0;
            }
            QComboBox QAbstractItemView::item {
                height: 32px;
                padding-left: 12px;
                border-bottom: 1px solid #374151;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #2563eb;
                color: #ffffff;
            }
            """
        )
        self.employee_combo.setPlaceholderText("Select an employee")

        dateedit_style = """
        QDateEdit {
            background-color: #1f2937;
            color: #e5e7eb;
            border: 2px solid #374151;
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 14px;
        }
        QDateEdit:focus {
            border: 2px solid #2563eb;
            background-color: #111827;
        }
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border-left: 2px solid #374151;
            background: #111827;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }
        QDateEdit::down-arrow {
            width: 16px;
            height: 16px;
        }
        QCalendarWidget QWidget {
            background-color: #111827;
            color: #e5e7eb;
        }
        QCalendarWidget QTableView {
            background-color: #0b1220;
            color: #e5e7eb;
        }
        QCalendarWidget QHeaderView::section {
            background-color: #111827;
            color: #f8fafc;
            font-weight: 600;
        }
        """

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.calendarWidget().setFirstDayOfWeek(Qt.Monday)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setStyleSheet(dateedit_style)
        self.start_date_input.setMinimumWidth(130)
        self.start_date_input.setLocale(QLocale(QLocale.English))
        self.start_date_input.calendarWidget().setLocale(QLocale(QLocale.English))

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.calendarWidget().setFirstDayOfWeek(Qt.Monday)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setStyleSheet(dateedit_style)
        self.end_date_input.setMinimumWidth(130)
        self.end_date_input.setLocale(QLocale(QLocale.English))
        self.end_date_input.calendarWidget().setLocale(QLocale(QLocale.English))

        self.add_button = QPushButton("Add Vacation")
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

        employee_layout = QVBoxLayout()
        employee_layout.addWidget(self.employee_combo)

        start_layout = QVBoxLayout()
        start_layout.addWidget(self.start_date_input)

        end_layout = QVBoxLayout()
        end_layout.addWidget(self.end_date_input)

        form_layout.addLayout(employee_layout)
        form_layout.addLayout(start_layout)
        form_layout.addLayout(end_layout)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Employee", "Start Date", "End Date", "Status", "Created At"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
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
        self.delete_button.clicked.connect(self.on_delete_selected)
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

    def display_vacations(self, vacations):
        """
        Populates the table with vacation data.
        Highlights rows for vacations that ended before today.
        """
        self.table.setRowCount(0)
        self.row_to_vac_id = {}
        today = QDate.currentDate()
        for row, vac in enumerate(vacations):
            self.table.insertRow(row)
            self.table.setItem(
                row, 0, QTableWidgetItem(f"{vac['first_name']} {vac['last_name']}")
            )
            self.table.setItem(row, 1, QTableWidgetItem(vac["start_date"]))
            self.table.setItem(row, 2, QTableWidgetItem(vac["end_date"]))
            self.table.setItem(row, 3, QTableWidgetItem(vac["status"]))
            self.table.setItem(row, 4, QTableWidgetItem(vac["created_at"]))
            self.row_to_vac_id[row] = vac["id"]

            end_date = QDate.fromString(vac["end_date"], "yyyy-MM-dd")
            if end_date < today:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor(100, 100, 100, 80))

    def set_employee_list(self, employees):
        """Fills the employee list dropdown."""
        self.employee_combo.clear()
        for emp in employees:
            self.employee_combo.addItem(
                f"{emp['first_name']} {emp['last_name']}", emp["id"]
            )

    def confirm_delete(self, count: int) -> bool:
        """Show a confirmation dialog before deleting vacation requests."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(f"Are you sure you want to delete {count} vacation request(s)?")
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

    def on_delete_selected(self):
        """Handles the deletion of selected vacation requests."""
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows or not hasattr(self, "row_to_vac_id"):
            return

        if not self.confirm_delete(len(selected_rows)):
            return

        vac_ids = [
            self.row_to_vac_id[row]
            for row in selected_rows
            if row in self.row_to_vac_id
        ]
        if vac_ids:
            self.controller.delete_vacation(vac_ids)
