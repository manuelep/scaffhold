# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# Database connection configuration
# -------------------------------------------------------------------------
if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
        pool_size = configuration.get('db.pool_size', 10),
        migrate_enabled = configuration.get('db.migrate'),
        check_reserved = None, #['all'],
        bigint_id = configuration.get('db.bigint_id', False)
    )
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    #session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# Session storage configuration
# -------------------------------------------------------------------------
if request.env.web2py_runtime_gae:
    session.connect(request, response, db=db,
        masterapp = configuration.get('session.masterapp')
    )
elif configuration.get('session.storage')=='cookie':
    session.connect(request, response,
        cookie_key = configuration.get('session.cookie_key'),
        compression_level = None,
        masterapp = configuration.get('session.masterapp')
    )
elif configuration.get('session.storage')=='memcached' and configuration.get('cache.storage')=='memcached':
    from gluon.contrib.memdb import MEMDB
    session.connect(request, response,
        db = MEMDB(cache.memcache),
        masterapp = configuration.get('session.masterapp')
    )
elif configuration.get('session.storage')=='redis':
    raise NotImplementedError()
elif configuration.get('session.storage')=='database':
    if configuration.get('session.uri'):
        session.connect(request, response,
            db = DAL(configuration.get('session.uri'),
                pool_size = configuration.get('session.pool_size', 10),
                migrate_enabled = configuration.get('session.migrate', False),
                check_reserved = ['all']
            ),
            masterapp=configuration.get('session.masterapp')
        )
    elif configuration.get('session.db'):
        session.connect(request, response,
            db = vars()[configuration.get('session.db')],
            masterapp = configuration.get('session.masterapp')
        )

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_stacked'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------


def manage_auth():

    if configuration.get('CAS.enabled', False):
        cas_url = configuration.get('CAS.url', URL(
            configuration.take('CAS.application'),
            configuration.get('CAS.controller', 'default'),
            configuration.get('CAS.function', 'user'),
            args = configuration.get('CAS.args', 'cas').split(","),
            host = configuration.get('CAS.host', request.host),
            scheme = configuration.get('CAS.scheme', request.env.wsgi_url_scheme),
            port = configuration.get('CAS.port', request.env.server_port)
        ))
    else:
        cas_url = None

    # host names must be a list of allowed host names (glob syntax allowed)
    auth = Auth(db, host_names = configuration.get('host.names'),
        cas_provider = cas_url
    )

    # -------------------------------------------------------------------------
    # create all tables needed by auth, maybe add a list of extra fields
    # -------------------------------------------------------------------------
    auth.settings.extra_fields['auth_user'] = []
    auth.define_tables(username=False, signature=False)

    current.auth = auth

    return auth

# -------------------------------------------------------------------------
# Scheduler configuration
# -------------------------------------------------------------------------

if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler, HEARTBEAT
    from swissknife.timeformat import prettydelta

    sdb = DAL(configuration.take('scheduler.uri'),
        pool_size = configuration.get('scheduler.pool_size', 10),
        migrate_enabled = configuration.get('scheduler.migrate', False),
        check_reserved = None
    )

    scheduler = Scheduler(sdb, heartbeat=configuration.get('scheduler.heartbeat', HEARTBEAT))

    _elapsed_time = lambda row: row.scheduler_run.status=='COMPLETED' and \
        prettydelta(row.scheduler_run.stop_time - row.scheduler_run.start_time, use_suffix=False)
    sdb.scheduler_run.elapsed_time = Field.Virtual("elapsed_time", _elapsed_time)

    sdb.scheduler_task.vars.readable = False
    sdb.scheduler_task.task_name.readable = False
    sdb.scheduler_task.retry_failed.readable = False
    sdb.scheduler_task.uuid.readable = False
