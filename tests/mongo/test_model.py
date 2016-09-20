import os
import unittest
from datetime import datetime

from light.mongo.model import Model
from light.constant import Const
from bson.objectid import ObjectId

CONST = Const()


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'localhost'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '27017'
        # os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        # os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

    def test_add(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.add(
            {'schema': 'a',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2003/01/01'}, {'date': '2004/01/01'}]}]}],
             'valid': '1'}
        ))
        print(model.add(
            {'schema': 'b',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2005/01/01'}, {'date': '2006/01/01'}]}]}],
             'valid': '2'}
        ))
        print(model.add(
            {'schema': 'c',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2007/01/01'}, {'date': '2008/01/01'}]}]}],
             'valid': '3'}
        ))
        print(model.add(
            {'schema': 'd',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2009/01/01'}, {'date': '2010/01/01'}]}]}],
             'valid': '4'}
        ))
        print(model.add([
            {'schema': 'e',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2003/01/01'}, {'date': '2004/01/01'}]}]}],
             'valid': '5'},
            {'schema': 'e',
             'nestsii': [{'fields': [{'nestarray': [{'date': '2003/01/01'}, {'date': '2004/01/01'}]}]}],
             'valid': '5'}
        ]))

    def test_get(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.get({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}))
        print(model.get('57e0b76f1d41c81776ced8ca'))
        print(model.get(ObjectId('57e0b76f1d41c81776ced8ca')))
        print(model.get({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}, 'valid'))
        print(model.get({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}, {'valid': 1, 'schema': 1}))

    def test_get_by(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.get_by({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}))
        print(model.get_by({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}, 'valid'))
        print(model.get_by({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}, {'valid': 1, 'schema': 1}))

    def test_update_by(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.update_by({'valid': 5}, {'$inc': {'valid': 3}}))
        print(model.update_by('57e0b76f1d41c81776ced8ca', {'$inc': {'valid': 30}}))
        print(model.update_by(ObjectId('57e0b76f1d41c81776ced8ca'), {'$inc': {'valid': 30}}))

    def test_remove_by(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.remove_by({'nestsii.fields.nestarray.date': datetime(2005, 1, 1, 0, 0)}))
        print(model.remove_by('57e0b76f1d41c81776ced8cc'))
        print(model.remove_by(ObjectId('57e0b76f1d41c81776ced8cc')))

    def test_increment(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.increment({'valid': 3}, {'$inc': {'valid': 2}}))
        print(model.increment('123457791d41c817b4a09b37', {'$inc': {'valid': 57}}))
        print(model.increment(ObjectId('678907791d41c817b4a09b37'), {'$inc': {'valid': 68}}))

    def test_distinct(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        print(model.distinct('valid'))
        print(model.distinct('valid', {'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}))

    def test_total(self):
        model = Model('LightDB', 'light', 'unittest', self.define)
        self.assertGreater(model.total({'nestsii.fields.nestarray.date': datetime(2003, 1, 1, 0, 0)}), 3)

    def test_write_file_to_grid(self):
        in_file = 'test_model.py'
        out_file = in_file + '.temp'
        model = Model('LightDB')

        result = model.write_file_to_grid(in_file)

        result = model.read_file_from_grid(result['fileId'], out_file)
        self.assertEqual(in_file, result['name'])
        self.assertTrue(os.path.isfile(out_file))
        os.remove(out_file)

    def test_write_stream_to_grid(self):
        in_file = 'test_model.py'
        out_file = in_file + '.temp'

        model = Model('LightDB')

        f = open(in_file, 'rb')
        result = model.write_stream_to_grid(in_file, f, 'text/x-python')
        f.close()

        result = model.read_stream_from_grid(result['fileId'])
        f = open(out_file, 'wb')
        f.write(result['fileStream'])
        f.close()

        self.assertEqual(in_file, result['name'])
        self.assertTrue(os.path.isfile(out_file))
        os.remove(out_file)

    def setUp(self):
        self.define = {
            # ObjectID type
            '_id': {
                'reserved': 1,
                'type': 'ObjectID',
                'name': 'ID'
            },
            # Number type
            'valid': {
                'reserved': 1,
                'type': 'Number',
                'name': '有效标识',
                'description': '1:有效 0:无效'
            },
            # Boolean type
            'flag': {
                'reserved': 1,
                'type': 'Boolean',
                'name': 'Flag'
            },
            # Date type
            'createAt': {
                'reserved': 1,
                'type': 'Date',
                'name': '创建时间'
            },
            # String type
            'schema': {
                'type': 'String',
                'name': 'Schema名',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array basic type
            'fields': {
                'type': 'Array',
                'name': '附加项 关联后选择的字段',
                'default': '',
                'description': '',
                'reserved': 2,
                'contents': 'String'
            },
            # Array Object type
            'general': {
                'type': 'Array',
                'name': '附加项 关联后选择的字段',
                'default': '',
                'description': '',
                'reserved': 2,
                'contents': 'Object'
            },
            # Array type
            'selects': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': 'String'
                    },
                    'valid': {
                        'reserved': 1,
                        'type': 'Number',
                        'name': '有效标识',
                        'description': '1:有效 0:无效'
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array-Nest type
            'nests': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': {
                            'valid': {
                                'reserved': 1,
                                'type': 'Number',
                                'name': '有效标识',
                                'description': '1:有效 0:无效'
                            },
                            'nestins': {
                                'type': 'String',
                                'name': '嵌套',
                                'default': '',
                                'description': '',
                                'reserved': 2
                            },
                            'nestarray': {
                                'type': 'Array',
                                'name': '附加项 关联后选择的字段',
                                'default': '',
                                'description': '',
                                'reserved': 2,
                                'contents': 'String'
                            }
                        }
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array-Nest-II type
            'nestsii': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': {
                            'nestarray': {
                                'type': 'Array',
                                'name': '附加项 关联后选择的字段',
                                'default': '',
                                'description': '',
                                'reserved': 2,
                                'contents': {
                                    'date': {
                                        'type': 'Date',
                                        'name': '备份截止日',
                                        'default': '',
                                        'description': '',
                                        'reserved': 2
                                    }
                                }
                            }
                        }
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Object type
            'limit': {
                'contents': {
                    'date': {
                        'type': 'Date',
                        'name': '备份截止日',
                        'default': '',
                        'description': '',
                        'reserved': 2
                    },
                    'count': {
                        'type': 'Number',
                        'name': '备份次数',
                        'default': '',
                        'description': '',
                        'reserved': 2
                    }
                },
                'type': 'Object',
                'name': '限制',
                'default': '',
                'description': '',
                'reserved': 2
            }
        }
