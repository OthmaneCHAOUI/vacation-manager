from src.database.database import get_connection

class Employee:
    """ Model for employee-related data. """    

    def __init__(self):
        """Default constructor for the EmployeeModel class."""
        pass

    def __init__(self, id, first_name, last_name, position, vacation_credit=22, last_year_remaining=0, vacation_used=0):
        """Valued constructor for the EmployeeModel class."""
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__position = position
        self.__vacation_credit = vacation_credit
        self.__last_year_remaining = last_year_remaining
        self.__vacation_used = vacation_used

    """ Getters and setters for the EmployeeModel class attributes."""

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_vacation_credit(self):
        return self.__vacation_credit

    def set_vacation_credit(self, vacation_credit):
        self.__vacation_credit = vacation_credit

    def get_last_year_remaining(self):
        return self.__last_year_remaining

    def set_last_year_remaining(self, last_year_remaining):
        self.__last_year_remaining = last_year_remaining

    def get_vacation_used(self):
        return self.__vacation_used

    def set_vacation_used(self, vacation_used):
        self.__vacation_used = vacation_used

    def __str__(self):
        return f"EmployeeModel(id={self.__id}, first_name={self.__first_name}, last_name={self.__last_name}, position={self.__position}, vacation_credit={self.__vacation_credit}, last_year_remaining={self.__last_year_remaining}, vacation_used={self.__vacation_used})"
