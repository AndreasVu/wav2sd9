import os
import mmap
import sys


def main():
    if not len(sys.argv) == 2:
        print('Usage: wav2sd9folder *.wav')
        exit(1)

    global wavfile, wavmap
    dir_path = os.path.dirname(os.path.realpath(__file__))
    replacement = sys.argv[1]

    if not str(replacement).endswith('.wav'):
        print('Not a .wav file')
        exit(1)
    else:
        wavfile = open(replacement, 'r+b')
        wavmap = mmap.mmap(wavfile.fileno(), 0)
        if wavmap[0x24] == 100:
            print('The wav file must be exported with Microsoft ADPCM')
            exit(1)

    wavmap.seek(0x5)
    size = wavmap.read(1), wavmap.read(1)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.sd9'):
                continue

            filepath = os.path.join(root, file)
            print(filepath)
            writefile(filepath, wavmap, size)


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
