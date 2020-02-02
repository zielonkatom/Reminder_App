

from selenium import webdriver
from time import sleep
import smtplib
# hidden data in other file app_pass
from app_pass import email_login, email_pass, URL
from datetime import datetime


class AnimeReminder:
    def __init__(self):
        self.webdriver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.webdriver.get(URL)

        sleep(5)

    def get_list_of_objects(self):
        list_of_objects = self.webdriver.find_element_by_xpath('//*[@id="app"]/section[1]/div/div[2]/div').text
        self.webdriver.quit()
        return list_of_objects.split("\n")

    def prepare_message(self, list_of_objects):
        message = """
Hi there!

This is an updated list for today:

"""
        store_objects = """"""
        for i in range(0, len(list_of_objects), 3):
            if (i + 1) % 3 == 0:
                continue
            store_objects = store_objects + (list_of_objects[i] + " - " + list_of_objects[i + 1] + "\n")

        message = message + store_objects + """

""" + URL + """

Have a nice day!

"""
        return message

    def send_email(self, message):

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_login, email_pass)

        smtp_server.sendmail(email_login, email_login,
                             'Subject: AnimeReminder - ' + datetime.now().strftime("%d/%m/%Y") + '\n' +
                             message.encode('ascii', 'ignore').decode('ascii'))

        smtp_server.quit()
        print("Message successfully sent - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ".")


def remind_me():
    bot = AnimeReminder()
    objects_list = bot.get_list_of_objects()
    message = bot.prepare_message(objects_list)
    bot.send_email(message)


if __name__ == "__main__":
    while True:
        try:
            remind_me()
            sleep(86400)
        except Exception as ex:
            print("Failed " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print(ex)
