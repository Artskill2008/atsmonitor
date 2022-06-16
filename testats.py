#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
import pymysql
import os
import time
import threading
import logging
import configparser


class Calltel(threading.Thread):

    def __init__(self, number, semaphore: threading.Semaphore):
        super().__init__()
        self.number = number
        self.sem = semaphore
        logger.info('Tel started work')

    def tel_profile(self):
        return ("Channel: SIP/00080655/" + self.number + "\n"
                "Callerid:" + self.number + "\n"
                "MaxRetries: 0\n"
                f"RetryTime: {retrycall}\n"
                f"WaitTime: {waitcall}\n"
                "Context: freepbx\n"
                "Extension:_8XXXXXXXXXX\n"
                "Priority: 1\n")

    def run(self):
        self.call(self.number)
        time.sleep(int(sleep))
        with self.sem:
            print("Ожидание 62 секунды.", self.number)
            request = self.db_conn(self.number)
            callstatus = request[1]
#           callstatus =  'ANSWERED'
            print(self.number, callstatus)
            for i in range(int(dials)):
                if callstatus == 'ANSWERED':
                    self.write_status(callstatus)
                    break
                else:
                    if i == 2:
                        self.write_status(callstatus)
                        break
                    self.call(self.number)
                    time.sleep(int(sleep))
                    callstatus = self.db_conn(self.number)[1]
            logger.info('work from {} complete'.format(self.number))

    def write_status(self, status):
        global tel_status
        self.sem.acquire()
        tel_status.append("number: " + str(self.number) + " status " + str(status))
        self.sem.release()


    def db_conn(self,num_for_request):
        conn = pymysql.connect(host='localhost', user='asterisk', password='PSr730Xg$', db='asterisk')
        cursor = conn.cursor()
        cursor.execute(f"SELECT {num_for_request}, disposition FROM cdr ORDER BY `calldate` DESC limit 1")
        row = cursor.fetchone()  # Получаем данные 1.
        conn.close()
        return row


    def call(self, call_number):
            with open('{}.call'.format(call_number), "w") as my_file:
                my_file.write(self.tel_profile())
            os.system("chown asterisk.asterisk {}.call".format(call_number))
            os.system(f"cp {call_number}.call /etc/zabbix/ast/test/{call_number}control.call")
            os.system(f"mv {call_number}.call /var/spool/asterisk/outgoing/{call_number}.call")



def main():
    semaphore = threading.Semaphore(int(semset))

    with open('numbers.txt', 'r') as numbers:
        for num in numbers:
            tel_ck = Calltel(num.strip(), semaphore=semaphore)
            tel_ck.start()
        tel_ck.join()



startTime = time.time()
conf = configparser.RawConfigParser()
conf.read('testats.conf')
retrycall = conf.get("SETTINGS", "RetryTime")
waitcall = conf.get("SETTINGS", "WaitTime")
sleep = conf.get("SETTINGS", "TimeSleep")
waitlat = conf.get("SETTINGS", "WaitLatecomers")
semset = conf.get("SETTINGS", "Semaphore")
dials = conf.get("SETTINGS", "NumberOfDials")
tel_status = []
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    main()
time.sleep(int(waitlat))
print(tel_status)
with open('report.txt', 'w') as report:
    for line in tel_status:
        report.write(str(line) + "\n")
now = datetime.now()
print(now)
endTime = time.time() #время конца замера
totalTime = endTime - startTime #вычисляем затраченное время
print("Время, затраченное на выполнение данного кода = ", totalTime)
