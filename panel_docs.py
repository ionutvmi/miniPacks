import sublime, sublime_plugin
import json
import os
from sublimePacks.utils.walk_up import walk_up
from sublimePacks.utils.minify_json import json_minify


class ShowMyDocsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()

        # validate the doc file
        docs_file = self.get_docs_file()

        if not docs_file:
            self.err("No docs found !")
            return

        words = self.get_words()

        # check of we have any word
        if words == []:
            self.err("Nothing is selected !")
            return

        data = self.get_data(docs_file)

        for d in data:
            if self.match_key(d, words[0]):
                window.run_command('write_in_panel', { "text": str(d['content'])})
                return

        self.err("No docs found !")

    def err(self, msg):
        """
        Closes the panel and shows the error in the status bar
        """
        window = self.view.window()
        window.run_command('hide_panel')
        print("\nPANEL DOCS: " + msg + "\n")
        sublime.status_message(msg)

    def match_key(self, d, word):
        """
        Searches the docs for a key to match the word
        """
        if not 'keys' in d:
            return False

        # check of we have a key
        if 'case' in d and d['case']:
            if word not in d['keys']:
                return False
        else:
            # case insensitive
            if word.lower() not in [x.lower() for x in d['keys']]:
                return False


        # check if we match the scope
        if 'scope' in d:
            return bool(self.compare_scope(d['scope']))

        return True

    def get_data(self, f):
        """
        Reads a json file
        """
        data = []
        try:
            file = open(f)
            try:
                txt = json_minify(file.read())
                data = json.loads(txt)
            except ValueError as e:
                self.err("Error json decode: " + str(e))

            file.close()
        except IOError:
            self.err("Error on file open: " + f)

        return data

    def get_words(self):
        """
        Returns the selection or the current word under the caret in ST
        """
        list = []
        # grab the word or the selection from the view
        for region in self.view.sel():
            location = False
            if region.empty():
                # if we have no selection grab the current word
                location = self.view.word(region)
            else:
                # grab the selection
                location = region

            if location and not location.empty():
                list.append(self.view.substr(location))

        return list

    def get_docs_file(self):
        """
        Seaches for paneldocs.json file in the current and parent folders
        """
        for root, dirs, files in walk_up('.'):
            for file in files:
                if file == 'paneldocs.json':
                    return os.path.normpath(root + '/' + file)

        return False

    def compare_scope(self, scope):
        """
        Compares the current scope with the provided one
        """
        if scope is '*':
            return True

        d = self.view.scope_name(self.view.sel()[0].begin())
        return sublime.score_selector(d, scope)

class WriteInPanelCommand(sublime_plugin.TextCommand):
    def run(self, edit, panel_name = 'test', text = ''):
        window = self.view.window()

        v = window.get_output_panel(panel_name)

        v.set_read_only(False)
        v.insert(edit, 0, text + '\n')
        v.set_read_only(True)

        window.run_command("show_panel", {"panel": "output." + panel_name})

# TODO: Web angular app to:
#    - make new docs
#    - edit existing docs
#    - load command (maybe a popup)
#    - have an edit and a read mode
#    - the read mode has a fuzzy search
#    - use select2 tags for keys

