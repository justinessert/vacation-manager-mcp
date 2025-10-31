from typing import Dict, List
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

class Employee(BaseModel):
    id: str
    vacation_days_per_year: int
    vacation_history: list

    @property
    def remaning_vacation_days(self) -> int:
        """
        Calculate the remaining vacation days for the employee.

        Returns:
            int: The number of vacation days left for the employee.
        """
        used_days = len(self.vacation_history)
        return self.vacation_days_per_year - used_days

# Invalid Employee ID Error
class InvalidEmployeeIDError(Exception):
    """
    Exception raised when an invalid employee ID is provided.
    """
    pass

# Insufficient Vacation Days Error
class InsufficientVacationDaysError(Exception):
    """
    Exception raised when an employee tries to log vacation days
    but has no remaining vacation days.
    """
    pass

employees: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        vacation_days_per_year=20,
        vacation_history=["2023-01-15", "2023-02-20", "2023-03-10"]
    ),
    "E002": Employee(
        id="E002",
        vacation_days_per_year=15,
        vacation_history=["2023-01-05", "2023-01-25"]
    ),
}

# Create an MCP server
mcp = FastMCP("VacationManager")

def _get_employee(employee_id: str) -> Employee:
    """
    Retrieve an employee object by their ID.

    Args:
        employee_id (str): The ID of the employee to retrieve.

    Returns:
        Employee: The employee object corresponding to the given ID.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
    """
    employee = employees.get(employee_id)
    if not employee:
        raise InvalidEmployeeIDError(f"Employee with ID {employee_id} not found.")
    return employee


# Get remaining vacation days tool
@mcp.tool()
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
    employee = _get_employee(employee_id)
    return employee.remaning_vacation_days


# Log vacation day tool
@mcp.tool()
def log_vacation_day(employee_id: str, dates: List[str]) -> str:
    """
    Log vacation days for an employee.

    Args:
        employee_id (str): The ID of the employee.
        dates (List[str]): A list of dates to log as vacation days.

    Returns:
        str: A confirmation message indicating the number of vacation days logged.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
        InsufficientVacationDaysError: If the employee has no remaining vacation days.
    """
    employee = _get_employee(employee_id)
    
    for date in dates:
        if employee.remaning_vacation_days <= 0:
            raise InsufficientVacationDaysError(f"Employee {employee_id} has no remaining vacation days.")
        employee.vacation_history.append(date)
    
    return f"Logged {len(dates)} vacation days for employee {employee_id}."

# Get vacation history tool
@mcp.tool()
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
    employee = _get_employee(employee_id)
    return employee.vacation_history

# Health check resource
@mcp.resource("health://")
def health_check() -> str:
    """
    Perform a health check for the MCP server.

    Returns:
        str: A string indicating the server is healthy ("OK").
    """
    return "OK"

# Employee greeting resource
@mcp.resource("greet/{employee_id}")
def greet_employee(employee_id: str) -> str:
    """
    Generate a greeting message for an employee.

    Args:
        employee_id (str): The ID of the employee.

    Returns:
        str: A greeting message for the employee.

    Raises:
        InvalidEmployeeIDError: If the employee ID does not exist.
    """
    employee = _get_employee(employee_id)
    return f"Hello, Employee {employee.id}!"


if __name__ == "__main__":
    mcp.run()