# Invalid Employee ID Error
class InvalidEmployeeIDError(Exception):
    """
    Exception raised when an invalid employee ID is provided.
    """

# Insufficient Vacation Days Error
class InsufficientVacationDaysError(Exception):
    """
    Exception raised when an employee tries to log vacation days
    but has no remaining vacation days.
    """

# Invalid Employee Name Error
class InvalidEmployeeNameError(Exception):
    """
    Exception raised when an invalid employee name is provided.
    """