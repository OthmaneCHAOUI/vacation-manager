from src.database.database import get_connection

class Vacation:
    """ Model for vacation-related data. """
    
    def __init__(self):
        """ default constructor for the VacationModel class. """
        pass

    def __init__(self, id, employee_id, start_date, end_date, reason="", status="pending"):
        """ valued constructor for the VacationModel class. """
        self.__id = id
        self.__employee_id = employee_id
        self.__start_date = start_date
        self.__end_date = end_date
        self.__reason = reason
        self.__status = status

    """ Getters and setters for the VacationModel class attributes. """
    
    def get_id(self):
        return self.__id

    def get_employee_id(self):
        return self.__employee_id

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_reason(self):
        return self.__reason

    def get_status(self):
        return self.__status

    def set_id(self, id):
        self.__id = id

    def set_employee_id(self, employee_id):
        self.__employee_id = employee_id

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def set_reason(self, reason):
        self.__reason = reason

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return f"Vacation(id={self.__id}, employee_id={self.__employee_id}, start_date={self.__start_date}, end_date={self.__end_date}, reason={self.__reason}, status={self.__status})"
    