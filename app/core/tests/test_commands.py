"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycop2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') #replace the check method of the Command class with a mock object
class CommandTest(SimpleTestCase):
    """Test commands."""
    
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True #indicates that when the check method is called, it will return True, simulating a ready database.

        call_command('wait_for_db') #simulates calling the wait_for_db command.

        patched_check.assert_called_once_with(databases=['default']) #checks that the check method was called exactly once with the specified argument (database=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycop2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])