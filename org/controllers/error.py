"""Controller Exceptions"""


class UserExist(Exception):
    """"User already exist"""
    def __init__(self, user):
        super().__init__(f"User {user} already exist")


class UserAssignedUnit(Exception):
    """"User already assigned to Unit"""
    def __init__(self, user, unit):
        super().__init__(f"User {user} already assigned to Unit {unit}")


class UnitExist(Exception):
    """"Unit already exist"""
    def __init__(self, unit):
        super().__init__(f"Unit {unit} already exist")


class UserNotFoundError(Exception):
    """User not found"""
    def __init__(self, login):
        super().__init__(f"User {login} not found")
