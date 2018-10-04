"""
	jupyter-mysql-kernel
	author:rabin, alain bertrand
"""

class MysqlParser():
	def __init__(self, display, **kwargs):
		if display == 'prettytable':
			self.load = __import__('prettytable')
			self.type = 'prettytable'
		else:
			try:
				self.load = __import__('pandas')
				self.type = 'pandas'
			except ImportError as msg:
				self.load = __import__('prettytable')
				self.type = 'prettytable'

	def pandas(self):
		if self.type == 'pandas':
			return True
		return False

	def format(self, content):
		if self.type == 'pandas':
			content = self.load.DataFrame(content).to_html()
		else:
			content = self.load.from_db_cursor(content).get_html_string()
		return content