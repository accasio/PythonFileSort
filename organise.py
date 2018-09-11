"""
This is a modified version of the original script taken from https://gist.github.com/sqordfish/8e749e79a80bcad369c5
This version will sort subfolders as well. And also sorts unknown file types into a separate (./Other/) folder.
It will also rename files with the same names but have different MD5 values.
"""

import os
import hashlib
import sys
import shutil
from time import time


# Creates folders for different file types
def makeFolders(sortDir, fileTypes):
    for fileType in fileTypes.keys():
        directory = sortDir + fileType

        if not os.path.exists(directory):
            os.mkdir(directory)
    if not os.path.exists(sortDir + "Other"):
        os.mkdir(sortDir + "Other")


def renameFile(dest, moveFile, fileType):
    srcPath = moveFile
    filename = os.path.basename(moveFile)
    dstPath = dest + fileType + "\\" + filename

    # If the file doesn't have a duplicate in the new folder, move it
    if not os.path.isfile(dstPath):
        os.rename(srcPath, dstPath)
        return
    # If the file already exists with that name and has the same md5 sum
    elif os.path.isfile(dstPath) and \
            checkSum(srcPath) == checkSum(dstPath):
        os.remove(srcPath)
        print "removed " + srcPath
        return

    # If the file doesn't exist but has the same name as another file, rename it.
    elif os.path.isfile(dstPath) and \
            checkSum(srcPath) != checkSum(dstPath):
        newname = os.path.basename(os.path.dirname(srcPath))
        dstPath = dest + fileType + "\\" + newname + filename
        if not os.path.isfile(dstPath):
            os.rename(srcPath, dstPath)
        else:
            # If a file exits with newname added on rename with UNIX timestamp
            dstPath = dest + fileType + "\\" + str(int(time() * 10000)) + filename
            os.rename(srcPath, dstPath)
    else:
        print "Didn't know what to do with '%s', you may have to sort it manually." % srcPath


# Moves file to its proper folder and delete any duplicates
def moveFile(dest, moveFile, fileTypes):
    # The file format is what is after the period in the file name
    if "." in moveFile:
        temp = moveFile.split(".")
        fileFormat = temp[-1]
    else:
        renameFile(dest, moveFile, "Other")
        return

    for fileType in fileTypes.keys():
        if fileFormat.lower() in fileTypes[fileType]:
            renameFile(dest, moveFile, fileType)
            return

        elif fileType == 'Virtual_Machine_and_iso':
            renameFile(dest, moveFile, "Other")


# Get md5 checksum of a file. Chunk size is how much of the file to read at a time.
def checkSum(fileDir, chunkSize=8192):
    md5 = hashlib.md5()
    f = open(fileDir)
    while True:
        chunk = f.read(chunkSize)
        # If the chunk is empty, reached end of file so stop
        if not chunk:
            break
        md5.update(chunk)
    f.close()
    return md5.hexdigest()


def loopFolder(dest, folder, fileTypes):
    file_list = os.listdir(folder)
    # delete empty folders
    if not file_list:
        shutil.rmtree(folder)

    for filename in file_list:
        if os.path.isdir(folder + '\\' + filename):
            loopFolder(dest, folder + '\\' + filename, fileTypes)
        else:
            moveFile(dest, folder + '\\' + filename, fileTypes)


def main():
    # Dictionary contains file types as keys and lists of their corresponding file formats
    # tried to include as many formats as possible but I'm sure there are more that could be added
    fileTypes = {}
    fileTypes["Images"] = ["jpg", "gif", "png", "jpeg", "bmp", "psd", "tif", "svg"]
    fileTypes["Audio"] = ["mp3", "wav", "aiff", "flac", "aac", "wma", "au", "amr"]
    fileTypes["Video"] = ["m4v", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", "ts", "mp4", "mkv", "avi", "3gp", "m1v"]
    fileTypes["Documents"] = ["doc", "docx", "txt", "ppt", "pptx", "pdf", "rtf", "xls", "eml", "csv"]
    fileTypes["Exe"] = ["exe", "msi"]
    fileTypes["Compressed"] = ["zip", "tar", "7", "rar"]
    fileTypes["Virtual_Machine_and_iso"] = ["vmdk", "ova", "iso"]

    # The second command line argument is the download directory
    # sortDir = 'C:\\Folder\\'
    sortDir = sys.argv[1]
    downloadFiles = os.listdir(sortDir)
    makeFolders(sortDir, fileTypes)

    for filename in downloadFiles:
        # include blacklisted folders here
        if filename in ['System Volume Information', '$RECYCLE.BIN', 'Images', 'Audio', 'Documents', 'Exe',
                        'Compressed', 'Virtual_Machine_and_iso', 'Other']:
            continue
        if os.path.isdir(sortDir + filename):
            loopFolder(sortDir, sortDir + filename, fileTypes)
        else:
            moveFile(sortDir, sortDir + filename, fileTypes)


main()