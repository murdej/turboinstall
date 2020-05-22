#!/usr/bin/env python
from subprocess import Popen, PIPE, call
import re, sys, string, os

WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'

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
        print()
        print(FAIL + 'Can not find app ' + app + ' for architecture ' + arch + ENDC)
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
        print(' ' + app, end=' ')

def shellRun(cmd):
    if type(cmd) is list :
        print(OKGREEN + string.join(cmd, ' ') + ENDC) # 'shellRun: ' + 
    else:
        print(OKGREEN + cmd + ENDC)
            
    if not simulate: 
        if type(cmd) is list :
            call(cmd)
        else:
            os.system(cmd)

def runInstallPlan():
    # runPre
    for cmd in installPlan['runPre']:
        shellRun(cmd)
    
    # ppaRepo
    for ppa in installPlan['ppaRepo']:
        ppa = ppa[0]
        shellRun(['add-apt-repository', 'ppa:' + ppa])
    
    # debRepo
    for r in installPlan['debRepo']:
        shellRun(['add-apt-repository', r[0]])
        if len(r) > 1 :
            shellRun('wget -q -O - "' + r[1] + '" | apt-key add -')
        
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
	{
		'app' : 'arch-i386',
		'arch' : ['x86_64'],
		'script' : [
			[ 'runPre', 'dpkg', '--add-architecture', 'i386' ]
		]
	},
	## Google Chrome
	{
		'app' : 'google-chrome',
		'title' : 'Google Chrome',
		'category': 'Browser',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb' ]
		]
	},
	{
		'app' : 'google-chrome',
		'category': 'Browser',
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
			# [ 'debUrl', 'http://download.skype.com/linux/skype-ubuntu-precise_4.2.0.13-1_i386.deb' ]
			[ 'debUrl', 'http://download.skype.com/linux/skype-ubuntu-precise_4.3.0.37-1_i386.deb' ]
		]
	},
	{ 
		'app' : 'skype',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'http://download.skype.com/linux/skype-ubuntu-precise_4.3.0.37-1_i386.deb' ]
		],
		'dep': ['arch-i386']
	},

	#todo: 64bit
	## TeamViewer
	{
		'app' : 'teamviewer',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://download.teamviewer.com/download/linux/teamviewer_i386.deb' ]
		]
	},
	{
		'app' : 'teamviewer',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'https://download.teamviewer.com/download/linux/teamviewer_amd64.deb' ]
		],
		'dep' : [ 'arch-i386' ]
	},
	## Clementine
	{
		'app' : 'clementine',
		'script' : [
			[ 'ppaRepo', 'me-davidsansome/clementine' ],
			[ 'debApt', 'clementine']
		]
	},
	## Firefox
	{
		'app' : 'firefox',
		'script' : [
			[ 'debApt', 'firefox']
		]
	},
	## Dropbox
	{
		'app' : 'dropbox',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'https://linux.dropbox.com/packages/ubuntu/dropbox_1.6.0_amd64.deb' ]
		]
	},
	{
		'app' : 'dropbox',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://linux.dropbox.com/packages/debian/dropbox_1.6.0_i386.deb' ]
		]
	},
	## Google earth
	{
		'app' : 'google-earth',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debApt', 'lsb-core' ],
			[ 'debUrl', 'https://dl.google.com/dl/earth/client/current/google-earth-stable_current_amd64.deb' ]
		]
	},
	{
		'app' : 'google-earth',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/dl/earth/client/current/google-earth-stable_current_i386.deb' ]
		]
	},
	## Esmska
	{
		'app' : 'esmska',
		'arch' : ['all'],
		'script' : [
			[ 'debRepo', 'deb http://download.opensuse.org/repositories/Java:/esmska/common-deb/ ./', 'http://download.opensuse.org/repositories/Java:/esmska/common-deb/Release.key' ],
			[ 'debApt', 'esmska' ]
		]
	},
	## Oracle java 8
	{
		'app' : 'oracle-java-8',
		'script' : [
			[ 'ppaRepo', 'webupd8team/java' ],
			[ 'debApt', 'oracle-java8-installer']
		]
	},
	{
		'app' : 'oracle-java',
		'dep' : ['oracle-java-8']
	},
	## GetDeb repository
	{
		'app' : 'rep-getdeb',
		'script' : [
			[ 'debUrl', 'http://archive.getdeb.net/install_deb/getdeb-repository_0.1-1~getdeb1_all.deb' ]
		]
	},
	## Google talk plugin
	{
		'app' : 'google-talk-plugin',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/linux/direct/google-talkplugin_current_i386.deb' ]
		]
	},
	{
		'app' : 'google-talk-plugin',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb' ]
		]
	},
	## Kody (xbmc)
	{
		'title': 'Kody (XBMC)',
		'app': 'kody',
		'script' : [
			[ 'ppaRepo', 'team-xbmc/ppa' ],
			[ 'debApt', 'kodi' ]
		]
	},
	## Kerio VPN Client 
	{
		'app' : 'kerio-vpn-client',
		'title' : 'Kerio VPN Client',
		'arch' : ['i386'],
		'script' : [
			[ 'debUrl', 'http://download.kerio.com/cz/dwn/kerio-control-vpnclient-linux.deb' ]
		]
	},
	## Kerio VPN Client 
	{
		'app' : 'kerio-vpn-client',
		'title' : 'Kerio VPN Client',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'http://download.kerio.com/cz/dwn/kerio-control-vpnclient-linux-amd64.deb' ]
		]
	},
	## Steam
	{
		'app' : 'steam',
		'title' : 'Steam client',
		'script' : [
			[ 'debUrl', 'https://steamcdn-a.akamaihd.net/client/installer/steam.deb' ]
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
			#[ 'runPost', '/usr/share/doc/libdvdread4/install-css.sh' ]
		],
	},	
	{
		'app': 'ubuntu-restricted-extras',
		'script' : [
			[ 'debApt', 'ubuntu-restricted-extras' ],
			#[ 'runPost', '/usr/share/doc/libdvdread4/install-css.sh' ]
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
	{
		'app': 'sweethome3d',
		'dep': [ 'rep-getdeb' ],
		'script' : [
			[ 'debApt', 'sweethome3d' ]
		]
	},
	{
		'app': 'copy-com',
		# 'description': 'Cloud disk\nbla bla bla',
		'script' : [
			[ 'ppaRepo', 'paolorotolo/copy' ],
			[ 'debApt', 'copy' ]
		]
	},
	{
		'app': 'cinnamon',
		'script' : [
			[ 'ppaRepo', 'lestcape/cinnamon' ],
			[ 'debApt', 'cinnamon' ]
		]
	},
	{
		'app': 'wine-latest',
		'dep': [ 'wine-1.8' ] 
	},
	{
		'app': 'wine-1.8',
		'script' : [
			[ 'ppaRepo', 'ubuntu-wine/ppa' ],
			[ 'debApt', 'wine1.8' ],
			[ 'debApt', 'winetricks' ]
		]
	},
	{
		'app': 'vineyard',
		'script' : [
			[ 'ppaRepo', 'cybolic/ppa' ],
			[ 'debApt', 'vineyard' ]
		]
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
if cmd == '--apps' or cmd == None:
    apps = []
    info = {}
    for isc in installScripts:
        appName = isc['app']
        if appName not in apps:
            apps.append(isc['app'])
            info[appName] = { 'title': '', 'description': '' }

        if 'title' in isc:
            info[appName]['title'] = isc['title']

        if 'description' in isc:
            info[appName]['description'] = isc['description']

    apps.sort()
    # print string.join(apps, '\n')
    for appName in apps:
        print(OKBLUE + appName + ENDC + (" - " + info[appName]['title'] if info[appName]['title'] else ''))
        if info[appName]['description']:
            print('\t' + info[appName]['description'].replace('\n', '\n\t'))
            
    # print "Type " + sys.argv[0] + 
    
elif cmd == '--root' or cmd == "--sh":
    arch = callO(['uname', '-m']).strip()
    simulate = cmd == "--sh"
    for app in sys.argv[2:]:
        print(OKBLUE + 'Prepar installing ' + app + ENDC + ': ', end=' ')
        addInstallPlan(app, arch)
        print()
        
    # print installPlan
    runInstallPlan()

else:
    print('You are not root, log as root')
    apps = ['sudo', 'kdesudo', 'gksudo', 'sudo']
    app = findApp(apps)
    # print app
    # call([app, sys.argv[0] + " --root " + string.join(sys.argv[1:])])
    call([app, sys.argv[0], "--root"] + sys.argv[1:])

# print string.join(sys.argv)
# print '---- ok ----'
