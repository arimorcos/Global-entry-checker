import goes_checker
import time
import datetime

if __name__ == "__main__":

    checker = goes_checker.check_goes()
    compare_date = datetime.date(2016, 3, 1)

    keep_going = True
    while keep_going:
        new_date = checker.check_new_date()

        # Compare
        delta = (new_date - compare_date).days
        print new_date.strftime('%x')
        if delta < 0:
            msg = "New date found: {}".format(new_date.strftime('%x'))
            checker.send_email(msg)
            keep_going = False
        time.sleep(60)
