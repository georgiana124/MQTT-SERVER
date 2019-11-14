from tkinter import *
import Connection as connection
import client as client
import socket
root = Tk()
"""
w = Canvas(root, width=1400, height=900)
w.pack()
root.update()
mainloop()
"""
#conn = connection.Connection()
client = client.Client()
ip = socket.gethostbyname('iot.eclipse.org')
client.publish()
print(ip)