import servo
import httplib
import json
import wiringpi

device_name = "raspi1"

keynames = ["Fan","FanIntensity", "Aircon","Temp", "Lights"]
types = ["SWITCH","SLIDER","SWITCH","SLIDER","SWITCH"]
servopins = [0,1,2,3]

onoffconstants = ["Off","On"]

def get_server_data():
    server = "192.241.140.108"
    port = "5000"
    headers = {'Content-type': 'application/json'}
    server_path = "/get"

    connection = httplib.HTTPConnection(server, port=port)
    connection.request('GET', server_path, headers=headers)

    response = connection.getresponse().read()

    d = json.loads(response.decode())

    return d['data']

def step():
    data = get_server_data()

    for i in range(len(keynames)):
        full_key = device_name+"_"+keynames[i]
        if full_key in data:
            print full_key
            if types[i] == "SWITCH":
                if data[full_key]['value']==onoffconstants[0]:
                    print "\tUp"
                    servo.up(servopins[i])
                elif data[full_key]['value']==onoffconstants[1]:
                    print "\tDown"
                    servo.down(servopins[i])

def poll(interval):
    while True:
        try:
            step()
        except:
            print "Exception - investigate..."
            pass
        wiringpi.delay(interval)

poll(10)
