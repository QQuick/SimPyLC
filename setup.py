import os

from setuptools import setup

import SimPyLC as sp

def read (*paths):
	with open (os.path.join (*paths), 'r') as aFile:
		return aFile.read()

setup (
	name = 'SimPyLC',
	version = sp.base.programVersion,
	description = 'SimPyLC PLC simulator, after its C++ big brother that has controlled industrial installations for more than 20 years now. ARDUINO CODE GENERATION ADDED!',
	long_description = (
		read ('README.rst') + '\n\n' +
		read ('qQuickLicense.txt')
	),
	keywords = ['PLC', 'Arduino','simulator', 'SimPyLC', 'emulator', 'GEATEC', 'opy', 'eden'],
	url = 'http://www.qquick.org/educational',
	license = 'qQuickLicence',
	author = 'Jacques de Hooge',
	author_email = 'jacques.de.hooge@qquick.org',
	packages = ['SimPyLC'],	
	include_package_data = True,
	install_requires = [],
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: Other/Proprietary License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6'
	],
)
