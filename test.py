from datetime import datetime
import MySQLdb
import os
import time


class Calltel:

    def __init__(self, number):
        self.number = number

    def tel_profile(self):
        return ("Channel: SIP/00080655/" + self.number + "\n"
                "Callerid:" + self.number + "\n"
                "MaxRetries: 0\n"
                "RetryTime: 60\n"
                "WaitTime: 60\n"
                "Context: freepbx\n"
                "Extension:_8XXXXXXXXXX\n"
                "Priority: 1\n")

    def check_tel(self):
        with open("venv/1.call", "w") as my_file:
            my_file.write(self.tel_profile())
        os.system("chown asterisk.asterisk 1.call")
        os.system("cp 1.call /etc/zabbix/ast/test.call")
        os.system("mv 1.call /var/spool/asterisk/outgoing/1.call")
        time.sleep(30)
        print("Первый 30 секунд.", self.number)
        conn = MySQLdb.connect('localhost', 'asterisk', 'PSr730Xg$', 'asterisk')
        cursor = conn.cursor()
        cursor.execute("SELECT src, disposition FROM cdr ORDER BY `calldate` DESC limit 1")  # Zapros k bd 1
        row = cursor.fetchone()  # Получаем данные 1.
        tel = row[0]
        callstatus = row[1]
        print(tel, callstatus)
        conn.close()
        return callstatus


def tel(number):
    for i in range(3):
        tel = Calltel(number)
        callstatus = tel.check_tel()
        if callstatus == ('ANSWERED'):
            with open('report.txt', 'a') as report:
                report.write("number: " + tel + " status " + callstatus)
                break


with open('numbers.txt', 'r') as numbers:
    for num in numbers:
        tel(num)
now = datetime.now()
print(now)

