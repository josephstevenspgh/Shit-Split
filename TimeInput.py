from Tkinter import *

class TimeInput:    
    def EnterOK(self, event):
        self.ClickedOK()

    def ClickedOK(self):
        # OK Clicked
        self.TimeForLevel = self.AddTimes(self.TimeOffset, self.GetTime())
        self.InputHappened = True
        self.root.destroy()

    def AddTimes(self, oldTime, newTime):
        if(self.DisplayCentiseconds):
            # Centisecond logic
            print "* AddTimes"
            print("oldTime: %s" % oldTime)
            print("newTime: %s" % newTime)
            retval = float(oldTime)+float(newTime)
            print("retval: %s" % retval)
            return retval
        else:
            return oldTime+newTime

    def GetTime(self):
        if(self.DisplayCentiseconds):
            if(len(self.txtMins.get()) == 0):
                thisMins = 0
            else:
                thisMins = int(int(self.txtMins.get())*60)

            if(int(self.txtSecs.get()) < 1):
                thisSecs = 0
            else:
                thisSecs = int(self.txtSecs.get())

            if(len(self.txtCents.get()) == 0):
                thisCents = 0
            else:
                thisCents = str(self.txtCents.get())
                print("* Get Time:")
                print("thisCents: %s" %thisCents)

            return str(int(thisMins+thisSecs))+"."+str(thisCents)

        else:
            # allow nothing to be entered for either one
            if(len(self.txtMins.get()) == 0):
                thisMins = 0
            else:
                thisMins = int(int(self.txtMins.get())*60)
            if(int(self.txtSecs.get()) < 1):
                thisSecs = 0
            else:
                thisSecs = int(self.txtSecs.get())
            return int(thisMins+thisSecs)

    def ClearTimes(self):
        # Clear out the times and reset the focus
        self.txtMins.delete(0, 50)
        self.txtSecs.delete(0, 50)
        self.txtMins.focus_set()
        self.txtSecs.configure(fg='black')

    def AddTime(self, event):
        # + key hit - Add time, but don't submit
        self.TimeOffset += self.GetTime()
        # Clear Times
        self.ClearTimes()

    def SubTime(self, event):
        # - key hit - Subtract time, but don't submit
        self.TimeOffset -= self.GetTime()
        # Clear Times
        self.ClearTimes()

    def MoveNext(self, event):
        self.txtSecs.configure(fg='white')
        self.txtSecs.delete(0, 50)
        self.txtSecs.focus_set()        

    def MoveToCents(self, event):
        self.SecInputs += 1
        if(self.SecInputs >= 2):
            self.txtCents.configure(fg='white')
            self.txtCents.delete(0, 50)
            self.txtCents.focus_set()

    def GetInput(self):
        return self.TimeForLevel

    def __init__(self, LvlString = "", cent = False):
        # Time Offset variable
        self.TimeOffset = 0
        self.TimeOffsetString = "0:00"
        self.DisplayCentiseconds = cent

        self.SecInputs = 0

        # create a root window
        self.root = Tk()
        self.root.title("Time Entry")
        self.root.configure(background='black')
        self.root.geometry('+300+500') 

        self.TimeForLevel = 0

        # create a frame in the window to hold other widgets
        app = Frame(self.root)
        self.TimeInputFrame = Frame(app)
        self.InputHappened = False

        # Labels and shit, yo
        self.lblLevelName = Label(app, text=LvlString, bg='black', fg='white')
        self.txtMins = Entry(self.TimeInputFrame, width=1, bg='black', fg='white', insertbackground='white', text="")
        self.txtSecs = Entry(self.TimeInputFrame, width=2, bg='black', fg='black', insertbackground='white', text="")
        self.txtCents = Entry(self.TimeInputFrame, width=2, bg='black', fg='black', insertbackground='white', text="")
        self.lblColon = Label(self.TimeInputFrame, text=":", bg='black', fg='white')
        self.lblDec = Label(self.TimeInputFrame, text=".", bg='black', fg='white')

        # Add shit to window
        app.configure(bg='black', pady=4, padx=4)
        self.TimeInputFrame.configure(bg='black')
        app.grid()
        self.lblLevelName.grid(column = 0, row = 0, columnspan=4, pady=4, padx=4)
        self.txtMins.grid(column=0, row=0)
        self.lblColon.grid(column=1, row=0)
        self.txtSecs.grid(column=2, row=0)
        # If centiseconds should be displayed, do it !
        if(self.DisplayCentiseconds):
            self.lblDec.grid(column=3, row=0)
            self.txtCents.grid(column=4, row=0)
        
        self.TimeInputFrame.grid(column=1, row=1, columnspan=2)

        # Bindings
        if(self.DisplayCentiseconds):
            self.txtCents.bind("<Return>", self.EnterOK)
        else:
            self.txtSecs.bind("<Return>", self.EnterOK)
        self.txtMins.bind("<Key>", self.MoveNext)
        if(self.DisplayCentiseconds):
            self.txtSecs.bind("<Key>", self.MoveToCents)
        self.txtSecs.bind("-", self.SubTime)
        self.txtSecs.bind("+", self.AddTime)
        self.txtCents.bind("-", self.SubTime)
        self.txtCents.bind("+", self.AddTime)


        # Steal that focus !
        self.root.iconify()
        self.root.update()
        self.root.deiconify()
        self.txtMins.focus_set()
        if(sys.platform != "linux2"):
            self.root.iconbitmap("shitsplit.ico")

def main():
    TimeInput().mainloop() 

if __name__ == '__main__':
    main()        