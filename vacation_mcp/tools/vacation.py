from typing import List

from vacation_mcp.employees import get_employee
from vacation_mcp.exceptions import InsufficientVacationDaysError
from vacation_mcp.server import server


# Get remaining vacation days tool
@server.tool()
def get_remaining_vacation_days(employee_id: str) -> int:
    """
    Get the number of remaining vacation days for an employee.

    Args:
        employee_id (str): The ID of the employee.

    Returns:
        int: The number of vacation days remaining for the employee.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
    """
    employee = get_employee(employee_id)
    return employee.remaning_vacation_days


# Log vacation day tool
@server.tool()
def log_vacation_day(employee_id: str, dates: List[str]) -> str:
    """
    Log vacation days for an employee. Ex: ["2023-04-01", "2023-04-02"]

    Args:
        employee_id (str): The ID of the employee.
        dates (List[str]): A list of dates to log as vacation days.

    Returns:
        str: A confirmation message indicating the number of vacation days logged.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
        InsufficientVacationDaysError: If the employee has no remaining vacation days.
    """
    employee = get_employee(employee_id)
    
    for date in dates:
        if employee.remaning_vacation_days <= 0:
            raise InsufficientVacationDaysError(f"Employee {employee_id} has no remaining vacation days.")
        employee.vacation_history.append(date)
    
    return f"Logged {len(dates)} vacation days for employee {employee_id}."

# Get vacation history tool
@server.tool()
def get_vacation_history(employee_id: str) -> List[str]:
    """
    Retrieve the vacation history for an employee.

    Args:
        employee_id (str): The ID of the employee.

    Returns:
        List[str]: A list of dates representing the employee's vacation history.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
    """
    employee = get_employee(employee_id)
    return employee.vacation_history