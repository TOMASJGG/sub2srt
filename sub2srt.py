#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_lineno_generator():
    import itertools

    return itertools.count(1)

def get_time_converter(fps):
    def convert(frames):
       total_seconds = frames/fps
    
       hours = int(total_seconds / 3600)
       minutes = int(total_seconds % 3600 / 60)
       seconds = int(total_seconds % 3600 % 60)
       millis = int(1000 * (total_seconds - int(total_seconds)))

       return "%d:%d:%d,%d" % (hours, minutes, seconds, millis)
    return convert

def get_line_converter(to_time, lineno):
    import re
    re_sub = re.compile('\{(?P<start>[0-9]+)\}\{(?P<end>[0-9]+)\}(?P<text>.*)')

    def convert(line):
        (start, end, text) = re_sub.match(line).groups()

        duration = "%s --> %s" % (to_time(int(start)), to_time(int(end)))

        return "%d\r\n%s\r\n%s\r\n\r\n" % (lineno.next(), duration, text)
    return convert

def get_args():
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert subtitle file formats from .sub to .srt.',
        epilog='Have fun!')

    parser.add_argument('fps', type=float)
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('output', type=argparse.FileType('w'))

    return parser.parse_args() # from command line

def main():
    args = get_args()

    line_converter = get_line_converter(get_time_converter(args.fps),
                                        get_lineno_generator())

    for line in args.input.readlines():
        args.output.write(line_converter(line))

    print "Yay! Done!"

if __name__ == '__main__':
    main()
