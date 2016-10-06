import sys

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

    def get_env_light_db_port(self):
        return 'LIGHTDB_PORT'

    ENV_LIGHT_DB_PORT = property(get_env_light_db_port)

    def get_env_light_db_host(self):
        return 'LIGHTDB_HOST'

    ENV_LIGHT_DB_HOST = property(get_env_light_db_host)

    def get_env_light_db_user(self):
        return 'LIGHTDB_USER'

    ENV_LIGHT_DB_USER = property(get_env_light_db_user)

    def get_env_light_db_pass(self):
        return 'LIGHTDB_PASS'

    ENV_LIGHT_DB_PASS = property(get_env_light_db_pass)

    def get_env_light_db_auth(self):
        return 'LIGHTDB_AUTH'

    ENV_LIGHT_DB_AUTH = property(get_env_light_db_auth)

    def get_env_light_app_port(self):
        return 'PORT'

    ENV_LIGHT_APP_PORT = property(get_env_light_app_port)

    def get_env_light_mysql_port(self):
        return 'LIGHTMYSQL_PORT'

    ENV_LIGHT_MYSQL_PORT = property(get_env_light_mysql_port)

    def get_env_light_mysql_host(self):
        return 'LIGHTMYSQL_HOST'

    ENV_LIGHT_MYSQL_HOST = property(get_env_light_mysql_host)

    def get_env_light_mysql_user(self):
        return 'LIGHTMYSQL_USER'

    ENV_LIGHT_MYSQL_USER = property(get_env_light_mysql_user)

    def get_env_light_mysql_pass(self):
        return 'LIGHTMYSQL_PASS'

    ENV_LIGHT_MYSQL_PASS = property(get_env_light_mysql_pass)

    def get_env_light_app_domain(self):
        return 'APPNAME'

    ENV_LIGHT_APP_DOMAIN = property(get_env_light_app_domain)

    def get_default_tenant(self):
        return 'Default'

    DEFAULT_TENANT = property(get_default_tenant)

    def get_env_light_app_websocket(self):
        return 'LIGHTAPP_WEBSOCKET'

    ENV_LIGHT_APP_WEBSOCKET = property(get_env_light_app_websocket)

    def get_env_light_app_dev(self):
        return 'LIGHTAPP_DEV'

    ENV_LIGHT_APP_DEV = property(get_env_light_app_dev)

    def get_env_light_app_master(self):
        return 'LIGHTAPP_MASTER'

    ENV_LIGHT_APP_MASTER = property(get_env_light_app_master)

    def get_env_light_app_local(self):
        return 'LIGHTAPP_LOCAL'

    ENV_LIGHT_APP_LOCAL = property(get_env_light_app_local)

    def get_valid(self):
        return 1

    VALID = property(get_valid)

    def get_invalid(self):
        return 0

    INVALID = property(get_invalid)

    def get_max_int(self):
        return sys.maxsize

    MAX_INT = property(get_max_int)
