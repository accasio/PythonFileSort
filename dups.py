"""
Removes files with the same name from a folder but with different file extensions.
Can be handy if you have multiple versions of songs in various file formats.
"""

import glob
import os
import sys

# folder_to_sort = 'D:\\Audio\\'
folder_to_sort = sys.argv[1]

mus_files = list(sorted(glob.glob(folder_to_sort + '*')))

names = [os.path.splitext(os.path.basename(mus_file))[0] for mus_file in mus_files]

for mus_file in mus_files:
    mus_filename = os.path.splitext(os.path.basename(mus_file))[0]
    occurrences = names.count(mus_filename)

    if occurrences > 1:
        for i, sub_file in enumerate(mus_files):
            sub_filename = os.path.splitext(os.path.basename(sub_file))[0]
            if mus_filename == sub_filename and sub_file != mus_file:
                print 'Deleting ', mus_file
                os.remove(mus_file)
                del mus_files[i]
                del names[i]
                occurrences = occurrences - 1
                if occurrences == 1:
                    break
