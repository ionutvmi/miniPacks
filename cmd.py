"""
Open cmd in the directory of the current file
"""
import os, sublime_plugin
class CmdCommand(sublime_plugin.TextCommand):
    def run(self, edit, powershell = False):
        file_name=self.view.file_name()
        path=file_name.split("\\")
        current_driver=path[0]
        path.pop()
        current_directory="\\".join(path)
        cmd = 'cmd'
        if powershell:
            cmd = 'powershell'
        command= "cd "+current_directory+" & "+current_driver+" & start %s" % cmd
        os.system(command)

