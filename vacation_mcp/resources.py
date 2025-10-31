from vacation_mcp.employees import _get_employee
from vacation_mcp.server import server


# Health check resource
@server.resource("health://")
def health_check() -> str:
    """
    Perform a health check for the MCP server.

    Returns:
        str: A string indicating the server is healthy ("OK").
    """
    return "OK"

# Employee greeting resource
@server.resource("greet/{employee_id}")
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