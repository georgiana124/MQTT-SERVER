import client as client
from GUI import *

my_gui = GUI()

if(my_gui._isClicked):
    client = client.Client("abc", username=my_gui.v1, password=my_gui.v2)
    client.connect()
