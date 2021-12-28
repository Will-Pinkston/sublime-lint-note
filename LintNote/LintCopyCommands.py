import sublime
import sublime_plugin

import os
import re


# design goal: a vim-like ultra-terse syntax typing out exactly what information I want to copy to the clipboard
# I'll probably just assign a letter/string to each of the different possible data points
#
# something like: `^l^+c` [begin recording input ~ show current input in a tooltip?] `:n c ^c` [save ':n c' as input]
# n := line number
# c := line contents (without leading or trailing whitespace)
# f := filename
# F := filename with full path

## data getters
def line_number(view, point):
	return view.rowcol(point)[0] + 1

def line_content(view, point):
	return view.substr( view.line(point) ).strip()

def file_name(view, kind='short'):
	if view.file_name():
		if kind == 'short':
			return view.file_name().split(os.path.sep)[-1]
		elif kind == 'full':
			return view.file_name()
	else:
		return "untitled"

## command manip
def build_output(view, cmd_fmt):
	output = ''
	line_points = [region.begin() for region in view.sel()]
	for pt in line_points:
		output += cmd_fmt.format(
			line_number = line_number(view,pt),
			line_content = line_content(view,pt),
			filename = file_name(view),
			full_filename = file_name(view, 'full')
		)
	return output

def build_fmt(cmd):
	cmd = re.sub('n', '{line_number}', cmd)
	cmd = re.sub('c', '{line_content}', cmd)
	cmd = re.sub('f', '{filename}', cmd)
	cmd = re.sub('F', '{full_filename}', cmd)
	return cmd


#add command / option to append to clipboard via view.get_clipboard_async( lambda cb: view.set_clipboard(cb + build_output(view, command)) )

class LintFancyCopyCommand(sublime_plugin.TextCommand):
	def run( self, edit, command ):
		sublime.set_clipboard(build_output(self.view, command))


class LintTerseCopyPromptCommand(sublime_plugin.TextCommand):
	def run( self, edit ):
		self.view.window().show_input_panel('LintTerseCopy command', '', lambda cmd: self.done(cmd), None, None)

	def done( self, cmd ):
		sublime.set_clipboard( build_output(self.view, build_fmt(cmd)) )

# wishlist
#
# add a way to save a 'current' command format. ^l^c is then overridden to use that until
# an empty command is entered, then it goes back to the default `:n c` command (kind of like a macro)
#
# more robust handling for filenames and file paths
# especially, a way of getting a files path from project root
#
# handle specific text selections (including multiline), use '..' to show when some of the line's code (not counting whitespace) has been omitted
# single line:
#	:{line_number} ..{selected contents}..
# multiline:
#	:{line_number}	|..{selected contents}
#				  	|  {line_content}
#					|  ... (for each interior line in the selection)
#	:{line_number}	|  {selected contents}..
#
# handle copying function signatures
# in: function func_name($param1, $param2, $param3="default value")
# out: function func_name(	<$param1>:{input value placeholder},
#							<$param2>:{input value placeholder},
#							<$param3="default value">:{input value placeholder} )
# if there's a way to make the {input valuye placeholder}'s easily selectable/replaceable like with snippets that would be awesome
#
# for multiline selection, provide syntax to just grab line number region: `:{start_line_number}-{end_line_number}`