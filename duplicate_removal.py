
import sublime, sublime_plugin
import re

same_lines = None

def check_content(contents, line):
    for l in contents:
        if l == line:
            global same_lines
            same_lines.add(line)
            contents.remove(l)
            return False
    return True


def filter_line(line):
    line = re.sub("^ +", "", line)
    line = re.sub(" +$", "", line)
    return line


def insert_content(contents, line):
    line = filter_line(line)
    if check_content(contents, line) and len(line) > 0:
        contents.append(line)


def add_comment(result, comment):
    result += "-" * 60 + "\n"
    result += comment + "\n"
    result += "-" * 60 + "\n"
    return result


class DuplicateRemovalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global same_lines
        same_lines = set()

        # get content of current file.
        size = self.view.size()
        region = sublime.Region(0, size)
        substr = self.view.substr(region)

        # parse content
        contents = []
        _line = ""
        index = 0
        while index < len(substr):
            char = substr[index]
            if char is '\n':
                insert_content(contents, _line)
                _line = ""
            else:
                _line += char

            index += 1

        insert_content(contents, _line)

        # insert resule to contents
        result = ""
        result = add_comment(result, "The Diff Lines")
        for line in contents:
            result += line + "\n"

        jump_point = len(result)

        # insert matched lines to contents
        if len(same_lines) > 0:
            result += "\n"
            result = add_comment(result, "The Same Lines")
            for line in same_lines:
                result += line + "\n"

        # replace contents to current file.
        self.view.replace(edit, region, result)

        # jump to end of diff lines
        self.view.show(jump_point, False)
        sels = self.view.sel()
        sels.clear()
        region = sublime.Region(jump_point, jump_point)
        sels.add(region)
