#Test task for Python vacancy

#Overview

Test task requires to cover the given code under test with test case written in Python3 standard library 'unittest'. It is also needed to find and point to any inconsistencies between the code and the specifications. This project is a completed test task for a vacancy. It consists of three files:

 - 'task_for_set_vacancy.py' is the code under test; 
 - 'try_until_test.py' is  the test case done with Python3 unittest library; 
 - 'try_until_fixed.py' is the additional file which represents the fixed version of the tested code

#The code under test

The given code is a function 'try_until' which is a part of a bigger project. The function takes one arbitrary argument 'func' (which is a certain unspecified function), one predefined argument 'interval' and a set of optional arguments.  Based on the provided specifications and the logic of the code itself, the function should produce the next results:

 - continuously call the 'func' function while is raises unspecified 'exc.TryAgainError' exception
 - if the call of the 'func' produces any results, it should returns these results and stop iterations
 - if the given timeout is expired it should raise the 'exc.UserTimeoutError' exception
 - if the optional argument 'times' is given, 'func' will be called a specified number of times. If the amout of call     times is exceeded the 'exc.UserTimeoutError' exception will be raised

The function also provides logging of certain messages, some of which can be defined by user via optional arguments 'try_msg' and 'error_msg'. 

#Specification inconsistencies 

There are certain amount of inconsistencies found between the specifications and the actual code. 
The first part 'repeat call func while it raises exc.TryAgainError' indicates that the 'func' should be repeated only when it raises exc.TryAgainError exception. However, given code has only one 'except' clause which will catch all raised exceptions and stop iterations. The 'func' will be called again only if it did not raise any exception and did not return any result.  

One way to meet the specified requirements is to move the code

    log.debug("Wait {:.2f} seconds before the next attempt".format(interval))
        time.sleep(interval)
        num += 1

into an additional except clause 'except exc.TryAgainError'.  The 'else' block from the original should also be moved inside this new except clause. 

Line 22 contains a string with a {0} part, but no '.format' method is given. The unformatted string contains no actual information and is meaningless. Logically, it should contain '.format(num)'. It will format the string with the current repeat number and will show in the log message how many times 'func' was called. 
Fixes of these and some minor grammar errors are represented in 'try_until_fixed.py'.

#Test Plan

The correct code should provide four different outcomes, as shown in specification. So the main four test scenarios would be:
 - check that 'try_until' return result of the 'func', if it was produced
 - check if 'func' raised any exception rather than exc.TryAgainError,  'try_until' raises the custom exception           exc.Error
 - check if repeat times exceeded, 'try_until' raises exc.UserTimeoutError with specific message
 - check if timeout exceeded, 'try_until' raises exc.UserTimeoutError with specific message

Also, function provides opportunity for user to specify his own input by optional arguments. The function should behave properly when correct and incorrect user input is given. Therefore, two additional scenarios should be tested:
 - check that 'try_until' returns proper output with correct optional user input passed
 - check that 'try_until' returns proper output with incorrect optional user input passed

All of these scenarios are covered in 'try_until_test.py' test case. 



