from datetime import datetime


DATE_FORMAT = "%Y-%m-%d"


def vacation_days(start_date, end_date):
    """Return the inclusive number of days in a vacation interval."""
    start = datetime.strptime(start_date, DATE_FORMAT)
    end = datetime.strptime(end_date, DATE_FORMAT)
    return (end - start).days + 1


def used_vacation_days(vacations):
    """Return the inclusive number of days in existing vacations."""
    return sum(
        vacation_days(vacation["start_date"], vacation["end_date"])
        for vacation in vacations
    )


def total_used_days(vacations, additional_start, additional_end):
    """Return existing and newly requested vacation days combined."""
    return used_vacation_days(vacations) + vacation_days(
        additional_start, additional_end
    )
