"""
Open a program in the directory of the current file
"""
import os, sublime, sublime_plugin
def _(*args):
    pass

class StartProgramCommand(sublime_plugin.TextCommand):
    def run(self, edit, program = 'cmd'):
        if program:
            self.start_program(program)
        else:
            v = sublime.active_window().show_input_panel("Start", "powershell", self.start_program, _, _)
            v.sel().clear()
            v.sel().add(sublime.Region(0, v.size()))

    def start_program(self, program):
        file_name = self.view.file_name()
        directory = os.path.dirname(file_name)
        driver = os.path.splitdrive(file_name)[0]

        command= "cd "+ directory +" & "+ driver +" & start %s" % program
        os.system(command)


