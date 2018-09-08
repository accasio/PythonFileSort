import os
import sys
import hashlib
import shutil


# Creates folders for different file types
def makeFolders(downloadDirectory, fileTypes):
    for fileType in fileTypes.keys():
        directory = downloadDirectory + "\\" + fileType

        if not os.path.exists(directory):
            os.mkdir(directory)
    if not os.path.exists("D:\\Other"):
        os.mkdir("D:\\Other")


# Moves file to its proper folder and delete any duplicates
def moveFile(moveFile, fileTypes):
    # The file format is what is after the period in the file name

    if "." in moveFile:
        temp = moveFile.split(".")
        fileFormat = temp[-1]
    else:
        return

    for fileType in fileTypes.keys():
        if fileFormat in fileTypes[fileType]:
            srcPath = moveFile
            filename = os.path.basename(moveFile)
            dstPath = "D:\\" + fileType + "\\" + filename

            # If the file doesn't have a duplicate in the new folder, move it
            if not os.path.isfile(dstPath):
                os.rename(srcPath, dstPath)
            # If the file already exists with that name and has the same md5 sum

            elif os.path.isfile(dstPath) and \
                    checkSum(srcPath) == checkSum(dstPath):
                os.remove(srcPath)
                print "removed " + srcPath
                return

            elif os.path.isfile(dstPath) and \
                    checkSum(srcPath) != checkSum(dstPath):
                newname = os.path.basename(os.path.dirname(srcPath))

                dstPath = "D:\\" + fileType + "\\" + newname + filename
                if not os.path.isfile(dstPath):
                    os.rename(srcPath, dstPath)
                elif os.path.isfile(dstPath) and \
                        checkSum(srcPath) == checkSum(dstPath):
                    os.remove(srcPath)
                    print "removed " + srcPath

        elif fileType == 'Virtual_Machine_and_iso':
            print moveFile
            """
            srcPath = moveFile
            filename = os.path.basename(moveFile)
            dstPath = "D:\\Other\\" + filename

            # If the file doesn't have a duplicate in the new folder, move it
            if not os.path.isfile(dstPath):
                os.rename(srcPath, dstPath)
            # If the file already exists with that name and has the same md5 sum

            elif os.path.isfile(dstPath) and \
                    checkSum(srcPath) == checkSum(dstPath):
                os.remove(srcPath)
                print "removed " + srcPath
            return
            
            
            """





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


def loopFolder(folder, fileTypes):
    downloadFiles = os.listdir(folder)
    if not downloadFiles:
        shutil.rmtree(folder)
    elif len(downloadFiles) == 1 and '.ini' in downloadFiles[0] or '.db' in downloadFiles[0]:
        shutil.rmtree(folder)

    for filename in downloadFiles:
        if filename == '$RECYCLE.BIN' or '.ini' in filename or '.lnk' in filename \
                or '.db' in filename or filename == '.Picasa3Temp' or 'bob marley and the wailers' in filename:
            continue
        if os.path.isdir(folder + '\\' + filename):
            loopFolder(folder + '\\' + filename, fileTypes)
        else:
            moveFile(folder + '\\' + filename, fileTypes)

def main():
    # Dictionary contains file types as keys and lists of their corresponding file formats`
    fileTypes = {}
    fileTypes["Images"] = ["jpg", "gif", "png", "jpeg", "bmp", "JPG", "bmp", "psd", "BMP", "tif"]
    fileTypes["Audio"] = ["mp3", "wav", "aiff", "flac", "aac", "wma", "au", "amr"]
    fileTypes["Video"] = ["m4v", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", "MOV", "mp4", "mkv", "AVI", "avi", "3gp", "m1v"]
    fileTypes["Documents"] = ["doc", "docx", "txt", "ppt", "pptx", "pdf", "rtf", "xls", "eml", "PDF"]
    fileTypes["Exe"] = ["exe"]
    fileTypes["Compressed"] = ["zip", "tar", "7", "rar"]
    fileTypes["Virtual_Machine_and_iso"] = ["vmdk", "ova", "iso"]

    # The second command line argument is the download directory
    downloadDirectory = 'D:\\Unknown Artist\\'
    downloadFiles = os.listdir(downloadDirectory)
    # makeFolders(downloadDirectory, fileTypes)

    for filename in downloadFiles:
        if filename == '$RECYCLE.BIN' or filename == 'RECYCLER' or filename == 'System Volume Information' or filename == 'Audio' or filename == 'Images' or filename == 'Video' or \
                filename == 'Documents' or filename == 'Exe' or filename == 'Compressed' or \
                filename == 'Virtual_Machine_and_iso' or filename == 'Other' or filename == "Extra":
            continue
        if os.path.isdir(downloadDirectory + filename):
            loopFolder(downloadDirectory + filename, fileTypes)
        else:
            moveFile(downloadDirectory + filename , fileTypes)


main()