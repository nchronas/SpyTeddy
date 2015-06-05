# starts an AP with ssid and psk given
# usage python setup_ap.py <ssid> <psk>

import os
import sys
import dbus
import time
import subprocess

# from ENV or default
ssid = os.environ.get('SSID', 'ResinAP')
psk = os.environ.get('PASSPHRASE', '12345678')

tech_type = 'wifi'
path = '/net/connman/technology/' + tech_type
try:
	bus = dbus.SystemBus()

	tech = dbus.Interface(bus.get_object('net.connman', path), 'net.connman.Technology')

	if tech == None:
		print '* no %s technology available' % tech_type
	        sys.exit(1)

	properties = tech.GetProperties()

	if properties['Tethering']:
	    print '* interface already tethering. Resetting'
	    tech.SetProperty('Tethering', dbus.Boolean(0))
	    # FIXME: If we don't wait connman complains later.
	    # We should be listening for events instead of waiting
	    # a fixed amount of time
	    time.sleep(10)

	print '* setting SSID to: %s' % (ssid)
	tech.SetProperty('TetheringIdentifier', ssid)

	print '* setting Passphrase to: %s' % (psk)
	tech.SetProperty('TetheringPassphrase', psk)

	print '* enabling tethering on %s' % tech_type
	tech.SetProperty('Tethering', dbus.Boolean(1))

	# setup captive portal using iptables
	# 8080 - port of the local web server where users would be redirected
	print '* setting up captive portal redirect'

	#sleep 10
	time.sleep(10)

	subprocess.call(['/app/setup-iptables.sh', 'ADD', '8080'])

	print '* done starting AP'

	sys.exit(0)

except dbus.exceptions.DBusException:
	print 'Unable to complete:', sys.exc_info()
	sys.exit(1)