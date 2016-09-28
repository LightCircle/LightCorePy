from light.cache import Cache
from light.constant import Const

CONST = Const()
I18N_INSTANCE = None


class I18n(object):
    def __init__(self):
        self.catalog = Cache.instance().get(CONST.SYSTEM_DB_I18N)
        self._lang = 'zh'

    def i(self, key):
        index = key.find('.')
        lang_type = key[:index]
        lang_key = key[index + 1:]

        item = next((item for item in self.catalog if item['key'] == lang_key and item['type'] == lang_type), {})
        if 'lang' not in item:
            return lang_key

        if self._lang not in item['lang']:
            return lang_key

        return item['lang'][self._lang]

    def set_lang(self, lang):
        self._lang = lang

    lang = property(fset=set_lang)

    @staticmethod
    def instance():
        global I18N_INSTANCE

        if not I18N_INSTANCE:
            I18N_INSTANCE = I18n()

        return I18N_INSTANCE
