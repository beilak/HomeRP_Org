import datetime
import unittest

from org.db_schemas.db_unit import Unit
from org.controllers.unit import UnitFactory
from org.org import UnitIn


class UnitTest(unittest.TestCase):
    TEST_UNITS = dict(test_unit_1=UnitIn(unit_id="test_unit_id_1", description="TEST UNIT",
                                         admin="TEST_USER1", join_pass="MyJoinPass"))

    @classmethod
    def setUpClass(cls):
        test_unit = cls.TEST_UNITS["test_unit_1"]
        if UnitFactory.is_unit_exist(test_unit.unit_id) is False:
            UnitFactory.create(test_unit)

    def test_create_unit(self):
        test_unit = self.TEST_UNITS["test_unit_1"]

        while True:
            test_unit.unit_id = "test_unit_id{}".format(str(datetime.datetime.now().microsecond))
            if UnitFactory.is_unit_exist(test_unit.unit_id) is True:
                continue
            break
        unit: Unit = UnitFactory.create(test_unit)
        is_created = False if unit is None else True
        self.assertEqual(is_created, True)


if __name__ == '__main__':
    unittest.main()
