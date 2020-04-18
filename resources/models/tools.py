# -*- coding: utf-8 -*-

class safeio(object):
    """
    Usage:

        - {{}}

        - @auth.requires(safeio.verify(), requires_login=False)

    """

    @staticmethod
    def cfg(hmac_key=None, salt=None):
        try:
            safeioconf
        except NameError:
            return vars()
        else:
            return dict(
                hmac_key = safeioconf.get('hmac_key') if hmac_key is None else hmac_key,
                salt = safeioconf.get('salt') if salt is None else salt
            )

    @classmethod
    def url(cls, *args, hmac_key=None, salt=None, **kwargs):
        """ """
        return URL(
            *args,
            **dict(kwargs, **cls.cfg(hmac_key, salt))
        )

    @classmethod
    def verify(cls, hmac_key=None, salt=None, **kwargs):
        return URL(
            request,
            **dict(kwargs, **cls.cfg(hmac_key, salt))
        )
