import datetime
import unittest

from org.db_schemas.db_user import User
from org.controllers.unit import UnitFactory
from models.org.user import UserFactory
from org.org import UnitIn
from models.org.valid_schemas.user_valid import UserIn


class UserTest(unittest.TestCase):
    TEST_USERS = dict(test_user_1=UserIn(login="TEST_USER1", first_name="Test_name",
                                         last_name="Test_last_name", password="MyPass",
                                         email="test_user@test.ru"))
    TEST_UNITS = dict(test_unit_1=UnitIn(unit_id="test_unit_id_1", description="TEST UNIT",
                                         admin="TEST_USER1", join_pass="MyJoinPass"))

    def __init__(self, *args, **kwargs):
        super(UserTest, self).__init__(*args, **kwargs)
        self.created_user = set()

    @classmethod
    def setUpClass(cls):
        test_user_1 = cls.TEST_USERS["test_user_1"]
        if UserFactory.is_user_exist(test_user_1.login) is False:
            UserFactory.create(test_user_1)

    def test_creating_user(self):
        test_user_1 = self.TEST_USERS["test_user_1"]

        while True:
            test_user_1.login = "test_user_{}".format(str(datetime.datetime.now().microsecond))
            if UserFactory.is_user_exist(test_user_1.login) is True:
                continue
            break

        user: User = UserFactory.create(cr_user=test_user_1)
        if User is not None:
            self.created_user.add(User)

        is_user_created = False if user is None else True
        self.assertEqual(is_user_created, True)  # add assertion here

    def test_get_user(self):
        user: User = UserFactory.get_user(self.TEST_USERS["test_user_1"].login)
        is_user_found = False if user is None else True
        self.assertEqual(is_user_found, True)  # add assertion here

    def test_join_to_unit(self):
        test_user_1 = self.TEST_USERS["test_user_1"]
        test_unit_1 = self.TEST_UNITS["test_unit_1"]
        test_unit = UnitFactory.get_unit(test_unit_1.unit_id)
        user = UserFactory.join_to_unit(test_user_1.login, test_unit)
        is_joined = False
        for unit in user.units:
            if unit.unit_id == test_unit_1.unit_id:
                is_joined = True
                break
        self.assertTrue(is_joined, msg="User {} didn't join to Unit {}".
                        format(test_user_1.login,
                               test_unit_1.unit_id))

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
