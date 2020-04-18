# -*- coding: utf-8 -*-

# DOC
# http://web2py.com/books/default/chapter/29/09/access-control#Customizing-Auth
# Using extra_fields after the auth object definition is the recommended way to
# customize Auth db model as it will not break any internal mechanism.

if 'auth' in vars():
    try:
        assert custom_auth_table_definition_required
    except (NameError, AssertionError,):
        pass
    else:
        auth_define_table()

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer if 'auth' in vars() else Mail()
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')
