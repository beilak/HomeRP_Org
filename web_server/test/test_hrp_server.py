import unittest
from fastapi.testclient import TestClient
from fastapi import status
from web_server.hrp_server import hrp_api
import datetime


class HRPWebServerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_user = "TEST_USER1"
        cls.TEST_USER = test_user
        test_unit = "test_unit_id_1"
        cls.TEST_UNIT = test_unit
        cls.TEST_DEBIT_ACC1 = "010203040506070809"
        client = TestClient(hrp_api)
        cls.client = client

        client.post("/users/",
                    json={"login": test_user, "first_name": "First",
                          "last_name": "Last", "password": "TestPass",
                          "email": "test@test.ru"})
        client.post("/units/",
                    json={"unit_id": test_unit, "description": "Unit desc",
                          "admin": test_user,
                          "join_pass": "UnitTestPass"})
        client.put("/users/{}/join_to_unit".format(test_user),
                   json={"login": test_user,
                         "unit_id": test_unit})

    def test_get_users(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        link = "/users/{}".format(self.TEST_USER)
        response = self.client.get(link)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_login = response.json()['login']
        self.assertEqual(response_login, self.TEST_USER)

    def test_create_user(self):
        new_user_login = "TEST_USR_WEB_{}".format(str(datetime.datetime.now().hour) +
                                                  str(datetime.datetime.now().minute) +
                                                  str(datetime.datetime.now().microsecond))
        response = self.client.post("/users/",
                                    json={"login": new_user_login, "first_name": "First",
                                          "last_name": "Last", "password": "TestPass",
                                          "email": "test@test.ru"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.text)
        response_login = response.json()['login']
        self.assertEqual(response_login, new_user_login)

    def test_update_user(self):
        # ToDo Add test after implemented service method
        pass

    def test_create_unit(self):
        new_unit_id = "TEST_UNIT{}".format(str(datetime.datetime.now().hour) +
                                           str(datetime.datetime.now().minute) +
                                           str(datetime.datetime.now().microsecond))
        response = self.client.post("/units/",
                                    json={"unit_id": new_unit_id, "description": "Unit desc",
                                          "admin": self.TEST_USER,
                                          "join_pass": "UnitTestPass"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.text)
        response_unit_id = response.json()['unit_id']
        self.assertEqual(response_unit_id, new_unit_id)

    def test_get_units(self):
        response = self.client.get("/units/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unit(self):
        response = self.client.get("/units/{}".format(self.TEST_UNIT))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_unit_id = response.json()["unit_id"]
        self.assertEqual(response_unit_id, self.TEST_UNIT)

    def test_user_join_to_unit(self):
        new_unit_id = "TEST_UNIT{}".format(str(datetime.datetime.now().hour) +
                                           str(datetime.datetime.now().minute) +
                                           str(datetime.datetime.now().microsecond))
        response = self.client.post("/units/",
                                    json={"unit_id": new_unit_id, "description": "Unit desc",
                                          "admin": self.TEST_USER,
                                          "join_pass": "UnitTestPass"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.text)
        response_unit_id = response.json()['unit_id']

        response = self.client.put("/users/{}/join_to_unit".format(self.TEST_USER),
                                   json={"login": self.TEST_USER,
                                         "unit_id": response_unit_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.text)
        response_login = response.json()["login"]
        self.assertEqual(response_login, self.TEST_USER)
        is_unit_joined = False
        for item in response.json()["units"]:
            if new_unit_id == item["unit_id"]:
                is_unit_joined = True
                break
        self.assertTrue(is_unit_joined)

    def test_get_unit_users(self):
        response = self.client.get("/units/{}/users".format(self.TEST_UNIT))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.text)

    def test_create_debit_acc(self):
        response = self.client.post("/units/" + self.TEST_UNIT + "/account",
                                    json={"acc_number": self.TEST_DEBIT_ACC1,
                                          "unit_id": self.TEST_UNIT,
                                          "user_login": self.TEST_USER,
                                          "acc_type": "DEBIT_CARD",
                                          "description": "Зарплатная карта",
                                          "bank": "Тенькофф"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.text)
        response_acc_num = response.json()['acc_number']
        self.assertEqual(response_acc_num, self.TEST_DEBIT_ACC1)
        response_acc_id = response.json()['acc_id']
        self.assertIsNotNone(response_acc_id)

    def test_create_chase_acc(self):
        response = self.client.post("/units/" + self.TEST_UNIT + "/account",
                                    json={"unit_id": self.TEST_UNIT,
                                          "user_login": self.TEST_USER,
                                          "acc_type": "CHASE",
                                          "description": "Наличка",
                                          "bank": "Тенькофф"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.text)
        response_acc_num = response.json()['acc_number']
        self.assertIsNone(response_acc_num)
        response_acc_id = response.json()['acc_id']
        self.assertIsNotNone(response_acc_id)


def test_get_accounts(self):
    # ToDo
    self.assertTrue(False)


def get_accounts(self):
    # ToDo
    self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
