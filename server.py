# coding:utf-8

from __future__ import unicode_literals
import os
import argparse
import cgi
from urllib import quote

from flask import Flask, render_template, safe_join, send_file
from werkzeug.exceptions import NotFound


app = Flask(__name__)

ROOT_DIR = '.'


@app.route('/<path:filename>')
@app.route('/')
def show_files(filename=''):
    filename = safe_join(ROOT_DIR, filename)
    if os.path.isdir(filename):
        files = os.listdir(filename)
        files.sort(key=lambda x: x.lower())
        files_dict = {}
        for name in files:
            fullname = os.path.join(filename, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"

            files_dict[quote(linkname.encode('utf-8'))] = cgi.escape(displayname)

        return render_template('show_files.html',
                               path=cgi.escape(os.path.splitdrive(filename)[-1]), files=files_dict)

    if not os.path.isfile(filename):
        raise NotFound

    return send_file(filename)


def main():
    global ROOT_DIR
    parser = argparse.ArgumentParser(description='Simple HTTP Server in Flask')
    parser.add_argument('--path')

    ROOT_DIR = os.path.abspath(parser.parse_args().path or os.getcwd())
    app.run(debug=True)


if __name__ == '__main__':
    main()
