import logging
import time
import sys

def try_until(func, try_msg=None, error_msg=None, log=None, interval=1, timeout=None, times=None):
    """
    repeat call func while it raises exc.TryAgainError
    return last call value 
    raises exc.UserTimeoutError if timeout expired or call times reached
    """
    log = log or LOG
    timeout = timeout or GLOBAL_TIMEOUT
    begin_msg = 'Try-until {0} (timeout: {1} interval: {2} times: {3})'.format(
                func, timeout, interval, times or 'unlimited')
    try_msg = try_msg or 'Trying {0}'.format(func)
    error_msg = error_msg or 'Try-until for {0} failed'.format(func)

    num = 1
    start_time = time.time()
    log.info(begin_msg)
    while True:
        log.debug(try_msg + ' ({0}) ...')
        try:
            result = func()
            if result:
                return result
        except:
            msg = '{0}: got error: {1}'.format(error_msg, sys.exc_info()[1])
            e = exc.Error(msg)
            e.__traceback__ = sys.exc_info()[2]
            raise e
        else:
            if time.time() - start_time > timeout:
                msg = '{0}: timeout {1} seconds exceeded'.format(error_msg, timeout)
                raise exc.UserTimeoutError(msg)
            if times and num >= times:
                msg = '{0}: call count {1} times exceeded'.format(error_msg, times)
                raise exc.UserTimeoutError(msg)

        log.debug("Wait {:.2f} seconds before the next attempt".format(interval))
        time.sleep(interval)
        num += 1
        