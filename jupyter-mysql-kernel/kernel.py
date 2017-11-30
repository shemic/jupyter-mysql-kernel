"""
	jupyter-mysql-kernel
	author:rabin
"""
from ipykernel.kernelbase import Kernel
from .parser import MysqlParser
import os.path
import sys
import re
import pymysql
import json

__version__ = '0.0.1'

version_pat = re.compile(r'version (\d+(\.\d+)+)')

class MysqlKernel(Kernel):
	implementation = 'jupyter-mysql-kernel'
	implementation_version = __version__

	@property
	def language_version(self):
		m = version_pat.search(self.banner)
		return m.group(1)

	_banner = None

	@property
	def banner(self):
		if self._banner is None:
			self._banner = 'mysql kernel'
		return self._banner

	language_info = {'name': 'mysql',
					 'mimetype': 'text/x-sh',
					 'file_extension': '.sql'}

	mysql_setting_file = os.path.join(os.path.expanduser('~'), '.local/config/mysql_config.json')
	mysql_config = {
		'user'	  : 'root'
		,'host'	  : '192.168.15.10'
		,'port'	  : '3309'
		,'charset'   : 'utf8'
		,'password'  : '123456'
	}

	def __init__(self, **kwargs):
		Kernel.__init__(self, **kwargs)
		if os.path.exists(self.mysql_setting_file):
			with open(self.mysql_setting_file,"r") as f:
				self.mysql_config.update(json.load(f))
		self.parser = MysqlParser()
		self.connect()

	def connect(self):
		if self.parser.pandas():
			cursorclass = pymysql.cursors.DictCursor
		else:
			cursorclass = pymysql.cursors.Cursor
		try:
			self.connect = pymysql.connect(host=self.mysql_config['host'], port=int(self.mysql_config['port']), user=self.mysql_config['user'], charset=self.mysql_config['charset'], passwd=self.mysql_config['password'], cursorclass=cursorclass)
			self.cursor = self.connect.cursor()
		except Exception:
			self.connect = False

	def execute(self, sql):
		if self.connect:
			self.cursor.execute(sql)

	def fetchall(self):
		if self.connect:
			if self.parser.pandas():
				return self.cursor.fetchall()
			else:
				return self.cursor
		return False

	def commit(self):
		if self.connect:
			self.connect.commit()

	def output(self, output):
		if not self.silent:
			if type(output) != str:
				output = self.parser.format(output)
			display_content = {
				'source': 'kernel',
				'data': {
					'text/html': output
				}, 'metadata': {}
			}
			self.send_response(self.iopub_socket, 'display_data', display_content)

	def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
		self.silent = silent
		if not code.strip():
			return self.ok()
		if not self.connect:
			msg = 'Unable to connect to Mysql server. Check that the server is running.'
			self.output(msg)
			return self.err(msg)

		sql = code.rstrip()
		output = ''
		try:
			for v in sql.split("\n"):
				v = v.rstrip()
				if len(v) > 0:
					if v[0] == "#":
						continue
					self.execute(v)
					if 'select' in v or 'show' in v:
						output = self.fetchall()
					else:
						self.commit()
						output = 'yes'
			self.output(output)
			return self.ok()
		except Exception as msg:
			self.output(format(msg))
			return self.err('Error executing code ' + sql)

	def ok(self):
		return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

	def err(self, msg):
		return {'status': 'error', 'error' : msg, 'traceback': [msg], 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
