#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simple-lint entrypoint script
"""

import argparse
import glob
import logging
import os


__version__ = "0.5.0"
"""
str: Program version
"""

LOGGER = logging.getLogger('simple-lint')

"""
logging: Logger instance
"""

FILE_LINTERS = {
    ".sh": "shellcheck",
    ".yml": {"yamllint", "ansible-lint"},
    ".py": {"pylint", "flake8"}
}
"""
dict: File extensions and linters
"""


def parse_options():
    """
    Parses options and arguments
    """

    desc = 'simple-linter - Linter for multiple languages'
    epilog = '''Check-out the website for more details:
http://github.com/stdevel/simple-linter'''
    parser = argparse.ArgumentParser(description=desc, \
    epilog=epilog)

    # define option groups
    gen_opts = parser.add_argument_group("generic options")
    linter_opts = parser.add_argument_group("linter options")

    # generic options
    # -E / --exclude
    gen_opts.add_argument(
        "-E", "--exclude", action="append", default=[],
        type=str, dest="filter_exclude", metavar="NAME",
        help="excludes particular files (default: no)"
    )
    # -d / --debug
    gen_opts.add_argument(
        "-d", "--debug", dest="generic_debug", default=False, \
        action="store_true", help="enable debugging outputs (default: no)"
    )

    # linter options
    linter_opts.add_argument(
        "-l", "--list", action="store_true", default=False,
        dest="list_only", help="only lists files (default: no)"
    )
    # TODO: implement
    # linter_opts.add_argument(
    #     "-D", "--disable", action="append", default=[],
    #     type=str, dest="linter_exclude", metavar="COMMAND",
    #     help="excludes particular linters (default: no)"
    # )
    # TODO: implement
    # linter_opts.add_argument(
    #     "--versions", action="store_true", default=False,
    #     type=str, dest="linter_versions",
    #     help="show only show linter versions (default: no)"
    # )

    # directories to scan
    parser.add_argument(
        'directories', metavar='DIR', type=str, nargs='*',
        help='directories containing files to check'
    )

    # parse options and arguments
    options = parser.parse_args()
    # pre-select /data if no directories given
    if not options.directories:
        options.directories = ["/data"]
    # exclude linters
    # TODO: remove linters from dict
    return options


def run_linters(files, options):
    """
    Runs linters

    :param files: files to check
    :type files: list
    """
    for _file in files:
        linters = FILE_LINTERS[os.path.splitext(_file)[1]]
        if isinstance(linters, set):
            for _cmd in linters:
                LOGGER.debug("Checking file '%s' with '%s'...", _file, _cmd)
                # os.system("%s %s" % (_cmd, _file))
                run_cmd(_cmd, _file, options)
        else:
            LOGGER.debug("Checking file '%s' with '%s'...", _file, linters)
            # os.system("%s %s" % (linters, _file))
            run_cmd(linters, _file, options)


def run_cmd(cmd, file, options):
    """
    Runs a command

    :param cmd: command
    :type cmd: str
    """
    if options.list_only:
        LOGGER.info(file)
    else:
        os.system("%s %s" % (cmd, file))


def main(options):
    """
    Main function, starts the logic based on parameters
    """
    # scan _all_ the directories
    for _dir in options.directories:
        LOGGER.debug("Checking directory '%s'", _dir)

        # finding files per extension
        _files = []
        for ext in FILE_LINTERS:
            for name in glob.glob("%s/*%s" % (_dir, ext)):
                if name not in options.filter_exclude:
                    # TODO: use globbing for exclude?
                    _files.append(name)
        LOGGER.debug("Files to check: '%s'", _files)

    run_linters(_files, options)


def cli():
    """
    This functions initializes the CLI interface
    """
    options = parse_options()

    # set logging level
    logging.basicConfig()
    if options.generic_debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    LOGGER.setLevel(log_level)

    main(options)


if __name__ == "__main__":
    cli()
