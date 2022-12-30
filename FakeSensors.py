import paho.mqtt.client as PahoMQTT
import time
import json
import random

class FakeSensor:
	def __init__(self, clientID,broker):
		self.clientID = clientID #UNIQUE ID!
		self.topic = ""
		# create an instance of paho.mqtt.client
		self._paho_mqtt = PahoMQTT.Client(self.clientID,True) 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		#self.messageBroker = 'iot.eclipse.org'
		self.messageBroker = broker

	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self,message):
		# publish a message with a certain topic
		self._paho_mqtt.publish(self.topic, message, 2)

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))




if __name__ == "__main__":
	test = FakeSensor("fakeSensors",'mqtt.eclipseprojects.io')
	test.start()
	
	dict = json.load(open('CompanyList.json'))
	while(True):
		for company in dict['CompanyList']:
			for device in company['deviceList']:
				if device['isSensor']:
					for measure in device['measureType']:
						topic = f"IoTomatoes/{company['companyName']}/{device['ID']}/{measure}"
						print(topic)
						test.topic = topic
						if(measure == 'temperature'):
							measure = round(random.uniform(0, 40),2)
							test.myPublish(json.dumps({'measure': measure}))
						elif(measure == 'humidity'):
							measure = round(random.uniform(0, 100),2)
							test.myPublish(json.dumps({'measure': measure}))
						elif(measure == 'light'):
							measure = round(random.uniform(10**(-4), 5**3),5)
							test.myPublish(json.dumps({'measure': measure}))
						elif(measure == 'sound'):
							measure = round(random.uniform(-20, 70),2)
							test.myPublish(json.dumps({'measure': measure}))
						else:
							print("Error: measure not found")
						print("Payload sent: ", measure, "\n")
		print("\n")
		time.sleep(5)

	test.stop()
