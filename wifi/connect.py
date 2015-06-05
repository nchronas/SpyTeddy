# connect to service path using the psk
#usage python connect.py <service_path> <psk>

import dbus
import pyconnman
import dbus.mainloop.glib
import gobject
import sys
import pickle
import pprint
import time
import subprocess

# service path
service_path = sys.argv[1]

# psk
psk = sys.argv[2]

#available wireless networks
wireless_networks = pickle.load(open( '/data/ssids.p', 'rb' ))


if __name__ == '__main__':
	try:
		print '* trying to connect to ', service_path, 'using psk: ', psk

		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

		manager = pyconnman.ConnManager()

		params = {'name': None,
				'ssid': wireless_networks[service_path],
				'identity': None,
				'username': None,
				'password': None,
				'passphrase': psk,
				'wpspin': None }

		print '* registering authentication agent'

		agent_path = '/resin/agent'

		agent = pyconnman.SimpleWifiAgent(agent_path)
		agent.set_service_params('*',
		params['name'],
		params['ssid'],
		params['identity'],
		params['username'],
		params['password'],
		params['passphrase'],
		params['wpspin'])

		manager.register_agent(agent_path)
		print '* auth agent has been registered'

		tech = pyconnman.ConnTechnology('/net/connman/technology/wifi')

		print '* clean iptables'
		subprocess.call(['/app/setup-iptables.sh', 'R'])

		tethering = tech.get_property('Tethering')
		print '* currently tethering? ', tethering

		if tethering:
			print '* disable tethering'
			tech.set_property('Tethering', False)

			# TODO: change this hardcoded sleep time
			print '* sleeping for 15s'
			time.sleep(15)

		print '* linking to service: ', service_path
		service = pyconnman.ConnService(service_path)

		print '* connection state:', service.State

		if service.State != 'ready':
			connected = service.connect()

			print '* connect returned: ',connected

			print '* connection state after connect:', service.State

			#TODO: only save if succesful
			# save credentials
			if connected == None:
				print '* connected succefully, saving credentials in /data/creds.p'
				with open('/data/creds.p', 'wb') as f:
					pickle.dump({'path': service_path, 'psk': psk}, f)
			else:
				print '* could not connect'
				sys.exit(1)
		else:
			print '* already connected'

		# succefully connected or already connected
		sys.exit(0)

	except dbus.exceptions.DBusException:
		print '* unable to complete:', sys.exc_info()
		print '* exit connect'
		sys.exit(1)
