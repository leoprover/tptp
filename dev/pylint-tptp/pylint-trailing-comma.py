import astroid
import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker, IRawChecker

class TrailingCommaChecker(BaseChecker):
    __implements__ = (IRawChecker, IAstroidChecker, )

    # Costom section of the config for this checker.
    name = "multiline-trailing-comma"
    # The order that pylint will run the checkers.
    priority = -1
    # Messages (ie the warnings and errors) that the checker can emit.
    msgs = {
        # 'displayed-message', 'message-symbol', 'message-help'
        'C9900': (
            'Missing trailing dictionary comma.',
            'no-dict-trailing-comma',
            'Multiline Dicts should have a trailing comma.'
        ),
        'C9901': (
            'Missing trailing args comma.',
            'no-args-trailing-comma',
            'Multiline Arguments lists should have a trailing comma.'
        ),
        'C9901': (
            'Missing trailing list comma.',
            'no-list-trailing-comma',
            'Multiline Lists lists should have a trailing comma.'
        )
    }
    options = ()

    _lines = {}
    def process_module(self, node):
        """
        Fetch all lines, s.t. we can use them in visit_dict.
        """
        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                self._lines[lineno] = line

    def visit_dict(self, node):
        # no children
        if not node.items:
            return
        # not at least 2 children
        if len(node.items) < 2:
            return
        # ignore one liner
        if node.lineno == node.tolineno:
            return

        lineno_end_of_last_entry = node.last_child().tolineno

        last_line = self._lines[lineno_end_of_last_entry - 1].decode('utf-8')
        if re.search(r",\s+$", last_line):
            return 
        self.add_message('no-dict-trailing-comma', line=lineno_end_of_last_entry)

def register(linter):
    """
    This required method auto registers the checker.
    """
    linter.register_checker(TrailingCommaChecker(linter))