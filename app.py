import os
from datetime import datetime

FRIST_NUMBER = {8,9}

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
    return
def cleanup():
    return

def main():
    init()

    harvest()

    cleanup()

if __name__ == '__main__':
    main()