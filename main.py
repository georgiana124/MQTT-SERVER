import client as client
from GUI import *

my_gui = GUI()

client = client.Client("abc", username="GUI v1", password="GUI v2")
client.connect()
