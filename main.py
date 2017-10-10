import os
import time
import datetime
import serial
import RPi.GPIO as GPIO      


print "hello"

filename = "/home/pi/Dropbox-Uploader/"+datetime.datetime.now().strftime("%H%M%S.avi")
take_video="sudo avconv -t 10 -f video4linux2 -r 10 -s 256x133 -i /dev/video0 -y "+filename
os.system(take_video)

print "video done"
time.sleep(3)

print "starting upload"

os.system("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload "+filename+" /videos")
print "upload done"



GPIO.setmode(GPIO.BOARD)    
# Enable Serial Communication
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
 
port.write('AT'+'\r\n')
rcv = port.read(10)
print rcv
time.sleep(1)
 
port.write('ATE0'+'\r\n')      # Disable the Echo
rcv = port.read(10)
print rcv
time.sleep(1)
 
port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
rcv = port.read(10)
print rcv
time.sleep(1)
 
port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
rcv = port.read(10)
print rcv
time.sleep(1)
 

# Sending a message to a particular Number
 
port.write('AT+CMGS="92xxxxxxxx"'+'\r\n')
rcv = port.read(10)
print rcv
time.sleep(1)
 
port.write('Intruder alert!'+' www.dropbox.com/home/videos?preview='+filename+'\r\n')  # Message
rcv = port.read(10)
print rcv
 
port.write("\x1A") # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print rcv

port.write("\x0D\x0A")
rcv = port.read(10)
print rcv
time.sleep(1)

ck=1
while ck==1:
    rcv = port.read(10)
    print rcv
    fd=rcv
    if len(rcv)>3:                   # check if any data received 
        ck=12
        for i in range(5):            
            rcv = port.read(10)
            print rcv
            fd=fd+rcv                 # Extract the complete data 
 
# Extract the message number shown in between the characters "," and '\r'
        print fd
        p=fd.find(',')
        print p
        q=fd.rfind('\r')
        print q
        MsgNo=fd[p+1:q]
        print MsgNo
 
# Read the message corresponds to the message number
        rd=port.write('AT+CMGR='+MsgNo+'\r\n')
        msg=''
        for j in range(10):
            rcv = port.read(20)
            msg=msg+rcv
        print msg
    time.sleep(0.1)
    
if msg[:2]=="NO":
    print "He is an intruder"
    #buzzer alerts
elif msg[0:3]=="YES":
    print msg
else:
    print "else case: "+msg


