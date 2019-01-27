import mmap
import sys


def main():
    if not len(sys.argv) == 3:
        print('Usage: wav2sd9file *.wav *.sd9')
        exit(1)

    global wavFile
    replacement = sys.argv[1]
    original = sys.argv[2]

    if not original.endswith('.sd9') or not replacement.endswith('.wav'):
        print('Wrong filetypes')
        exit(-1)
    else:
        wavFile = open(replacement, 'r+b').read()
        if wavFile[0x24] == 100:
            print('The wav file must be encoded with Microsoft ADPCM')
            exit(1)

    size = chr(wavFile[0x05]).encode(), chr(wavFile[0x06]).encode()
    writefile(original, wavFile, size)
    print('Conversion done.')


def writefile(original, replacement, size):
    filesize = len(replacement) + 32

    with open(original, 'r+b') as f:
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
