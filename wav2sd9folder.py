import os
import mmap
import sys


def main():
    if not len(sys.argv) == 2:
        print('Usage: wav2sd9folder *.wav')
        exit(1)

    global wavFile
    dir_path = os.path.dirname(os.path.realpath(__file__))
    replacement = sys.argv[1]

    if not str(replacement).endswith('.wav'):
        print('Not a .wav file')
        exit(1)
    else:
        wavFile = open(replacement, 'r+b').read()
        if wavFile[0x24] == 100:
            print('The wav file must be encoded with Microsoft ADPCM')
            exit(1)

    size = chr(wavFile[0x05]).encode(), chr(wavFile[0x06]).encode()

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.sd9'):
                continue

            filepath = os.path.join(root, file)
            print(filepath)
            writefile(filepath, wavFile, size)


def writefile(file, replacement, size):
    filesize = len(replacement) + 32

    with open(file, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        mm.resize(filesize)
        mm.seek(0x09)
        mm.write(size[0])
        mm.seek(0x0A)
        mm.write(size[1])
        mm.seek(0x20)
        mm.write(replacement)


if __name__ == '__main__':
    main()
