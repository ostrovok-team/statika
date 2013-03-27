from logging import getLogger
from os import path


logger = getLogger('statika')


class BuildError(Exception):
    pass


class MediaBundle(object):
    INCLUDE_SEP = {'=', '(', '"', "'"}
    _current_path = None  # Dirname of file which is processing at the moment.

    def __init__(self, file_path):
        self.file_path = file_path
        self.root_dir = path.dirname(file_path)
        self.type = path.splitext(file_path)[1].strip('.')
        if self.type not in ('js', 'css'):
            raise NotImplementedError(
                'Not supported bundle type "%s"' % self.type
            )

    def generate(self, rules=None):
        if rules is None:
            rules = DEFAULT_RULES
        self._rules = rules
        for rule in rules:
            assert 'type' in rule, \
                'Value with "type" key must be specified in "rule"'
            assert 'instruction' in rule, \
                'Value with "instruction" key must be specified in "rule"'
            assert 'handler' in rule, \
                'Value with "handler" key must be specified in "rule"'

        with open(self._name(self.file_path), 'wb') as dst:
            dst.write(self.process_file(self.file_path))

    def process_file(self, file_path):
        if not path.isfile(file_path):
            raise BuildError(
                'Non existent file "%s" is specified' % file_path
            )

        res = ''
        old_path = self._current_path
        self._current_path = path.dirname(file_path)
        with open(file_path, 'rb') as src:
            line_no = 1
            for line in src.readlines():
                _line = line.strip()
                for rule in self._rules:
                    if rule['type'] != self.type:
                        continue
                    if _line.find(rule['instruction']) == 0:
                        # Remove instruction text from the line.
                        _line = _line.replace(rule['instruction'], '', 1). \
                            strip()
                        # Next symbol after instruction must be space
                        # or an opening bracket in JavaScript; space or quote
                        # in CSS.
                        if not len(_line) or _line[0] not in self.INCLUDE_SEP:
                            continue
                        _line = _line.strip(' ')
                        # Skip lines with equal sign after instruction.
                        if not len(_line) or _line[0] == '=':
                            continue

                        args = self._get_args(_line, rule['instruction'])
                        try:
                            line = rule['handler'](
                                self, rule['instruction'], args
                            )
                        except BuildError as e:
                            logger.error(
                                str(e) + ' in %s on line %s' % (
                                    self.file_path, line_no
                                )
                            )
                        break
                res += line
                line_no += 1
        self._current_path = old_path
        return res

    @staticmethod
    def _name(file_path):
        """
        Returns almost the same file's path, but with underscore character
        between file's base name. E.g. /tmp/bundle.js -> /tmp/_bundle.js.
        """
        return path.join(
            path.dirname(file_path),
            '_' + path.basename(file_path)
        )

    @staticmethod
    def _get_args(line, instruction):
        """
        Returns arguments of language's instruction extracted from line
        of a code. It has bad implemetation because arguments can contain
        a comma. But is is really fast.
        """
        return [
            a.strip(' "\'')
            for a in line.strip('();').split(',')
        ]


def handler_include(bundle, instruction, args):
    """
    :raise exception: BuildError
    """
    try:
        inc_file = path.join(bundle._current_path, args[0])
    except IndexError:
        raise BuildError(
            'File name must be specified by the first argument of %s' % \
            instruction
        )
    return bundle.process_file(inc_file)


DEFAULT_RULES = [
    {'type': 'js', 'instruction': 'include', 'handler': handler_include},
    {'type': 'css', 'instruction': '@import', 'handler': handler_include},
]


def build(bundles, rules=None):
    """
    Builds list of "bundles" sequentially according with "rules".
    Bundles should be a list of a full path to JS or CSS files with includes.
    By default rules are (if no rules were passed):
      - include('b-test/b-test.js') for JavaScript;
      - @import 'b/test/b-test.css' for CSS.
    """
    if rules is None:
        rules = DEFAULT_RULES
    for bundle_file in bundles:
        bundle = MediaBundle(bundle_file)
        bundle.generate(rules)
