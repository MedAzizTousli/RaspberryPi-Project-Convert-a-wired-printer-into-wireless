import socket #Import socket library -> File recieving
import os #Import os library -> File printing through bash
import RPi.GPIO as GPIO #Import GPIO library -> Turn high/low some LEDs
import sys #Import sys library -> Exit in case of error

def errorFunction(errorString): #Function that generates the different errors

    if (errorString=="socketCreationError"):
        print("Failed to create socket!") #Print error message
        GPIO.output(redLED,True) #Turn redLED high
        GPIO.output(greenLED,False) #Turn greenLED low
        sys.exit() #Exit in case of error
        
    elif (errorString=="bindError"):
        print("Failed to bind socket!")
        GPIO.output(redLED,True)
        GPIO.output(greenLED,False)
        sys.exit()

    elif (errorString=="listenError"):
        print("Failed to listen to connections!")
        GPIO.output(redLED,True)
        GPIO.output(greenLED,False)
        sys.exit()

    elif (errorString=="connectionError"):
        print("Failed to accept connection!")
        GPIO.output(redLED,True)
        GPIO.output(greenLED,False)
        sys.exit()
            
    elif (errorString=="sendDataError"):
        print("Failed to send data!")
        GPIO.output(redLED,True)
        GPIO.output(greenLED,False)
        sys.exit()

def liveServer(s,redLED,yellowLED,greenLED): #Function for live server
        
    while True: #Loop for live server -> Recieve many files

        print("Server is listening...") #Print welcome message
        GPIO.output(greenLED,True) #Turn greenLED high
        GPIO.output(redLED,False) #Turn redLED low
        GPIO.output(yellowLED,False) #Turn yellowLED low
        
        try:
            conn, address = s.accept() #Accept request to recieve data
        except socket.error:
            errorFunction("connectionError")
            
        fileName = conn.recv(1024) #Recieve file name     

        conn.send(b"fileName recieved") #Give the client the confirmation to send the file
        
        f = open('/home/pi/'+fileName,'wb') #Open new file in binary
        
        while True: #Loop to recieve the whole file

            GPIO.output(yellowLED,True) #Turn yellowLED high
            try:
                data = conn.recv(1024) #Recieve data
            except:
                break #Break in case of error from sender
                
            f.write(data) #Write data into file
            
            if not data: #If the buffer is empty i.e. the whole file is sent
                GPIO.output(yellowLED,False) #Turn yellowLED low
                break

        f.close() #Close the file
        conn.close() #Close the connection
        os.system("lp -d EPSON_L220_Series "+fileName) #Bash command to print the file
        
GPIO.setwarnings(False) #Do not show GPIO clean-up warnings

GPIO.setmode(GPIO.BOARD) #Choose broadway numbering mode

redLED = 7    #High when error is occured
yellowLED = 3 #High when someone is sending
greenLED = 5  #High when server is live

GPIO.setup(redLED,GPIO.OUT) #Set redLED to output
GPIO.setup(greenLED,GPIO.OUT) #Set greenLED to output
GPIO.setup(yellowLED,GPIO.OUT) #Set yellowLED to output

try: 
    s = socket.socket() #Create a socket
except socket.error:
    errorFunction("socketCreationError")
    
host = "" #Accept any host
port = 8000 #Any non well-known port can be written here

try:
    s.bind((host,port)) #Create connection with host on port
except socket.error:
    errorFunction("bindError")
    
try:
    s.listen(10) #Accept up to 10 connections
except socket.error:
    errorFunction("listenError")

liveServer(s,redLED,yellowLED,greenLED) #Call liveServer() function

s.close() #Close the socket
