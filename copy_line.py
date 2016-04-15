# Based on to http://stackoverflow.com/a/25345286/1579481
"""
Copy a line by number where the cursor is
Example inputs:
    For a single line: 25
    For line 25 and next 2 lines: 25:2
    For line 25 till 27: 25-27
"""

import sublime_plugin
import re

_line = re.compile('^\d+$')
_line_next = re.compile('^\d+\:\d+$')
_line_between = re.compile('^\d+\-\d+$')


class PromptCopyLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # prompt for the line # to copy
        self.view.window().show_input_panel(
            "Enter the line you want to copy: ",
            '',
            self.on_done,  # on_done
            None,          # on_change
            None           # on_cancel
        )

    def on_done(self, input):

        # single line
        if _line.match(input):
            self.paste_line(input)
        # line and next
        elif _line_next.match(input):
            lines = input.split(':')
            lines[0] = int(lines[0])
            lines[1] = int(lines[1])

            tmp = ''
            for i in range(lines[1] + 1):
                ln = lines[0] + i
                if self.is_valid_line(ln):
                    tmp += self.get_line_content(ln) + '\n'

            self.view.run_command(
                "paste_line", {"string": tmp, "newLine": False}
                )

        # between lines
        elif _line_between.match(input):
            lines = input.split('-')
            lines[0] = int(lines[0])
            lines[1] = int(lines[1])

            tmp = ''
            for i in range(lines[0], lines[1] + 1):
                if self.is_valid_line(i):
                    tmp += self.get_line_content(i) + '\n'

            self.view.run_command(
                "paste_line", {"string": tmp, "newLine": False}
                )

        else:
            self.view.run_command('prompt_copy_line')

    def is_valid_line(self, numLine):
        # NOL is the number of line in the file
        NOL = self.view.rowcol(self.view.size())[0] + 1
        # if the line # is not valid
        # e.g. 0 or less, or more that the number of line in the file
        if numLine < 1 or numLine > NOL:
            return False
        else:
            return True

    def get_line_content(self, line):
        # retrieve the content of numLine
        view = self.view
        point = view.text_point(line-1, 0)
        return view.substr(view.line(point))

    def paste_line(self, numLine):
        # make sure we have a valid line
        try:
            numLine = int(numLine)
        except ValueError:
            numLine = 0

        if not self.is_valid_line(numLine):
            self.view.run_command('prompt_copy_line')
            return

        # do the actual copy
        self.view.run_command(
            "paste_line", {"string": self.get_line_content(numLine)}
            )


class PasteLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, string, newLine=True):
        # retrieve current offset
        current_pos = self.view.sel()[0].begin()
        # retrieve current line number
        CL = self.view.rowcol(current_pos)[0]
        # retrieve offset of the BOL
        offset_BOL = self.view.text_point(CL, 0)

        if newLine:
            string += '\n'

        self.view.insert(edit, offset_BOL, string)
