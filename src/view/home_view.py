from pathlib import Path
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QShortcut,
    QComboBox,
)
from src.view.employee_view import EmployeeView
from src.controller.employee_controller import EmployeeController
from src.model.vacation_model import VacationModel
from src.view.calendar_view import CalendarView
from src.controller.vacation_controller import VacationController
from src.view.vacation_view import VacationView


class HomeView(QMainWindow):
    """Main window with a fixed sidebar and stacked pages."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workless - Vacation Manager")
        self.resize(1100, 700)
        self.showMaximized()

        shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut.activated.connect(self.close)

        self.project_root = Path(__file__).resolve().parents[2]
        icon_path = self.project_root / "assets" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._build_ui()
        self._load_stylesheet()

    def _load_stylesheet(self):
        css_path = self.project_root / "src" / "style" / "home_style.css"
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"⚠️ Stylesheet not found: {css_path}")

    def _build_ui(self):
        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.page_employees = EmployeeView()
        self.emp_controller = EmployeeController(self.page_employees, self)
        self.emp_controller.load_employees()

        self.sidebar = self._create_sidebar()
        self.sidebar.setFixedWidth(150)
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.page_home = self._make_home_page()
        self.page_vacations = VacationView(controller=None)
        self.vac_controller = VacationController(self.page_vacations)

        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_employees)
        self.stack.addWidget(self.page_vacations)

        self.setCentralWidget(central)

    def _create_sidebar(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        logo_path = self.project_root / "assets" / "icon.png"
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        if logo_path.exists():
            pix = QPixmap(str(logo_path))
            logo.setPixmap(pix.scaledToWidth(100, Qt.SmoothTransformation))
        else:
            logo.setText("Workless")
            logo.setStyleSheet("font-weight: 600; font-size: 18px;")

        layout.addWidget(logo)

        self.btn_home = QPushButton("Home")
        self.btn_employees = QPushButton("Employees")
        self.btn_vacations = QPushButton("Vacations")

        for btn in [self.btn_home, self.btn_employees, self.btn_vacations]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(btn)

        layout.addStretch(1)

        self.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_employees.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_vacations.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.insertWidget(1, sep)

        return panel

    def _make_home_page(self) -> QWidget:
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)

        title = QLabel("Company Vacation Calendar")
        title.setObjectName("h1")

        self.combo_vacation_employees = QComboBox()
        self.combo_vacation_employees.setPlaceholderText("Employees on vacation")
        self.combo_vacation_employees.setCursor(Qt.PointingHandCursor)
        self.combo_vacation_employees.setStyleSheet(
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

        self.calendar = CalendarView()

        self._update_vacation_employees_combo()
        self.combo_vacation_employees.currentIndexChanged.connect(self._highlight_employee_vacation)

        v.addWidget(title)
        v.addWidget(self.combo_vacation_employees)
        v.addWidget(self.calendar, 1)
        return page

    def _update_vacation_employees_combo(self):
        """Fill combo with all employees who have at least one vacation."""
        self.combo_vacation_employees.clear()
        try:
            employees = VacationModel.get_all_employees_with_vacation()
        except Exception:
            employees = []
        if employees:
            for emp in employees:
                self.combo_vacation_employees.addItem(emp)
        else:
            self.combo_vacation_employees.addItem("No employees on vacation")

    def _highlight_employee_vacation(self):
        """Highlight the latest vacation days of the selected employee in the calendar."""
        emp_name = self.combo_vacation_employees.currentText()
        if not emp_name or emp_name == "No employees on vacation":
            self.calendar.clear_highlighted_days()
            return

        vacations = VacationModel.get_vacations_for_employee_by_name(emp_name)
        if not vacations:
            return

        latest_vacation = max(vacations, key=lambda v: v["created_at"])
        start = QDate.fromString(latest_vacation["start_date"], "yyyy-MM-dd")
        end = QDate.fromString(latest_vacation["end_date"], "yyyy-MM-dd")
        highlighted_dates = []
        d = QDate(start)
        while d <= end:
            highlighted_dates.append(QDate(d))
            d = d.addDays(1)
        self.calendar.highlight_days(highlighted_dates)
        self.calendar.calendar.setSelectedDate(start)

    def refresh_vacation_employees(self):
        """Call this after employee/vacation changes to update the vacation employees list."""
        self._update_vacation_employees_combo()
        current_emp = self.combo_vacation_employees.currentText()
        if current_emp:
            index = self.combo_vacation_employees.findText(current_emp)
            self.combo_vacation_employees.setCurrentIndex(index)

    def closeEvent(self, event):
        """Override close event to perform any cleanup if needed."""
        event.accept()
