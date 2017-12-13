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
			[ 'debUrl', 'http://download.teamviewer.com/download/teamviewer_linux.deb' ]
		]
	},
	{
		'app' : 'teamviewer',
		'arch' : ['x86_64'],
		'script' : [
			[ 'debUrl', 'http://download.teamviewer.com/download/teamviewer_linux.deb' ]
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
			[ 'debApt', 'kubuntu-restricted-extras' ],
			[ 'runPost', '/usr/share/doc/libdvdread4/install-css.sh' ]
		],
	},	
	{
		'app': 'ubuntu-restricted-extras',
		'script' : [
			[ 'debApt', 'ubuntu-restricted-extras' ],
			[ 'runPost', '/usr/share/doc/libdvdread4/install-css.sh' ]
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
        {
        }
	## Packets
	{
		'app': 'murdej-bfu',
		'dep': ['apt-upgrade', 'google-chrome', 'skype', 'kde-full', 'teamviewer', 'kubuntu-restricted-extras', 'firefox', 'clementine', 'software-center']
	},
	{
		'app': 'graphics',
		'dep': ['gimp', 'inkscape']
	}
