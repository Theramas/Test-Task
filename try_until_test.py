import logging
import unittest
from unittest.mock import MagicMock
import task_for_set_vacancy

# 1. Support code

# Default arguments

logging.basicConfig(level=logging.DEBUG)
task_for_set_vacancy.LOG = logging.getLogger(__name__)
task_for_set_vacancy.GLOBAL_TIMEOUT = 3

# Exceptions

task_for_set_vacancy.exc = MagicMock()
task_for_set_vacancy.exc.TryAgainError = ValueError
task_for_set_vacancy.exc.UserTimeoutError = SyntaxError
task_for_set_vacancy.exc.Error = Exception

# Test functions for calling

def func1():
    return 13

def func2():
    raise task_for_set_vacancy.exc.TryAgainError('Try again.')

def func4():
    raise task_for_set_vacancy.exc.Error('Error')

# 2. Test case

class TestTryUntilFunc(unittest.TestCase):

    # Checks that if called function returns any result, try_until stops and
    # returns this result
    def test_return_value(self):
        result = task_for_set_vacancy.try_until(func1)
        self.assertTrue(result == 13)

    # Checks that errors and exceptions (except the 'exc.TryAgainError')
    # are captured correctly
    def test_error(self):
        with self.assertRaisesRegex(Exception, 'Try-until for {0} failed: got error: Error'.format(func4)):
            task_for_set_vacancy.try_until(func4)

    # Checks that upon exceeding the specified amount of calls the correct
    # exception is raised
    def test_exceed_times(self):
        with self.assertRaisesRegex(Exception, 'Try-until for {0} failed: call count 2 times exceeded'.format(func2)):
            task_for_set_vacancy.try_until(func2, times=2)

    # Checks that try_until repeats call function when exc.TryAgainError is
    # raised AND that correct exception is raised upon exceeding timeout
    def test_exceed_timeout(self):
        with self.assertRaisesRegex(Exception, 'Try-until for {0} failed: timeout 3 seconds exceeded'.format(func2)):
            task_for_set_vacancy.try_until(func2)

    # Checks that try_until returns correct output upon calling it with
    # user-defined arguments
    def test_user_input(self):
        with self.assertRaisesRegex(Exception, 'Try-until for {0} failed: timeout 6 seconds exceeded'.format(func2)):
            task_for_set_vacancy.try_until(func2,try_msg='Trying',log=logging.getLogger(__name__),interval=2,timeout=6)
        with self.assertRaisesRegex(Exception, 'An error: got error: Error'.format(func4)):
            task_for_set_vacancy.try_until(func4, error_msg='An error')

    # Checks that code reacts correctly to the wrong user input
    def test_wrong_arguments(self):
        with self.assertRaises(Exception):
            task_for_set_vacancy.try_until(1)
        with self.assertRaisesRegex(Exception, "'int' object has no attribute 'info'"):
            task_for_set_vacancy.try_until(func2,log=1)
        with self.assertRaisesRegex(Exception, "Unknown format code 'f' for object of type 'str'"):
            task_for_set_vacancy.try_until(func2,interval='M')
        with self.assertRaises(TypeError):
            task_for_set_vacancy.try_until(func2,timeout='M')
        with self.assertRaises(TypeError):
            task_for_set_vacancy.try_until(func2,times='M')

if __name__ == '__main__':
    unittest.main() 