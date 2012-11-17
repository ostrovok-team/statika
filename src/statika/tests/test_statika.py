from logging import StreamHandler
from os import path, remove
from unittest import TestCase
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from statika import build, logger


logger_output = StringIO()
logger.addHandler(StreamHandler(logger_output))


class BaseCase(TestCase):

    static_dir = path.abspath(path.join(path.dirname(__file__), 'static'))
    css_bundle = path.join(static_dir, 'test.css')
    js_bundle = path.join(static_dir, 'test.js')
    bundles = (css_bundle, js_bundle)

    def _bundle(self, bundle):
        return '%s/_%s' % (path.dirname(bundle), path.basename(bundle))

    def setUp(self):
        build(self.bundles)

    def tearDown(self):
        for bundle in self.bundles:
            filename = self._bundle(bundle)
            if path.isfile(filename):
                remove(filename)


class TestStatika(BaseCase):

    def test_files(self):
        for bundle in self.bundles:
            self.assertTrue(path.isfile(self._bundle(bundle)))
        self.assertEqual(logger_output.getvalue(), '')

    def test_css(self):
        block_css = open(
            path.join(self.static_dir, 'b-test', 'b-test.css'), 'rb'
        ).read()
        bundle_content = open(self._bundle(self.css_bundle), 'rb').read()
        self.assertIn(block_css, bundle_content)
        self.assertEqual(logger_output.getvalue(), '')

    def test_js(self):
        block_js = open(
            path.join(self.static_dir, 'b-test', 'b-test.js'), 'rb'
        ).read()
        bundle_content = open(self._bundle(self.js_bundle), 'rb').read()
        self.assertIn(block_js, bundle_content)
        self.assertEqual(logger_output.getvalue(), '')
