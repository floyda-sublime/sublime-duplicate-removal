#coding:utf-8

import sublime, sublime_plugin
import re

same_lines = set()

def check_content(contents, line):
    for l in contents:
        if l == line:
            global same_lines
            same_lines.add(line)
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
        for line in contents:
            result += line + "\n"

        # insert matched lines to contents
        result += "\n"
        result += "matched lines:\n"
        
        for line in same_lines:
            result += line + "\n"

        # replace contents to current file.
        self.view.replace(edit, region, result)
