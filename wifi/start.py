import os
import sys
import pyconnman
import dbus
import time
import pprint
import subprocess
import dbus.mainloop.glib
import gobject
import pickle

server_started = False

def start_server():
	print '* starting web server'
	p = subprocess.Popen(['python', '/app/server.py'])


#ConnManager.SIGNAL_SERVICES_CHANGED event handler
def on_scan_done(signal, callback, *args):
	# print '\n========================================================='
	# print '>>>>>', signal, '<<<<<'
	# print args
	# print '========================================================='

	print '* got SIGNAL_SERVICES_CHANGED event'

	#manager.remove_signal_receiver(pyconnman.ConnManager.SIGNAL_SERVICES_CHANGED)

	callback()

#called by on_scan_done
#when scan is done, this event is triggered, wireless networks available can be saved
def get_services():
	global server_started
	services = manager.get_services()

	wireless_networks = {}
	wireless_ssids = ''

	for i in services:
		(path, params) = i
		if path.find('wifi') > -1:
			wireless_networks[str(path)] = str(params['Name'])
			wireless_ssids += str(params['Name']) + ' '

	print '* wireless networks found: ', wireless_ssids

	if len(wireless_networks) > 0:
		print '* saving wireless networks in /data/ssids.p'

		#save
		with open( '/data/ssids.p', 'wb' ) as f:
			pickle.dump(wireless_networks, f)

		if server_started == False:
		 	#need wifi credentials
		 	#start AP
		 	subprocess.call(['python', '/app/setup_ap.py'])

			server_started = True
			start_server()

def try_connect():
	print "* try to connect"

	return_code = -100

	try:
		wifi_creds = pickle.load(open( '/data/creds.p', 'rb' ))

		print "* wifi credentials found. Connecting..."

		pconnect = subprocess.Popen(
							['python',
							'/app/connect.py',
							str(wifi_creds['path']),
							str(wifi_creds['psk'])])

		pconnect.wait()

		return_code = pconnect.returncode

		print '* connect script returned ', return_code

	except:
		print "* wifi credentials not found"

	return return_code == 0;

def wifi_reset(tech):
	print "* resetting the wifi adapter"

	#reset wifi adapter (power off and on)
	if tech.get_property('Powered') == True:
		tech.set_property('Powered', False)

	try:
		tech.set_property('Powered', True)
	except dbus.exceptions.DBusException:
		print 'Unable power up wifi adapter:', sys.exc_info()



if __name__ == '__main__':

	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	manager = pyconnman.ConnManager()

	try:
		#while scanning ConnManager.SIGNAL_SERVICES_CHANGED event would be triggered
		manager.add_signal_receiver(on_scan_done,
									pyconnman.ConnManager.SIGNAL_SERVICES_CHANGED,
									get_services)
	except dbus.exceptions.DBusException:
		print 'Unable to complete:', sys.exc_info()

	tech = pyconnman.ConnTechnology('/net/connman/technology/wifi')

	try:
		#reset wifi adapter
		wifi_reset(tech)
	except dbus.exceptions.DBusException:
		print '* reset timed out'
		print '* sleep for 10s'
		time.sleep(10)
		# retry
		wifi_reset(tech)

	try:

		# connect
		if try_connect():
			#succesfully connected
			sys.exit()
		else:
			#scanning for wireless networks
			#found wifis are saved in /data/ssids.p
			print "* scanning for available wireless networks"
			tech.scan()


	except dbus.exceptions.DBusException:
		print 'Unable to complete:', sys.exc_info()

	mainloop = gobject.MainLoop()
	mainloop.run()
