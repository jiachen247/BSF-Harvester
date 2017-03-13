#!/usr/bin/env python

import os
import urllib
import urllib2
import ssl
from datetime import datetime
import sys
import json

FRIST_NUMBER = [8,9]
HTTP_URL_FORMAT = "https://www.bsfinternational.org/BSFAjaxUtils/Dispatch?action=AjaxGetClassMeetingInfo&searchByPhone=true&phoneNumber={}".format

FILE_DUMP_FORMAT = "{}-{}".format


HTTP_HEADERS = {
    "Host": "www.bsfinternational.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.bsfinternational.org/lessons",
    "X-Requested-With":"XMLHttpRequest"
}
HTTP_PARAMS = {
    "action":"AjaxGetClassMeetingInfo",
    "phoneNumber":"placeholder",
    "classNumber":"936",
    "searchByPhone":"true"
}
HTTP_PARAMS_ENCODED = data = urllib.urlencode(HTTP_PARAMS)


PATH_DUMP = "./DUMP"
PATH_DUMP_BK_FORMAT ="./DUMP-{}.bak".format


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
    def getSSLcontextTrustAllStrategy():
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def generateNumber(base_num,x):
        return FRIST_NUMBER[base_num]*10000000 + x
    def get(number):
        HTTP_PARAMS['phoneNumber'] = str(number)
        req = urllib2.Request(HTTP_URL_FORMAT(number),headers=HTTP_HEADERS)
        response = urllib2.urlopen(req,context=getSSLcontextTrustAllStrategy())
        return json.loads(response.read())


    #for base_num in range(1,2):
        #for x in range(1,9999999):
            #number = generateNumber(base_num,x)
            #print "Trying {}".format(number)
            #result = getByNumber()

    data =  get(sys.argv[1])
    print FILE_DUMP_FORMAT(data.classNumber , data.meetingChurch)
    print "hello"
    #response = urllib2.urlopen("http://example.com/foo/bar").read()
    return

def main():
    init()
    harvest()

if __name__ == '__main__':
    main()