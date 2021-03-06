# Copyright (c) 2013, Edd Barrett <edd@openbsd.org> <vext01@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import argparse

VERSION=0.1

EPILOG = """
INCLUDE and EXCLUDE are package specs of the form:

  pkgname | pkgname:filetype1, ..., filetype_n

The first variant includes all file types. Filetypes: run, src, doc, bin.

Example usage:

  Initialise the database:

      $ texscythe --initdb

  Compute a subset with scheme-tetex excluding scheme-mininial's docfiles:

      $ texscythe --subset -i scheme-tetex -x scheme-minimal:doc
"""

DESCR = "Compute subsets of the TeX Live texmf tree."

def print_version():
        print(72 * "-")
        print("  TeXScythe Version %s" % (VERSION))
        print("  (c) Edd Barrett 2013 <vext01@gmail.com> <edd@openbsd.org>")
        print(72 * "-")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            epilog=EPILOG,
            description=DESCR,
            formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--initdb", action='store_true',
            help="initialise the database")
    parser.add_argument("-s", "--subset", action='store_true',
            help="compute a subset")
    parser.add_argument("-i", "--include", nargs='*',
            help="include package in subset")
    parser.add_argument("-x", "--exclude", nargs='*',
            help="exclude package in subset")
    parser.add_argument("--version", action='store_true',
            help="show version")
    parser.add_argument("-P", "--prefix_filenames",
            help="prefix string to filenames")
    parser.add_argument("-o", "--output-plist",
            help="output filename")
    parser.add_argument("-t", "--tlpdb",
            help="path to texive.tlpdb")
    parser.add_argument("-d", "--sqldb",
            help="path to sqlite3 database")
    parser.add_argument("-a", "--arch",
            help="cpu architecure, e.g. 'alpha-linux' "
            "(if not set, ARCH pkgs ignored)")

    args = parser.parse_args()

    # No two of these should be enabled at once
    primary_tasks = [args.subset, args.version, args.initdb]
    chosen_tasks = [ x for x in primary_tasks if x ]

    if len(chosen_tasks) != 1:
        parser.error("please select a single primary task.\n  one of: --initdb, --subset, --version")

    # setup configuration
    config = {
            "sqldb"             : "texscythe.db",
            "plist"             : "PLIST",
            "prefix_filenames"  : "",
            "tlpdb"             : "texlive.tlpdb",
            "arch"              : None,
    }

    if args.sqldb is not None:
        config["sqldb"] = args.sqldb
    if args.prefix_filenames is not None:
        config["prefix_filenames"] = args.prefix_filenames
    if args.output_plist is not None:
        config["plist"] = args.output_plist
    if args.tlpdb is not None:
        config["tlpdb"] = args.tlpdb
    if args.arch is not None:
        config["arch"] = args.arch

    if not args.version:
        print_version()
        print("\nRunning with configuration:")
        for k in config.iterkeys():
            print("    %s: %s" % (k.ljust(25), config[k]))
        print("")

    # primary tasks
    if args.subset:
        import subset
        subset.compute_subset(config, args.include, args.exclude)
    elif args.initdb:
        import tlpdbparser
        tlpdbparser.initdb(config)
    elif args.version:
        print_version()
    else:
        assert False # should not happen
