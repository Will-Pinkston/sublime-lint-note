import sublime
import sublime_plugin
import re


class RegexEscapeCopyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		txt = self.view.substr(self.view.sel()[0])
		pattern = re.compile(r'([\[\].^$*+?{}|()])')
		sublime.set_clipboard( pattern.sub(r'\\' + r'\1', txt) )
		# txt = re.sub(r'[\[\].^$*+?{}|()]')
		# txt = txt.replace('[', '\\[').replace(']','\\]').replace('(', '\\(').replace('')
		# print(txt)

class FixWhitespaceCommand(sublime_plugin.TextCommand):
	tab_pattern = re.compile(f'    ')
	blank_line_pattern = re.compile(f'[ \t]+\n')

	def run(self, edit):
		for region in self.view.sel():
			txt = self.view.substr(region)
			txt = FixWhitespaceCommand.tab_pattern.sub("\t", txt)
			txt = FixWhitespaceCommand.blank_line_pattern.sub("\n", txt)
			self.view.replace(edit, region, txt)