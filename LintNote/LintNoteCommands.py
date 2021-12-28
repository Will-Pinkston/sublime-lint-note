import sublime
import sublime_plugin

from datetime import datetime
import os

def date_formatted(fmt): return datetime.now().strftime(fmt)
def date_full(): return date_formatted("%A %d %B %Y")	# Monday 01 January 2000
def date_short(): return date_formatted("%d %b %Y")		# 01 Jan 2000
def date_numeric(): return date_formatted("%Y %m %d")	# 2000 01 01

def getHeading(items={}):
	txt = '#\n'
	for i in items:
		txt += f'# {i}: {items[i]}\n'
	return txt+'#\n'

def move_cursor(curr_view, to_region):
	sel = curr_view.sel()
	sel.subtract(sel[0])
	sel.add(to_region)
	curr_view.show_at_center(to_region)

class LintNewNoteCommand(sublime_plugin.WindowCommand):
	def run( self ):
		self.window.show_input_panel('New note topic', '', lambda x: self.input_done(x), None, None)
		# add a filter to the 'onchange' callback to alert when invalid filename characters are entered?

	def input_done( self, topic ):
		path = 'c:\\Users\\wpinkston\\Documents\\notes' # add a way to change this via settings?
		name = topic if topic not in [None, ''] else 'unnamed'
		filename = f'{path}\\{date_numeric()} {name}.lint'

		with open(filename, 'w') as fp:
			fp.write(getHeading({'Topic': name, 'Date': date_full()}))
		view = self.window.open_file(filename)
		move_cursor(view, sublime.Region(0,7))

class LintRenameSaveCommand(sublime_plugin.WindowCommand):
	def run( self ):
		print('not implemented')
		# save the note's topic into the filename

class LintFocusOpenNoteCommand(sublime_plugin.WindowCommand):
	def run( self ):
		for v in self.window.views():
			if v.file_name() and '.lint' in v.file_name():
				self.window.focus_view(v)
				return
		# no note found -- is there a way to set what folder this 'open' command opens into?
		self.window.run_command('prompt_open_file')

class LintOpenNoteCommand(sublime_plugin.WindowCommand):
	def run( self ):
		print('not implemented')
		# open a note from the ~/Documents/notes folder into whatever project you're currently in
		# ~ maybe use sublime.open_dialog(<callback>,
		#								  <file_types>:[ ('LintNote text files', ['.lint']) ],
		#								  <directory>:'C:\Users\wpinkston\Documents\notes\',
		#								  <multi_select>:false,
		#								  <allow_folders>:false)

class LintInsertHeadingCommand(sublime_plugin.TextCommand):
	def run( self, edit ):
		move_cursor(self.view, sublime.Region(0,0))
		self.view.insert(edit, 0, '\n' + getHeading( {'Topic':'', 'Date':date_full()} ) + '\n')

class LintInsertDateCommand(sublime_plugin.TextCommand):
	def run( self, edit, asHeading=False ):
		txt = date_full()
		if asHeading:
			txt = getHeading({'Date':txt})
		for s in self.view.sel():
			self.view.insert(edit, s.begin(), txt)
		# self.view.set_name('test_buffer_name.lint')

# class LintSaveWrapper(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		# { "keys": ["ctrl+s"], "command": "save", "args": { "async": true } }
# 		if self.view.file_name()[-5:] == '.lint' || :
# 			print('save lint file')
# 		else:
# 			self.view.run_command('save', True)
#		
# 		sels = self.view.sel()
# 		cursor1 = sels[0]
# 		st, ed = cursor1.begin(), cursor1.end()
# 		print(f'{st}, {ed}')
# 		print(self.view.rowcol(st))
# 		# print(self.view.sheet().file_name())
# 		for w in sublime.windows():
# 			print(w)

class LintTestCommand(sublime_plugin.TextCommand):
	def run( self, edit, character ):
		print('test')
		print(character)
		# self.view.run_command('insert', {"characters": character})



# feature wishlist
#
# save current file as a lint note(?)
# -	I've got a scratch file with a few windows shortcuts in it that I'd been keeping open until I learned them
#	after the fourth(or more?) time I referenced it, I decided it should probably go in its own note
#
# change ^l+^o so that repeating ^o cycles through all currently open *.lint note files