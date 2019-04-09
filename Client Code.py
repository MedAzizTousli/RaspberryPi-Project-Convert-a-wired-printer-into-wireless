import socket #Import socket library -> File sending
from tkinter import * #Import Tkinter library -> Graphic interface
import tkinter.filedialog as fdialog #-> Get fileName from the browse button
from urllib.request import urlopen #-> Get logoImage from the internet
import base64 #-> Image encoding purposes

def errorFunction(errorString): #Function that generates the different errors
    
    errorMessage=Label(app,text="\n"+errorString+"\n")
    errorMessage.pack()

def fileFind(): #Function to browse the file
    
    file = fdialog.askopenfile(filetypes=[("PDF (.pdf)","*.pdf"),("Document (.doc)","*.doc"),("DocumentX (.docx)","*.docx")])
    global fileName
    fileName = file.name

def clientCode(): #Function for client

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket
    except socket.error:
        errorFunction("Failed to create socket!")
        
    host = "192.168.6.116" #The IP address of the server
    port = 8000 #The port used by the server

    try:
        s.connect((host,port)) #Create connection with host on port
    except socket.error:
        errorFunction("Failed to connect to host!")

    try:
        s.send(fileName.split('/')[-1].encode()) #Send fileName
    except socket.error:
        errorFunction("Failed to send fileName!")
        
    try:
        confirmation = s.recv(1024) #Get the confirmation from the server
    except socket.error:
        errorFunction("Server is not responding!")
    
    if confirmation==b'fileName recieved':
        
        f = open(fileName, "rb") #Open the file to be sent

        data = f.read(1024) #Send the file
        while (data):
            s.send(data)
            data = f.read(1024)

        reception=Label(app,text="\nFile sent successfully. Go take your documents from D32.\n") #Confirm sending to the user
        reception.pack()

    s.close() #Close the socket

"""----------Tkinter Interface----------"""

app=Tk() #Create Tkinter object
app.title("Printing Service") #Make window title
app.geometry("600x400") #Make window size

#Insert TPS logo
image_url="https://i.imgur.com/ALtEouU.gif" 
image_byt = urlopen(image_url).read()
image_b64 = base64.encodestring(image_byt) 
photo =PhotoImage(data=image_b64)
w = Label(app, image=photo)
w.pack()
ent = Entry(app)

#Insert welcome message
welcome=Label(app,text="\nWelcome to the AJP's printing service\n")
welcome.config(font=('tahoma',15,'bold'))
welcome.pack()

#Button browse a file
browseButton = Button(app, text='Browse a File', command=fileFind)
browseButton.place(relx=0.5, rely=0.5, anchor=CENTER)
browseButton.pack()

#For organizational purposes
space=Label(app,text="\n")
space.config(font=('tahoma',2,'bold'))
space.pack()

#Button print
printButton = Button(app, text='Print', command=clientCode)
printButton.place(relx=0.5, rely=0.5, anchor=CENTER)
printButton.pack()

app.mainloop() #Let Tkinter in a loop
