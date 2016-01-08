import os, glob, time, datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def getpid():
    dataAsString = str(os.getpid())

    fb = open("/home/pi/pidfile.pid","w")
    fb.write(dataAsString)
    fb.close()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def thingspeak():
    temperature = read_temp()
    params = urllib.urlencode({'field1': temperature, 'key':'4LZO6KZXCU9T2E3M'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update",params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    #time.sleep(16)
    
while True:
    getpid()
    dataAsInt = str(read_temp())
    dataAsString = str(dataAsInt)
    print dataAsString
    time.sleep(16)

#temperature = read_temp()
#params = urllib.urlencode({'field1': temperature, 'key':'4LZO6KZXCU9T2E3M'})
#headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
#conn = httplib.HTTPConnection("api.thingspeak.com:80")
#conn.request("POST", "/update",params, headers)
#response = conn.getresponse()
#print response.status, response.reason
#data = response.read()
#conn.close()
#time.sleep(16)
