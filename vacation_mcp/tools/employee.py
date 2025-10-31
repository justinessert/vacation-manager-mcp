from vacation_mcp.employees import employees
from vacation_mcp.exceptions import InvalidEmployeeNameError
from vacation_mcp.server import server

@server.tool()
def get_employee_id_by_name(employee_name: str) -> str:
    """
    Retrieve the employee ID based on the employee's name.

    Args:
        employee_name (str): The name of the employee.

    Returns:
        str: The ID of the employee.

    Raises:
        InvalidEmployeeNameError: If the employee name does not exist.
    """
    for emp_id, employee in employees.items():
        if employee.name == employee_name:
            return emp_id
    raise InvalidEmployeeNameError(f"Employee with name {employee_name} not found.")