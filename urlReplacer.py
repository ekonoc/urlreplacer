#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Detect and Replace URLs.
If you are planning to move your assets  to a CDN this program can make all the
changes by choosing the extension of the files to be analyzed and the extension
of the files to detect and replace the URL.

By default the program will go through the entire directory specified locating
files with extensions php, html and js to search href, src and srcset within
them to change the URL if it matches certain extensions
(jpg, jpeg, gif, png, tiff, js, css, scss, ico, svg, webm, mp4)

Every changed file is backed up with the extension .bak

But it is fully customizable.
"""


import argparse
import os
import fileinput
import re
import logging
import textwrap


__author__ = "KennBro"
__copyright__ = "Copyright 2020, The EKONOC Tools"
__credits__ = ["KennBro"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "KennBro"
__email__ = "kennbro <at> protonmail <dot> com"
__status__ = "Development"


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        logging.error("readable_dir:{} is not a valid path".format(path))
        raise argparse.ArgumentTypeError(
            "readable_dir:{} is not a valid path".format(path))


def process_urls(directory, file_ext):
    logging.info("Process directory : {}".format(directory))
    filelist = []
    lstDir = os.walk(directory)

    for root, dirs, files in lstDir:
        for _file in files:
            (filename, extension) = os.path.splitext(_file)
            if (extension[1:].lower() in file_ext):
                logging.debug('File detected : {}'.format(str(root) + _file))
                filelist.append(str(root) + "/" + _file)

    return tuple(i for i in filelist)


def detect_urls(files, search_ext, search_tag):
    logging.info("Searching URLs in : {}".format(files))
    logging.debug("Extension to find : {}".format(search_ext))
    filelist = []
    regex = search_tag + "(https?:\\/\\/[^\\/]*\\/)?([\\w|\\/|\\-|\\." + \
        "]*)\\.(" + search_ext + ")"

    with fileinput.input(files=files) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                logging.debug("Match Found in line {} in file {}".format(
                    fileinput.filelineno(), fileinput.filename()))
                filename = fileinput.filename()
                if str(filename) not in filelist:
                    filelist.append(str(filename))

    logging.info("Detect URLs in : {}".format(filelist))
    return tuple(i for i in filelist)


def replace_urls(files, search_ext, search_tag, cdn):
    logging.info("Replace URLs in : {}".format(files))
    logging.debug("Extension to replace : {}".format(search_ext))
    regex = search_tag + "(https?:\\/\\/[^\\/]*\\/)?([\\w|\\/|\\-|\\." + \
        "]*)\\.(" + search_ext + ")"

    with fileinput.input(files=files, inplace=True, backup=".bak") as f:
        for line in f:
            line = re.sub(regex, "\\1" + cdn + "\\3", line.rstrip())
            print(line)


if __name__ == '__main__':

    print("""
        (    (      (
        )\ ) )\ )   )\ )             (
    (  (()/((()/(  (()/(   (         )\    )         (   (
    )\  /(_))/(_))  /(_)) ))\ `  )  ((_)( /(   (    ))\  )(
 _ ((_)(_)) (_))   (_))  /((_)/(/(   _  )(_))  )\  /((_)(()\\
| | | || _ \| |    | _ \(_)) ((_)_\ | |((_)_  ((_)(_))   ((_)
| |_| ||   /| |__  |   // -_)| '_ \)| |/ _` |/ _| / -_) | '_|
 \___/ |_|_\|____| |_|_\\\\___|| .__/ |_|\__,_|\__| \___| |_|
                             |_|
          Developed by Kennbro powered by ekonoc""")
    print()

    log_format = "%(asctime)s [%(levelname)s]: %(filename)s:%(lineno)s" + \
        ">> %(message)s"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Detect and Replace URLs.
            If you are planning to move your assets  to a CDN this program can make all the changes by choosing the
            extension of the files to be analyzed and the extension of the files to detect and replace the URL.

            By default the program will go through the entire directory specified locating files with extensions php,
            html and js to search href, src and srcset within them to change the URL if it matches certain extensions
            (jpg, jpeg, gif, png, tiff, js, css, scss, ico, svg, webm, mp4)

            Every changed file is backed up with the extension .bak

            But it is fully customizable.
            '''),
        epilog='''
            Examples
            --------

            # Detect changes to be made in the /var/www/html directory
            python3 urlReplacer.py /var/www/html

            # Change CDN URLs to https://CDN.com/
            python3 urlReplacer.py -r https://CDN.com/ /var/www/html

            # Change only php and html files
            python3 urlReplacer.py -r https://CDN.com/ /var/www/html -e php -e html

            # Change only svg and png URLs
            python3 urlReplacer.py -r https://CDN.com/ /var/www/html -a svg -a png
            ''')
    parser.add_argument('-r', '--replace',
                        help='Replace URLs with the specified CDN')
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="modify output verbosity")
    parser.add_argument('-e', type=lambda arg: arg.split(','),
                        dest='file_extension',
                        default=["php", "html", "js"],
                        help='Add file extension to analyze in directory')
    parser.add_argument('-s', type=lambda arg: arg.split(','),
                        dest='file_search',
                        default=["jpg", "jpeg", "gif", "png", "tiff", "js",
                                 "css", "scss", "ico", "svg", "webm", "mp4"],
                        help='Add file extension to search into files')
    parser.add_argument('-t', type=lambda arg: arg.split(','),
                        dest='tag_search',
                        default=["href", "src", "srcset"],
                        help='Add tag to search inside files.')
    parser.add_argument('path', type=dir_path,
                        help="path to process")

    args = parser.parse_args()

    path = os.path.dirname(os.path.realpath(__file__))
    if args.path:
        path = args.path

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel,
                        format=log_format,
                        datefmt='%m-%d %H:%M')

    file_search = args.file_search[0]
    for ext in args.file_search:
        file_search = file_search + "|" + ext
    tag_search = "("
    for tag in args.tag_search:
        # TODO: Control url param
        tag_search = tag_search + tag + "=\"|"
    tag_search = tag_search[:-1] + ")"

    files = process_urls(path, args.file_extension)
    files = detect_urls(files, file_search, tag_search)

    if args.replace:
        replace_urls(files, file_search, tag_search, args.replace)
