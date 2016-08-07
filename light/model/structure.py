from light.cache import Cache
from light.constant import Const

CONST = Const()
STRUCTURE_INSTANCE = None


class Structure(object):
    def __init__(self):
        structures = Cache.instance().get(CONST.SYSTEM_DB_STRUCTURE)

        for structure in structures:
            setattr(self, structure['schema'], structure)

    @staticmethod
    def instance():
        global STRUCTURE_INSTANCE

        if not STRUCTURE_INSTANCE:
            STRUCTURE_INSTANCE = Structure()

        return STRUCTURE_INSTANCE
