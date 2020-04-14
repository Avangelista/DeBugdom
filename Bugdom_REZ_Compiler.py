# Bugdom_REZ_Compiler.py
# Rory 2020
# Compiles a directory of Bugdom assets into a .Rez file to be used in game

# Requires file_list.txt to work correctly!
# Get it here: https://github.com/nutmeg-5000/bugdom/blob/master/file_list.txt

import sys
import os
from zlib import compress

if len(sys.argv) >= 3:
    outFile = sys.argv[2]
else:
    outFile = 'Bugdom.Rez'

if len(sys.argv) >= 2:
    resDir = sys.argv[1]
else:
    print('Usage: ' + sys.argv[0] + ' path/to/asset/directory [output_file_name]')
    sys.exit()

try:
    with open('file_list.txt', 'r') as f:
        fileList = f.read().splitlines()
except OSError:
    print('ERROR: "file_list.txt" not found!')
    sys.exit()

print('Reading files from ' + resDir + '...')

totalFileNameLen = 0
totalFileDataLen = 0
archiveFiles = []
for file in fileList:
    try:
        with open(os.path.join(resDir, file), 'rb') as f:
            data = f.read()
    except OSError:
        print('ERROR: Necessary file "' + file + '" not found in directory!')
        sys.exit()
    formatted_name = file.replace('/', ':').encode() + b'\x00'
    compressed = compress(data)

    new_file = {
        'formatted_name': formatted_name,
        'size': len(data),
        'compressed_size': len(compressed),
        'compressed_data': compressed,
        'relative_name_offset': totalFileNameLen,
        'relative_data_offset': totalFileDataLen
    }
    archiveFiles.append(new_file)

    totalFileNameLen += len(formatted_name)
    totalFileDataLen += 4 + len(compressed)

nFiles = len(archiveFiles)

print('Setting up file structure...')

ID = b'BRGR'
VERSION = b'\x01\x00\x00\x00'
# insert our tagline here... as it doesn't seem to ruin anything
FILLER_1 = b'DBUG\x01\x00\x00\x00'
N_FILES = nFiles.to_bytes(4, byteorder='little')
infoSize = 12 + (12 * nFiles) + totalFileNameLen
INFO_SIZE = infoSize.to_bytes(4, byteorder='little')

INDEX = b''
NAMES = b''
DATA = b''
for f in archiveFiles:
    offset = 12 + infoSize + f['relative_data_offset'] + 0x20000000
    compressed_size = 4 + f['compressed_size']
    name_offset = 12 + (12 * nFiles) + f['relative_name_offset']
    INDEX += offset.to_bytes(4, byteorder='little') + compressed_size.to_bytes(4, byteorder='little') + name_offset.to_bytes(4, byteorder='little')

    NAMES += f['formatted_name']

    size = f['size']
    compressed_data = f['compressed_data']
    DATA += size.to_bytes(4, byteorder='little') + compressed_data

print('Writing to ' + outFile + '...')

with open(outFile, 'wb') as f:
    f.write(ID)
    f.write(VERSION)
    f.write(INFO_SIZE)
    f.write(FILLER_1)
    f.write(N_FILES)
    f.write(INDEX)
    f.write(NAMES)
    f.write(DATA)

print('Done!')
