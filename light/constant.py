class Const(object):
    def get_system_db(self):
        return 'LightDB'

    SYSTEM_DB = property(get_system_db)

    def get_system_db_prefix(self):
        return 'light'

    SYSTEM_DB_PREFIX = property(get_system_db_prefix)

    def get_system_db_config(self):
        return 'configuration'

    SYSTEM_DB_CONFIG = property(get_system_db_config)

    def get_system_db_validator(self):
        return 'validator'

    SYSTEM_DB_VALIDATOR = property(get_system_db_validator)

    def get_system_db_i18n(self):
        return 'i18n'

    SYSTEM_DB_I18N = property(get_system_db_i18n)

    def get_system_db_structure(self):
        return 'structure'

    SYSTEM_DB_STRUCTURE = property(get_system_db_structure)

    def get_system_db_board(self):
        return 'board'

    SYSTEM_DB_BOARD = property(get_system_db_board)

    def get_system_db_route(self):
        return 'route'

    SYSTEM_DB_ROUTE = property(get_system_db_route)

    def get_system_db_tenant(self):
        return 'tenant'

    SYSTEM_DB_TENANT = property(get_system_db_tenant)
