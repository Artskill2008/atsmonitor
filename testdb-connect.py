#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb

tel = 88007700022

conn = MySQLdb.connect('localhost', 'asterisk', 'PSr730Xg$', 'asterisk')
cursor = conn.cursor()
#cursor.execute("SELECT src, disposition FROM cdr ORDER BY `calldate` DESC limit 1")  # Zapros k bd 1
#cursor.execute("SELECT src, disposition FROM cdr ORDER BY `src`, `calldate` DESC limit 1")
cursor.execute("SELECT {}, disposition FROM cdr ORDER BY `calldate` DESC limit 1".format(tel))

row = cursor.fetchone()  # Получаем данные 1.
tel = row[0]
callstatus = row[1]
print(row, tel, callstatus)
print(tel, callstatus)

