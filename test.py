from Tkinter import * 

root = Tk()

# create a frame
frame = Frame(root, width=512, height=512)
frame.pack()

def popup(event):
	print "OS: "+str(sys.platform)
	print "Button Number: "+str(event.num)

# attach popup to frame
frame.bind("<ButtonPress>", popup)
root.mainloop()