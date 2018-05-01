import servo
import httplib
import json
import time
import wiringpi

device_name = "hebe"

keynames = ["Lights","Aircon", "Temp", "FanIntensity", "Fan"]
actions = [servo.set_lights, servo.set_aircon,servo.set_temp, servo.set_wind, servo.set_fan]
servopins = [0,1,2]

onoffconstants = ["Off","On"]


def get_server_data(server_path):
    server = "192.241.140.108"
    port = "5000"
    headers = {'Content-type': 'application/json'}

    connection = httplib.HTTPConnection(server, port=port)
    connection.request('GET', server_path, headers=headers)

    response = connection.getresponse().read()
    d = json.loads(response.decode())

    return d

def update_event(title):
    get_server_data("/setevent/"+device_name+"?title="+title)

def get_time():
    return get_server_data("/currtime")

def get_device_data():
    return get_server_data("/get/"+device_name)

def delete_gadget(gadget):
    get_server_data("/delgadget/"+device_name+"?gadget="+gadget)


def step():
    server_time = get_time()
    print "New Round!"
    data = get_device_data()

    print "got data!"

    for event in data['events']:
        if data['events'][event]['time'] < server_time:
            update_event(event)
            print event + " updated!"
    print "passed events"

    # This is a very dirty and resource-draining way to get around an issue, 
    # but otherwise the above loops shorts the entire thing out if there aren't
    # any events in the queue. There's definitely a better way (like actually
    # checking my inputs), but this is quickest. By a long shot.
    get_server_data("/event/"+device_name+"?title=Stop&time=10000000")

    curr_data = get_device_data()['current']

    for i in range(len(keynames)):  
        if keynames[i] in curr_data:
            print keynames[i]
            actions[i](curr_data[keynames[i]]['value'])
            delete_gadget(keynames[i])


def poll(interval):
    while True:
        try:
            step()
        except:
            print "Exception - investigate..."
            pass
        wiringpi.delay(interval)

get_server_data("/event/"+device_name+"?title=Stop&time=10000000")
servo.bottom_out_temp()
poll(10)
