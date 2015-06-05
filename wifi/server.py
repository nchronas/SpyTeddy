import web
import pickle
import pprint
import subprocess


urls = (
	'/.*', 'index'
)

app = web.application(urls, globals())

render = web.template.render('/app/templates/')

wireless_networks = pickle.load(open( '/data/ssids.p', 'rb' ))


class index:
	def GET(self):
		return render.index(wireless_networks = wireless_networks)

	def POST(self):
		data = web.input(_method='post')

		print '* launching connect procedure'

		p = subprocess.Popen(
						['python',
						'/app/connect.py',
						str(data.path),
						str(data.psk)])
		p.wait()

		if p.returncode == 0:
			#succefully connected
			#stop the server
			app.stop()
		else:
			#connection failed, we should restart the AP
			subprocess.call(['python', '/app/setup_ap.py'])

		return render.index(wireless_networks = wireless_networks)


if __name__ == '__main__':
	print '* starting server'
	app.run()
