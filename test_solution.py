import mysql.connector
import unittest
import datetime
from decimal import Decimal

from solution import (
    get_current_date,
    get_connection,
    get_budgets,
    show_message,
    insert_notified_and_show_message
    )


class TestShopAnalyzerg(unittest.TestCase):
    """
    The class with test methods for every part of solution
    """

    def test_get_current_date(self):
        """
        unit test of function get_current_date
        """

        expected_current_month = datetime.datetime.today().strftime('%Y-%m') + '-1'
        expected_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        current_date, current_month = get_current_date()
        self.assertEqual(expected_current_month, current_month, "should be equal")
        self.assertEqual(expected_current_date, current_date, "should be equal")

    def test_get_budgets(self):
        """
        unit test of function test_get_budgets
        """

        expected_budgets = (
            (1, 'Steve McQueen', Decimal('803.67'), Decimal('960.00'), datetime.date(2020, 7, 1), '50%'),
            (5, 'Meow Meow', Decimal('505.12'), Decimal('870.00'), datetime.date(2020, 7, 1), '50%'),
            (7, 'George Manly', Decimal('805.15'), Decimal('990.00'), datetime.date(2020, 7, 1), '50%')
            )
        cnx = get_connection()
        current_month = '2020-07-01'
        budgets = get_budgets(cnx, current_month)
        budgets = tuple(budgets)
        
        cnx.close()
        self.assertEqual(expected_budgets, budgets, "should be equal")
    
        
class TestConnection(unittest.TestCase):
    """Oracle MySQL for Connector tests"""

    cnx = None

    def setUp(self):
        """
        setting up the database connection
        """
        self.cnx = mysql.connector.connect(user = 'username', password = 'password', host = 'hostaddress', database = 'databasename')

    def tearDown(self):
        """
        test the connection
        closing the database connection
        """
        if self.cnx is not None and self.cnx.is_connected():
            self.cnx.close()

    def test_connection(self):
        self.assertTrue(self.cnx.is_connected())
    
    def test_get_connection(self):

        self.cnx = get_connection()
        self.assertIsNotNone(self.cnx)
        self.cnx.close()

#TODO: testing the show_message

#TODO: testing insert_notified_and_show_message

#TODO: functional test of add 50 then 50 and then 100 with help of test table and then aborting it


if __name__ == '__main__':
    unittest.main()