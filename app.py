import os
import urllib2
from datetime import datetime

FRIST_NUMBER = [8,9]
BASE_URL_FORMAT = "https://www.bsfinternational.org/BSFAjaxUtils/Dispatch?action=AjaxGetClassMeetingInfo&phoneNumber={}&searchByPhone=true".format

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
    def generateNumber(base_num,x):
        return FRIST_NUMBER[base_num]*10000000 + x

    for base_num in range(1,2):
        for x in 1,10:
            number = generateNumber(base_num,x)
            print "Trying {}".format(number)

    #response = urllib2.urlopen("http://example.com/foo/bar").read()
    return

def main():
    init()
    harvest()

if __name__ == '__main__':
    main()