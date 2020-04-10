# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

from gluon.tools import PluginManager
plugins = PluginManager()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=vars().get('reload_config', False))

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()
if configuration.get('app.requires_https', False):
    request.requires_https()
    session.secure()

# -------------------------------------------------------------------------
# Logging configuration
# -------------------------------------------------------------------------
import logging
logger = logging.getLogger("web2py.app.{}".format(request.application))
logging_level_name = configuration.get("app.log_level") or "DEBUG"
logging_level = getattr(logging, logging_level_name)
logger.setLevel(logging_level)

from gluon import current

current.logger = logger

# -------------------------------------------------------------------------
# Cache services configuration
# -------------------------------------------------------------------------
if configuration.get('cache.storage') == 'memcached':
    memcache_servers = configuration.get('memcached.hosts')
    from gluon.contrib.memcache import MemcacheClient
    cache.memcache = MemcacheClient(request, memcache_servers)
    cache.ram = cache.disk = cache.memcache
elif configuration.get('cache.storage') == 'redis':
    raise NotImplementedError()
