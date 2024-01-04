import os
import shutil
import filecmp
import argparse
import time

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source', help='the source directory path', type=str)
parser.add_argument('--replica', help='the replica directory path', type=str)
parser.add_argument('--interval', help='the synchronization interval in seconds', type=int)
parser.add_argument('--logger', help='the log filepath', type=str)

args = parser.parse_args()
sourceRoot = args.source
replicaRoot = args.replica
syncInterval = args.interval
loggerPath = args.logger


def log(message):
    logger.write(message + '\n')
    print(message)


while True:
    logger = open(loggerPath, "a")
    log('starting a synchronization action')

    # map the content of the source folder
    sourceContentFileList = []
    sourceContentDirList = []
    for root, dirs, files in os.walk(sourceRoot, topdown=False):
        for name in files:
            sourceFilePath = os.path.join(root, name)
            sourceContentFileList.append(sourceFilePath)
        for name in dirs:
            sourceDirPath = os.path.join(root, name)
            sourceContentDirList.append(sourceDirPath)

    # map the content of the replica folder
    replicaContentFileList = []
    replicaContentDirList = []
    for root, dirs, files in os.walk(replicaRoot, topdown=False):
        for name in files:
            sourceFilePath = os.path.join(root, name)
            replicaContentFileList.append(sourceFilePath)
        for name in dirs:
            sourceDirPath = os.path.join(root, name)
            replicaContentDirList.append(sourceDirPath)

    # delete the files and folders that shouldn't exist under the replica folder
    for path in replicaContentFileList:
        temp = sourceRoot + path.removeprefix(replicaRoot)
        if temp not in sourceContentFileList:
            log(f'removing file from replica folder: {path}')
            os.remove(path)

    for path in replicaContentDirList:
        temp = sourceRoot + path.removeprefix(replicaRoot)
        if temp not in sourceContentDirList:
            log(f'removing folder from replica folder: {path}')
            shutil.rmtree(path)

    # copy the files and folders that are missing or modified
    for path in sourceContentDirList:
        temp = replicaRoot + path.removeprefix(sourceRoot)
        if temp not in replicaContentDirList:
            # create a copy of this folder from source to replica folder
            log(f'copy folder {path} to replica folder')
            shutil.copytree(path, temp)

    for path in sourceContentFileList:
        temp = replicaRoot + path.removeprefix(sourceRoot)
        if temp not in replicaContentFileList or filecmp.cmp(path, temp) is False:
            # create a copy of this file from source to replica folder
            log(f'copy file {path} to replica folder')
            shutil.copyfile(path, temp)

    # sleep for the amount of seconds until the next round
    log(f'completed a cycle, sleeping {syncInterval} seconds')
    logger.close()
    time.sleep(syncInterval)
