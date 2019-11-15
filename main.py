from tkinter import *
import client as client
root = Tk()
"""
w = Canvas(root, width=1400, height=900)
w.pack()
root.update()
mainloop()
"""


client = client.Client(0x01)
client.connect()
