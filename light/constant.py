def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f(self)

    return property(fget, fset)


class Const(object):
    @constant
    def SYSTEM_DB(self):
        return 'LightDB'

    @constant
    def SYSTEM_DB_PREFIX(self):
        return 'light'

    @constant
    def SYSTEM_DB_CONFIG(self):
        return 'configuration'

    @constant
    def SYSTEM_DB_VALIDATOR(self):
        return 'validator'

    @constant
    def SYSTEM_DB_I18N(self):
        return 'i18n'

    @constant
    def SYSTEM_DB_STRUCTURE(self):
        return 'structure'

    @constant
    def SYSTEM_DB_BOARD(self):
        return 'board'

    @constant
    def SYSTEM_DB_ROUTE(self):
        return 'route'

    @constant
    def SYSTEM_DB_TENANT(self):
        return 'tenant'
