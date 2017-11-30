from distutils.core import setup
from distutils.command.install import install
from distutils import log

import json
import os
import sys

kernel_json = { 'argv': ['python', '-m' ,'jupyter-mysql-kernel',
						 '-f', '{connection_file}'],
				'display_name': 'Mysql',
				'language': 'mysql',
				}

# this code from bash_kernel made by Thomas Kluyver
# (https://github.com/takluyver/bash_kernel)
class install_with_kernelspec(install):
	def run(self):
		# Regular installation
		install.run(self)

		# Now write the kernelspec
		from IPython.kernel.kernelspec import install_kernel_spec
		from IPython.utils.tempdir import TemporaryDirectory
		with TemporaryDirectory() as td:
			os.chmod(td, 0o755) # Starts off as 700, not user readable
			with open(os.path.join(td, 'kernel.json'), 'w') as f:
				json.dump(kernel_json, f, sort_keys=True)
			# TODO: Copy resources once they're specified

			log.info('Installing IPython kernel spec')
			install_kernel_spec(td, 'jupyter-mysql-kernel', user=self.user, replace=True)

with open('README.md','r') as f:
	readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
	sys.argv.remove(svem_flag)

setup(name='jupyter-mysql-kernel',
	  version='0.0.1',
	  description='A mysql kernel for Jupyter',
	  long_description=readme,
	  author='rabin',
	  author_email='2934170@gmail.com',
	  url='https://github.com/shemic/jupyter-mysql-kernel',
	  packages=['jupyter-mysql-kernel'],
	  cmdclass={'install': install_with_kernelspec},
	  install_requires=['pymysql','prettytable'],
	  classifiers = [
		  'Framework :: IPython',
		  'License :: OSI Approved :: BSD License',
		  'Programming Language :: Python :: 3',
		  'Topic :: System :: Shells',
	  ]
)