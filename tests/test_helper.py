import unittest
import light.helper


class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def test_resolve(self):
        empty = light.helper.resolve('empty')
        self.assertIsNone(empty)

    def test_load_template(self):
        template = light.helper.load_template(name='template', path=light.helper.project_path())

        def func():
            return 'func string'

        self.assertEqual('func string', template.render({'func': func}))

    def test_random_guid(self):
        self.assertEqual(len(light.helper.random_guid()), 4)
        self.assertEqual(len(light.helper.random_guid(4)), 4)
        self.assertEqual(len(light.helper.random_guid(8)), 8)

        self.assertEqual(len(light.helper.random_guid(12, upper=True)), 12)
