#coding:utf-8

import sublime, sublime_plugin
import re

def check_content(contents, line):
    for l in contents:
        if l == line:
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
        # get content of current file.
        size = self.view.size()
        region = sublime.Region(0, size)
        substr = self.view.substr(region)

        # parse content
        contents = []
        _line = ''
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

        # replace the parsed result to current file.
        result = ""
        for line in contents:
            result += line + "\n"
        self.view.replace(edit, region, result)
