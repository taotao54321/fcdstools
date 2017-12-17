#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""quick-and-dirty test script

put *.fds in fds/ directory, and run this script.
"""

import pathlib
import subprocess
import sys
import tempfile

FDSCHECK = "./fdscheck"
FDSSPLIT = "./fdssplit"
FDSBUILD = "./fdsbuild"

FDS_DIR = pathlib.Path("fds/")

FDSS = tuple(FDS_DIR.glob("*.fds"))

def test_fds(fds):
    try:
        plain_fds = check_plain(fds)

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            body = check_manifest(fds)
            if not body: return False
            tmp.write(check_manifest(fds))
            manifest = tmp.name

        with tempfile.TemporaryDirectory() as dir_:
            split(fds, dir_)
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                fds_out = tmp.name
            build(fds_out, manifest, dir_, has_header(fds))

        plain_fds_out = check_plain(fds_out)

        return plain_fds == plain_fds_out
    except Exception as e:
        print(e, file=sys.stderr)
        return False

def check_plain(fds):
    cmdline = ( FDSCHECK, fds )
    proc = subprocess.run(cmdline, check=True, stdout=subprocess.PIPE)
    return proc.stdout

def check_manifest(fds):
    cmdline = (
        FDSCHECK,
        "-f", "manifest",
        fds,
    )
    proc = subprocess.run(cmdline, check=True, stdout=subprocess.PIPE)
    return proc.stdout

def split(fds, destdir):
    cmdline = (
        FDSSPLIT,
        "-d", destdir,
        fds,
    )
    subprocess.run(cmdline, check=True, stdout=subprocess.DEVNULL)

def build(fds_out, manifest, srcdir, with_header):
    opts = () if with_header else ("--noheader",)
    cmdline = (
        FDSBUILD,
        "-d", srcdir,
        *opts,
        fds_out,
        manifest,
    )
    subprocess.run(cmdline, check=True, stdout=subprocess.DEVNULL)

def has_header(fds):
    return fds.stat().st_size % 65500 == 16

def main():
    n_ok = 0
    for fds in FDSS:
        if test_fds(fds):
            n_ok += 1
        else:
            print(f"{fds}: failed")

    print(f"{n_ok}/{len(FDSS)} success")

    sys.exit(0 if n_ok == len(FDSS) else 1)

if __name__ == "__main__": main()
