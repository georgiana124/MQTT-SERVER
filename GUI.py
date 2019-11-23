from tkinter import *

class GUI(object):

    def __init__(self):
        self._root = Tk()
        self._root.geometry("1400x900")
        self._root.title("MQTT Client")
        self._button1 = Button(self._root, text="Close", command=self._root.quit)
        self._button1.place(bordermode=OUTSIDE, x=1200, y=800)
        self._root.bind("<Button-1>", self.motion)
        self._v1 = StringVar()
        self._v2 = StringVar()

        Label(self._root, text='Username').place(x=500, y=300)
        e1 = Entry(self._root)
        e1.focus_set();

        e1.place(x=590, y=300)

        def callback():
            # Get the strings from the Entries
            self.v1 = e1.get()
            self.v2 = e2.get()

        Label(self._root, text='Password').place(x=500, y=330)
        e2 = Entry(self._root)
        e2.place(x=590, y=330)

        b = Button(self._root, text="Connect", width=10, command=callback)
        b.place(x=600, y=400)


        self._root.update()

        self._root.mainloop()

    def motion(self, event):
        print(event.x, event.y)

