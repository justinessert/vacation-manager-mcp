from typing import Dict
from pydantic import BaseModel
from vacation_mcp.exceptions import InvalidEmployeeIDError

class Employee(BaseModel):
    id: str
    name: str
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

employees: Dict[str, Employee] = {
    "E001": Employee(
        id="E001",
        name="Alice Smith",
        vacation_days_per_year=20,
        vacation_history=["2023-01-15", "2023-02-20", "2023-03-10"]
    ),
    "E002": Employee(
        id="E002",
        name="Bob Johnson",
        vacation_days_per_year=15,
        vacation_history=["2023-01-05", "2023-01-25"]
    ),
}

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