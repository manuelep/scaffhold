#!/usr/bin/env python
# -*- coding: utf-8 -*-

def makedirs(filename):
    """ Courtesy of: https://stackoverflow.com/a/12517490/1039510 """

    is_py_32p = "{major}.{minor}".format(
        major=sys.version_info.major,
        minor=sys.version_info.minor
    )>="3.2"

    if is_py_32p:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    else:
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

def path(*dirs):
    """ """
    return os.path.join(request.folder, *dirs)

def dbsetup():
    dbcollector = ConnCollector(
        path = os.path.join(request.folder, "databases"),
        cache = None if args.nocache else Cache(request)
    )

    # import pdb; pdb.set_trace()
    for cnt,section in enumerate(args.connections):
        urikey = '{}.uri'.format(section)
        uri = myconf.take(urikey)
        extkey = '{}.extensions'.format(section)
        exts = list(filter(lambda s: s, myconf.get(extkey, [])))
        if myconf.take(urikey).startswith('postgres://'):
            print(["Ok", uri, exts])
            dbcollector.collect(uri, *exts)
        else:
            print(["No", uri])

    if cnt>0:
        dbcollector.setup()

def create_required_paths():
    """
    Usecase: web2py framework needs for their application some folder that can be
    initially empty but empty folders are not versioned by git and the framework
    does not manage their creation if missing raising an exception on startup.
    """
    for mypath in ("databases",):
        makedirs(path(mypath).rstrip('/')+'/')

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description = """
        To be run with command line (add -h for help):

        $ python web2py.py -S a/c/ -R applications/<this app>/<path to this script>/<this script>.py -A <this script options>
                             ^^^^^
        Essential doc quote:

        -S APPNAME, --shell=APPNAME
            run web2py in interactive shell or IPython (if
            installed) with specified appname (if app does not
            exist it will be created). APPNAME like a/c/f (c,f
            optional)

        -M, --import_models
            auto import model files; default is False;
            should be used with --shell option

        -R PYTHON_FILE, --run=PYTHON_FILE
            run PYTHON_FILE in web2py environment; should be used
            with --shell option

        -A ARGS, --args=ARGS
            should be followed by a list of arguments to be passed to script,
            to be used with -S. Warning: -A must be the last option

        Note:

        ## WARNING ## The -M option is FORBIDDEN for this script.

        """,
        formatter_class = argparse.RawTextHelpFormatter
    )

    try:
        assert not 'configuration' in vars()
    except AssertionError as err:
        message = """You are running this script without the necessary environment.
        Please read the documentation here below."""
        parser.print_help()
        raise Exception(message)
    else:
        import os
        from gluon.contrib.appconfig import AppConfig
        from gluon.cache import Cache
        from setupdb.dummydb import ConnCollector
        import sys

    myconf = AppConfig(configfile=os.path.join(os.getcwd(), "applications", request.application, "private", "appconfig.ini"))

    parser.add_argument("-c", "--connections",
        help = "List of keys in configuration where to find connection uris",
        type = lambda v: v.split(",")
    )

    parser.add_argument("--no-cache",
        help = 'Disable password caching',
        action = 'store_true',
        default = False,
        dest = 'nocache'
    )

    args = parser.parse_args()

    create_required_paths()
    dbsetup()
