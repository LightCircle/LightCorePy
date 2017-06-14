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

    def test_ansi_color_to_black(self):
        s = 'stream "\x1b[91m../vendor/libxml/encoding.c:2856:12\x1b[0m"'
        o = light.helper.ansi_color_to_black(s)
        self.assertEqual('stream "../vendor/libxml/encoding.c:2856:12"', o)

    def test_file_md5(self):
        o = light.helper.file_md5('./__init__.py')
        self.assertEqual('d41d8cd98f00b204e9800998ecf8427e', o)
