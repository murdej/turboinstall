#!/usr/bin/env python
from subprocess import Popen, PIPE, call
import re, sys, string, os

def findApp(names):
	output = Popen(['whereis'] + names, stdout=PIPE)
	app = None
	for line in output.stdout:
		tmp = re.split('\\s+', line)
		if len(tmp) > 1:
			app = tmp[1]
			break
	output.stdout.close()
	return app

def callO(app):
	output = Popen(app, stdout=PIPE)
	res = output.stdout.read()
	output.stdout.close()
	return res

def findInstallScript(app, arch):
	for isc in installScripts:
		if isc['app'] == app and ('arch' not in isc or arch in isc['arch']):
			return isc
	if arch in archAlternative:
		for archAlt in archAlternative[arch]:
			r = findInstallScript(app, archAlt)
			if r != None:
				return r
	return None

class InstallPlan:
	runPre = []
	debUrl = []
	debApt = []
	runPost = []

def addInstallPlan(app, arch):
	isc = findInstallScript(app, arch)
	if isc == None:
		print 'Can not find app ' + app + ' for architecture ' + arch
		exit()
	else:
		# install deps
		if 'dep' in isc:
			for depApp in isc['dep']:
				addInstallPlan(depApp, arch)
		
		# Only once
		if app not in installPlan['applied'] and 'script' in isc:
			for cmd in isc['script']:
				installPlan[cmd[0]].append(cmd[1:])
		
		installPlan['applied'].append(app)
		print ' ' + app,

def shellRun(cmd):
	print string.join(cmd, ' ') # 'shellRun: ' + 
	if not simulate: call(cmd)

def runInstallPlan():
	# runPre
	for cmd in installPlan['runPre']:
		shellRun(cmd)
	
	# ppaRepo
	for ppa in installPlan['ppaRepo']:
		ppa = ppa[0]
		shellRun(['add-apt-repository', 'ppa:' + ppa])
	
	if len(installPlan['ppaRepo']) + len(installPlan['debRepo']) > 0:
		shellRun(['apt-get', 'update'])
	
	# debApt
	debs = []
	for deb in installPlan['debApt']:
		debs = debs + deb
	if len(debs):
		shellRun(['apt-get', '-y', 'install'] + debs)

	if len(installPlan['debUrl']) > 0:
		tmpdir = '/tmp/turboinstall'
		shellRun(['mkdir', tmpdir])
		for url in installPlan['debUrl']:
			url = url[0]
			fname = os.path.basename(url)
			tmpname = tmpdir + '/' + fname
			shellRun(['wget', '-c', '-O', tmpname, url])
			shellRun(['dpkg', '-i', '--force-depends', tmpname])
		
	for cmd in installPlan['runPost']:
		shellRun(cmd)

## install script

archAlternative = {
	'i686' : ['i386'],
	'i386' : ['all'],
	'x86_64' : ['all']
}

installScripts = [
	## Google Chrome
	{
		'app' : 'google-chrome',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb' ]
		]
	},
	{
		'app' : 'google-chrome',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' ]
		],
	},
	## Skype
	{
		'app' : 'skype',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'http://download.skype.com/linux/skype-ubuntu-precise_4.2.0.13-1_i386.deb' ]
		]
	},
	#todo: 64bit
	## TeamViewer
	{
		'app' : 'teamviewer',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'http://download.teamviewer.com/download/teamviewer_linux.deb' ]
		]
	},
	#todo: 64bit
	## Clementine
	{
		'app' : 'clementine',
		'script' : [
			[ 'ppaRepo', 'me-davidsansome/clementine' ],
			[ 'debApt', 'clementine']
		]
	},
	## Clementine
	{
		'app' : 'firefox',
		'script' : [
			[ 'debApt', 'firefox']
		]
	},

	## Etc
	{
		'app' : 'apt-upgrade',
		'script' : [
			[ 'runPost', 'apt-get', '-y', 'update' ],
			[ 'runPost', 'apt-get', '-y', 'upgrade' ]
		],
	},
	{
		'app': 'kde-full',
		'script' : [
			[ 'debApt', 'kde-full' ]
		],
	},
	{
		'app': 'kubuntu-restricted-extras',
		'script' : [
			[ 'debApt', 'kubuntu-restricted-extras' ]
		],
	},	
	{
		'app': 'gimp',
		'script' : [
			[ 'debApt', 'gimp' ]
		],
	},	
	{
		'app': 'inkscape',
		'script' : [
			[ 'debApt', 'inkscape' ]
		],
	},	
	{
		'app': 'software-center',
		'script' : [
			[ 'debApt', 'software-center' ]
		],
	},	
	## Packets
	{
		'app': 'murdej-bfu',
		'dep': ['apt-upgrade', 'google-chrome', 'skype', 'kde-full', 'teamviewer', 'kubuntu-restricted-extras', 'firefox', 'clementine', 'software-center']
	},
	{
		'app': 'graphics',
		'dep': ['gimp', 'inkscape']
	}
]

	
installPlan = {
	'runPre' : [],
	'ppaRepo' : [],
	'debRepo' : [],
	'debApt' : [],
	'debUrl' : [],
	'runPost' : [],
	'applied' : []
}

simulate = False

## main app code
cmd = sys.argv[1] if len(sys.argv) > 1 else None
# isRoot = len(sys.argv) > 1 and sys.argv[1] == '--root'
# print '---- start ----'
if cmd == '--apps':
	apps = []
	for isc in installScripts:
		if isc['app'] not in apps:
			apps.append(isc['app'])
	print string.join(apps, '\n')
elif cmd == '--root' or cmd == "--sh":
	arch = callO(['uname', '-m']).strip()
	simulate = cmd == "--sh"
	for app in sys.argv[2:]:
		print 'Prepar installing ' + app + ': ',
		addInstallPlan(app, arch)
		print
		
	print installPlan
	runInstallPlan()

else:
	print 'no root'
	apps = ['sudo', 'kdesudo', 'gksudo', 'sudo']
	app = findApp(apps)
	print app
	# call([app, sys.argv[0] + " --root " + string.join(sys.argv[1:])])
	call([app, sys.argv[0], "--root"] + sys.argv[1:])

# print string.join(sys.argv)
# print '---- ok ----'