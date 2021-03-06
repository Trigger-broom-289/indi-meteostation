#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# INDUINO METEOSTATION
# http://induino.wordpress.com
#
# NACHO MAS 2013

import urllib
import urllib.request
import urllib.parse
import tidy
import datetime
import time
import locale
from string import *
from meteoconfig import *


class uwyoClass:
    YEAR = ""
    MONTH = ""
    FROM = ""

    def __init__(self):
        pass

    def __init__(self, date_time):
        self.set_date(date_time)

    def set_date(self, date_time):
        self.YEAR = datetime.datetime.strftime(date_time, "%Y")
        self.MONTH = datetime.datetime.strftime(date_time, "%m")
        if (date_time.hour > 13):
            self.FROM = datetime.datetime.strftime(date_time, "%d")+"12"
        else:
            self.FROM = datetime.datetime.strftime(date_time, "%d")+"00"
        print(self.YEAR, self.MONTH, self.FROM)

    def get_sounding_skewt(self):
        data = urllib.parse.urlencode({"region": "europe", "TYPE": "GIF:SKEWT", "YEAR": self.YEAR,
                                       "MONTH": self.MONTH, "FROM": self.FROM, "TO": self.FROM, "STNM": SOUNDINGSTATION}).encode("utf-8")

        # print data
        s = urllib.request.urlopen(
            "http://weather.uwyo.edu/cgi-bin/sounding?", data)
        o = s.read()
        s.close()
        document = tidy.parseString(o)
        urllib.request.urlretrieve("http://weather.uwyo.edu/upperair/images/"+self.YEAR +
                           self.MONTH+self.FROM+".10548.skewt.parc.gif", CHARTPATH+"skewt.gif")
#        print("URL =", urlib)
        # print document

    def get_sounding_data(self):
        data = urllib.parse.urlencode({"region": "europe", "TYPE": "TEXT:LIST", "YEAR": self.YEAR,
                                       "MONTH": self.MONTH, "FROM": self.FROM, "TO": self.FROM, "STNM": SOUNDINGSTATION}).encode("utf-8")
        # print data
        s = urllib.request.urlopen(
            "http://weather.uwyo.edu/cgi-bin/sounding?", data)
        o = s.read()
        s.close()
        document = tidy.parseString(o)
        fi = open(CHARTPATH+"sounding.html", "w")
        fi.write(str(document))
        fi.close()


if __name__ == '__main__':
    print("Starting internet data downloader")
    try:
        print("Retrieving SKEW-T diagrams from:", SOUNDINGSTATION)
    except:
        print("NO sounding station define in meteoconfig.py")
        exit(0)

    while (True):
        today = datetime.datetime.utcnow()
        s = uwyoClass(today)
        try:
            s.get_sounding_skewt()
            s.get_sounding_data()
            urllib.request.urlretrieve(EUMETSAT_LAST, CHARTPATH+"meteosat.jpg")
        except:
            print("Fail to retrieve internet data")
        del s
        time.sleep(600)
