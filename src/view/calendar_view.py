from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget
from PyQt5.QtCore import QDate, QLocale
from PyQt5.QtGui import QTextCharFormat, QColor

class CalendarView(QWidget):
    """
    Calendar view based on QCalendarWidget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget()
        self.calendar.setLocale(QLocale(QLocale.English))
        self.calendar.setDateEditEnabled(False)
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(1)  # Monday
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setSelectedDate(QDate.currentDate())

        layout.addWidget(self.calendar)

        self.load_stylesheet()
        self.highlight_current_day()

    def load_stylesheet(self):
        """Load CSS for calendar styling."""
        try:
            with open("src/style/calendar_style.css", "r", encoding="utf-8") as f:
                self.calendar.setStyleSheet(f.read())
        except FileNotFoundError:
            print("⚠️ Calendar stylesheet not found: src/style/calendar_style.css")

    def get_selected_date(self):
        """Return the selected QDate."""
        return self.calendar.selectedDate()

    def set_min_max_date(self, min_date: QDate, max_date: QDate):
        """Set minimum and maximum selectable dates."""
        self.calendar.setMinimumDate(min_date)
        self.calendar.setMaximumDate(max_date)

    def on_date_changed(self, callback):
        """
        Connect a callback to date selection change.
        Callback must accept a QDate.
        """
        self.calendar.selectionChanged.connect(lambda: callback(self.get_selected_date()))

    def highlight_days(self, qdate_list):
        """Highlight a list of QDate objects in the calendar."""
        self.clear_highlighted_days()
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#9400D3"))
        for qdate in qdate_list:
            if qdate != QDate.currentDate():
                self.calendar.setDateTextFormat(qdate, fmt)
        self.highlight_current_day()

    def clear_highlighted_days(self):
        """Clear all highlighted days except current day."""
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        self.highlight_current_day()

    def highlight_current_day(self):
        """Always highlight the current day in tomato color."""
        current_format = QTextCharFormat()
        current_format.setBackground(QColor("tomato"))
        self.calendar.setDateTextFormat(QDate.currentDate(), current_format)