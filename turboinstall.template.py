#!/usr/bin/env python3
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
        tmp = re.split('\\s+', line.decode("utf-8"))
        if len(tmp) > 1:
            app = tmp[1]
            break
    output.stdout.close()
    return app

def callO(app):
    output = Popen(app, stdout=PIPE)
    res = output.stdout.read().decode("utf-8")
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
        print(OKGREEN + ' '.join(cmd) + ENDC) # 'shellRun: ' + 
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
{{installScripts}}
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
