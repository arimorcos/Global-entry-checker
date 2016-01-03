import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime


class check_goes:
    """
    Checks the global online entry system to find out if an earlier date is available
    """

    def __init__(self, user_info_path='user_info.txt',
                 email_info_path='email_info.txt', loc_index=8):

        # load user info
        self.load_user_info(user_info_path)

        # load email info
        self.load_email_info(email_info_path)

        # Initialize website
        self.goes_site = 'https://goes-app.cbp.dhs.gov/main/goes'
        self.location_index = loc_index

    def load_user_info(self, path):
        """
        Loads the user info from the text file stored in the path
        :param path: path to user info file
        """

        with open(path, 'r') as f:
            self.username = f.readline().replace('\n', '')
            self.password = f.readline().replace('\n', '')

    def load_email_info(self, path):
        """
        Loads the email info from the text file stored in the path
        :param path: path to user info file
        """

        with open(path, 'r') as f:
            self.email_username = f.readline().replace('\n', '')
            self.email_password = f.readline().replace('\n', '')

    def send_email(self, content='test'):
        """
        Sends an email using provided info through gmail
        :param content: string containing the message to send
        :return:
        """

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_username, self.email_password)

        # Create message
        msg = MIMEMultipart()
        msg['From'] = 'GOES Checker'
        msg['To'] = self.email_username
        msg['Subject'] = 'New date available'
        msg.attach(MIMEText(content, 'plain'))

        server.sendmail(self.email_username, self.email_username, msg.as_string())
        server.quit()

    def check_new_date(self):
        """
        Navigates to the GOES website and checks the newest date available
        :return: date format of the newest available date
        """

        # Initialize driver and go to site
        driver = webdriver.Firefox()
        driver.get(self.goes_site)

        # Get login fields
        user_field = driver.find_element_by_xpath('//*[@id="user"]')
        pass_field = driver.find_element_by_xpath('//*[@id="password"]')

        # Fill in and submit
        user_field.send_keys(self.username)
        pass_field.send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="SignIn"]').click()

        # Enter
        driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/p[5]/a[2]').click()

        # Manage appointment
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/div/div[5]/table/tbody/tr[2]/td['
                                     '6]/input').click()

        # Reschedule appointment
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/div/div[2]/input[2]').click()

        # Get dropdown and select appropriate index
        dropdown = Select(driver.find_element_by_xpath('//*[@id="selectedEnrollmentCenter"]'))
        dropdown.select_by_index(self.location_index)
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/div/div/input[2]').click()

        # Now, get the current month
        month_year = driver.find_element_by_xpath(
            '//*[@id="scheduleForm"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]'
        ).text
        month, year = month_year.split()
        month = self.convert_month(month)

        # Get current day
        day = driver.find_element_by_xpath(
            '//*[@class="currentDayCell"]/a/span'
        ).text

        # Close website
        driver.close()

        # Create datetime object
        return datetime.date(int(year), int(month), int(day))

    def convert_month(self, month):
        """
        Converts string month to integer
        :param month: string of month
        :return: integer representation of month
        """

        month = month.lower()
        if month == "january":
            return 1
        elif month == "february":
            return 2
        elif month == "march":
            return 3
        elif month == "april":
            return 4
        elif month == "may":
            return 5
        elif month == "june":
            return 6
        elif month == "july":
            return 7
        elif month == "august":
            return 8
        elif month == "september":
            return 9
        elif month == "october":
            return 10
        elif month == "november":
            return 11
        elif month == "december":
            return 12
        else:
            raise BaseException("Can''t process month")





