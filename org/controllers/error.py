"""Controller Exceptions"""


class UserExist(Exception):
    """"User already exist"""
    def __init__(self, user):
        super().__init__(f"User {user} already exist")


class UserAssignedUnit(Exception):
    """"User already assigned to Unit"""
    def __init__(self, user, unit):
        super().__init__(f"User {user} already assigned to Unit {unit}")


class UserNotFoundError(Exception):
    """User not found"""
    def __init__(self, login):
        super().__init__(f"User {login} not found")


class UnitExist(Exception):
    """"Unit already exist"""
    def __init__(self, unit):
        super().__init__(f"Unit {unit} already exist")


class UnitNotFoundError(Exception):
    """Unit not found"""
    def __init__(self, unit_id):
        super().__init__(f"Unit {unit_id} not found")
