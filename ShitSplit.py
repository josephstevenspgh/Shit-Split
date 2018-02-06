#!/usr/bin/python
from TimeInput import *
import Tkinter as tk
import tkFont as tkf
import os

# # # # # # # # # # #
# # # ShitSplit # # #
# # # # # # # # # # #

# May luck be with you!

# Version 0.04
# This was hackishly put together by Joseph Stevens (setz) 
# You can contact me in #SpeedRunsLive on irc.speedrunslive.com
# Alternatively, I almost always have my twitch IRC chat open - http://www.twitch.tv/skiffain/new/

# To-Do list - see ChangeLog.txt

class ShitSplit(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		
		# Find OS - Mac quickfixes
		if(os.name.endswith("posix")):
			self.MacMode = True
			self.RightClick = "<Button-2>"
		else:
			self.MacMode = False
			self.RightClick = "<Button-3>"

		self.SSFont = tkf.Font(family='Verdana', size=8)

		# Some vars here - Make configuring colors/titles slightly easier for now
		self.master.title("ShitSplit")
		self.SplitFileName = "Splits/soniccd.ss"
		self.GoodSplit = '#48F'
		self.BadSplit = '#F44'		
		self.SSBGColor = 'black'
		self.SSFGColor = 'white'
		# self.master.iconbitmap("shitsplit.ico")
		if(sys.platform != "linux2"):
			self.master.iconbitmap("shitsplit.ico")
		self.ShowAttempts = True
		self.ShortenAttempts = False
		self.TitleAnchor = 'n'

		self.FirstTime = True
		self.ReadyToSave = False
		self.AttemptsSession = 0
		self.AttemptsTotal = 0

		# Load split file data
		self.LoadSplitThings()

		# GUI shit
		self.createWidgets()
		self.FirstTimeSetup()

	def Refresh(self):
		# Destroy everything
		self.app.destroy()
		self.AttemptsSession = 0
		self.AttemptsTotal = 0
		# Pretty much do it all over again.
		self.FirstTime = True
		self.ReadyToSave = False
		self.LoadSplitThings()
		self.createWidgets()
		self.FirstTimeSetup()

	def LoadSplitThings(self):
		# temp arrays/vars
		SFThing = []
		self.SplitNames = []
		self.SubSplitCounts = []
		self.SplitTimes = []
		self.SubSplits = []
		self.TotalInputCount = 0
		self.HasCentiseconds = False
		sscount = 0


		#Do Shit
		SplitFile = open(self.SplitFileName, "r")

		for line in SplitFile.readlines():
			SFThing.append(line)

		for x in SFThing:
			if x.find("#") > -1:
				# Split Title/Attempts
				oi = x.split("|")
				self.SplitTitle =  oi[0].split("#")[1]
				self.AttemptsTotal = int(oi[1])
				oi2 = oi[0].split("#")
			elif x.find("*") > -1:
				# Subsplit
				self.SubSplits.append(x.split("*")[1].rstrip())
				sscount += 1
			else:
				# Main Split
				oi = x.split("|")
				# Check to see if it has centiseconds

				if (oi[1].find(".")>-1):
					self.HasCentiseconds = True
				self.SplitNames.append(oi[0])
				self.SplitTimes.append(oi[1].rstrip())
				if(sscount > 0):
					self.SubSplitCounts.append(sscount)
				sscount = 0
		# Last SubSplitCount
		self.SubSplitCounts.append(sscount)

		# Find Total Input Count
		i=0
		while i < len(self.SubSplitCounts):
			self.TotalInputCount += self.SubSplitCounts[i]
			i+=1

		SplitFile.close()

	def FirstTimeSetup(self):
		self.update_idletasks()
		self.master.geometry(str(self.app.winfo_width())+"x"+str(self.app.winfo_height()))
		self.FirstTime = False

	def keyPressed(self, event):
	    if(event.char == 's'):
	    	self.StartTimer()
	    elif(event.char == 'S'):
	    	self.SaveSplits()
	    elif(event.char == 'r'):
	    	self.initSplits()
	    	self.StartTimer()

	def SaveAttempts(self):
		# Save only the new total attempts to the split file		
		TitleLine = "#"+self.SplitTitle+"|"+str(self.AttemptsTotal)+"\n"
		WLines = []

		i=0
		count=0
		while i < len(self.SplitNames):
			WLines.append(self.SplitNames[i]+"|"+self.SplitTimes[i]+"\n")	
			j=0
			while j < self.SubSplitCounts[i]:
				WLines.append("*"+self.SubSplits[count]+"\n")
				count += 1
				j += 1
			i += 1


		SplitFile = open(self.SplitFileName, "w")
		SplitFile.write(TitleLine)
		i=0
		while i < len(WLines):
			SplitFile.write(WLines[i])
			i += 1
		SplitFile.close()

	def SaveSplits(self):
		# Save a new split file

		# Make sure splits are done
		if(self.ReadyToSave == True):
			# Save the file !
			
			TitleLine = "#"+self.SplitTitle+"|"+str(self.AttemptsTotal)+"\n"
			WLines = []

			i=0
			count=0
			while i < len(self.SplitNames):
				WLines.append(self.SplitNames[i]+"|"+self.TimeDifs[i]+"\n")	
				j=0
				while j < self.SubSplitCounts[i]:
					WLines.append("*"+self.SubSplits[count]+"\n")
					count += 1
					j += 1
				i += 1


			SplitFile = open(self.SplitFileName, "w")
			SplitFile.write(TitleLine)
			i=0
			while i < len(WLines):
				SplitFile.write(WLines[i])
				i += 1
			SplitFile.close()
			self.Refresh()
		else:
			print "You must have every time input to save splits."

	def StartTimer(self):
		# I'm doing this the hard way with copy/paste because I'm lazy.
		# I may actually make this workable in the future if there is interest?
		# Popup window for time inputs
		if(self.SplittingInProgress == False):
			self.SplittingInProgress = True
			self.ReadyToSave = False
			self.IncreaseAttempts()

			TI = TimeInput(self.SubSplits[0], self.HasCentiseconds)

			self.CurrentSplit = 0
			self.CurrentSubSplit = 0
			self.CT = 0

			i = 0
			while (i < self.TotalInputCount):
				if(TI.InputHappened):
					# What to do ?!
					if(self.HasCentiseconds):
						self.CT += float(TI.GetInput())
					else:
						self.CT += TI.GetInput()

					#Increase Counters
					self.CurrentSubSplit += 1
					if(self.CurrentSubSplit >= self.SubSplitCounts[self.CurrentSplit]):
						# Split
						self.DoRepetitiveShit(self.CT, self.CurrentSplit)
						# Counters/Numbers
						self.CurrentSplit += 1
						self.CurrentSubSplit = 0
						self.CT = 0
					i += 1
					if(i < self.TotalInputCount):
						TI = TimeInput(self.SubSplits[i], self.HasCentiseconds)
					else:
						self.ReadyToSave = True
				else:
					# Temporary workaround
					self.after(100,self.update())

	def DoRepetitiveShit(self, Act1Time, DifIndex):		
		newerTime = Act1Time

		# Accumulate times and shit yo
		if(self.HasCentiseconds):
			if DifIndex > 0:
				newerTime += float(self.ConvertFromTime(self.lblTimes[DifIndex-1].cget("text")))
		else:
			if DifIndex > 0:
				newerTime += self.ConvertFromTime(self.lblTimes[DifIndex-1].cget("text"))

		# Compare and do cool split stuff
		if(self.HasCentiseconds):
			oldTime = float(self.ConvertFromTime(self.SplitList[DifIndex]))
		else:
			oldTime = int(self.ConvertFromTime(self.SplitList[DifIndex]))

		# New rewrite - I like this new condensed times idea
		self.svrTimes[DifIndex].set(self.ConvertToTime(newerTime))

		# Why the fuck was I doing things this way? REWRITE
		timeDiff = newerTime - oldTime
		print timeDiff
		self.svrDifference[DifIndex].set(self.ConvertToTime(str(timeDiff)))
		self.lblDifference[DifIndex].configure(textvariable=self.svrDifference[DifIndex])
		if timeDiff > 0:
			# Lost time on the split
			self.svrDifference[DifIndex].set("+"+self.lblDifference[DifIndex].cget("text"))
			self.lblDifference[DifIndex].configure(textvariable=self.svrDifference[DifIndex])
			self.lblTimes[DifIndex].configure(fg=self.BadSplit)
		elif timeDiff < 0:
			# Gained time on the split
			self.lblTimes[DifIndex].configure(fg=self.GoodSplit)
		else:
			# All splits are not created equal -- Except for this one
			self.lblTimes[DifIndex].configure(fg=self.SSFGColor)
		self.lblDifference[DifIndex].configure(fg=self.SSFGColor)
		# Make saving easier later
		self.TimeDifs.append(self.ConvertToTime(str(Act1Time)))

	def ConvertToTime(self, levTime):
		# Convert from a number of seconds into a string of minutes:seconds
		if(self.HasCentiseconds):
			levTime = str(levTime)
			Seconds = int(levTime.split(".")[0])
			CSeconds = int(levTime.split(".")[1])
			# Need Minutes?
			if(Seconds > 59):
				SepMins = int(Seconds / 60)
				SepSecs = Seconds - (SepMins*60)
				if SepSecs < 10:
					ReturnVal = str(SepMins)+":0"+str(SepSecs)
				else:
					ReturnVal = str(SepMins)+":"+str(SepSecs)
				if CSeconds < 10:
					CSeconds = "0"+str(CSeconds)
				ReturnVal = ReturnVal+"."+str(CSeconds)
			else:
				ReturnVal = str(Seconds)+"."+str(CSeconds)
		else:
			TimeInt = int(levTime)
			# Negatives got you down? Well fuck.
			if TimeInt < 0:
				ThisIsNeg = True
			else:
				ThisIsNeg = False
			TimeInt = abs(TimeInt)
			ReturnVal = str(TimeInt)
			if TimeInt > 59:
				# At least one minute needs to be displayed
				SepMins = int(TimeInt / 60)
				SepSecs = TimeInt - (SepMins*60)
				if SepSecs < 10:
					# Make sure the seconds number is 2 digits
					ReturnVal = str(SepMins)+":0"+str(SepSecs)
				else:
					ReturnVal = str(SepMins)+":"+str(SepSecs)
			if ThisIsNeg:
				ReturnVal = "-"+ReturnVal
		return ReturnVal

	def ConvertFromTime(self, levTime):
		# Convert from a string of Minutes:Seconds into a number of seconds
		if(self.HasCentiseconds == False):
			if (levTime.find(":")>-1):
				SplitString = levTime.split(":")
				retval = int((int(SplitString[0])*60) + int(SplitString[1]))
			else:
				retval = int(levTime)
			return retval
		else:
			# Handle this differently with centiseconds
			Minutes = levTime.split(":")[0]
			Seconds = levTime.split(":")[1].split(".")[0]
			Centiseconds = levTime.split(":")[1].split(".")[1]
			nSeconds = str((int(Minutes)*60) + int(Seconds))
			retval = str(nSeconds)+"."+str(Centiseconds)
			return retval

	def AddTimes(self, oldtime, newtime):
		t1 = self.ConvertFromTime(oldtime)
		t2 = self.ConvertFromTime(newtime)
		if(self.HasCentiseconds):
			newertime = self.ConvertToTime(float(t1)+float(t2))
		else:
			newertime = self.ConvertToTime(t1+t2)
		return newertime

	def IncreaseAttempts(self):
		self.AttemptsTotal = int(self.AttemptsTotal) + 1
		self.AttemptsSession = int(self.AttemptsSession) + 1
		# Update Split Window
		self.svrStatus.set(self.CalcAttempts())		
		# Save File w/Attempt Counter
		self.SaveAttempts()

	def CalcAttempts(self):
		# Just generate a string from attempts
		if self.ShortenAttempts:
			return "Attempts\nS: "+str(self.AttemptsSession)+" | T: "+str(self.AttemptsTotal)
		else:
			return "Attempts\nSession: "+str(self.AttemptsSession)+" | Total: "+str(self.AttemptsTotal)

	def popup(self, event):
		# Pop up the menu
		self.PMenu.post(event.x_root, event.y_root)

	def QuitSS(self):
		# Pretty simple concept - exit
		sys.exit()

	def LoadSplits(self, *args):
		# Load a new split file
		self.SplitFileName ="Splits/"+self.svrSplitMenu.get()
		# Clear out current variables/load new splits
		self.Refresh()

	def GenerateSMenu(self):
		# See what split files are available and put them in an array
		for files in os.walk('./Splits/'):
			self.SMList = list(files[2])
		# Generate the listing of av
		self.svrSplitMenu = StringVar()
		self.svrSplitMenu.set("word")
		self.SMenu = Menu(self, tearoff=0)
		i=0
		while i < len(self.SMList):
			# Check to see if it is the active split file
			if self.SplitFileName.endswith(self.SMList[i]):
				self.SMenu.add_radiobutton(label=self.SMList[i], value=self.SMList[i], variable=self.svrSplitMenu, state=tk.DISABLED)
			else:
				self.SMenu.add_radiobutton(label=self.SMList[i], value=self.SMList[i], variable=self.svrSplitMenu)
			i+=1
		self.svrSplitMenu.trace("w", self.LoadSplits)

	def createWidgets(self):
		self.master.configure(bg=self.SSBGColor)
		self.app = LabelFrame(self.master)
		self.app.configure(relief=FLAT, bg=self.SSBGColor, fg=self.SSFGColor, font=self.SSFont, text=self.SplitTitle, labelanchor=self.TitleAnchor, pady=5, padx=5)
		self.app.focus_set()

		# Labels and shit, yo
		self.lblSplitName = []
		self.lblTimes = []
		self.lblDifference = []
		self.svrDifference = []
		self.svrTimes = []
		self.OldTime = []

		# Create the Right-Click Context Menu
		# Create the Split Cascade Menu
		self.GenerateSMenu()
		self.PMenu = Menu(self, tearoff=0)
		self.PMenu.add_command(label="ShitSplit v04")
		self.PMenu.add_separator()
		self.PMenu.add_cascade(label="Select Splits", menu=self.SMenu)
		self.PMenu.add_command(label="Save Splits", command=self.SaveSplits)
		self.PMenu.add_separator()
		self.PMenu.add_command(label="Quit", command=self.QuitSS)

		if self.MacMode == False: 
			self.PMenu.configure(bg=self.SSBGColor, fg=self.SSFGColor)
			self.SMenu.configure(bg=self.SSBGColor, fg=self.SSFGColor)


		i=0
		while i < len(self.SplitNames):
			self.lblSplitName.append(Label(self.app))
			self.lblTimes.append(Label(self.app))
			self.lblDifference.append(Label(self.app))
			self.svrDifference.append(StringVar())
			self.svrTimes.append(StringVar())
			i += 1
		
		# Status Area
		self.svrStatus = StringVar()
		self.lblStatus = Label(self.app)
		self.svrStatus.set(self.CalcAttempts())
		self.lblStatus.configure(bg=self.SSBGColor, font=self.SSFont, fg=self.SSFGColor, textvariable=self.svrStatus)

		# init function yo
		self.initSplits()

		# Attempts/Header
		sessionFrame = Frame(self.app)
		sessionFrame.configure(bg=self.SSBGColor)
		self.SAttempts = StringVar()
		self.TAttempts = StringVar()
		self.SAttempts.set("S: "+str(self.AttemptsSession))
		self.TAttempts.set("T: "+str(self.AttemptsTotal))

		sessionFrame.grid(column=1, row=0, columnspan=3)
		self.lblSAttempts = Label(sessionFrame)


		self.app.bind("<Key>", self.keyPressed)
		#app.configure(bg=self.SSBGColor, pady=4, padx=4)
		self.app.grid()
		i = 0
		while (i < len(self.lblSplitName)):	# Add to window
			self.lblSplitName[i].grid(column = 0, row = i)
			self.lblTimes[i].grid(column = 1, row = i)
			self.lblDifference[i].grid(column = 2, row = i)
			i += 1

		# Attempts Counter
		if self.ShowAttempts:
			self.lblStatus.grid(column=0, row=i, columnspan=3)

		# Bind the PMenu
		self.app.bind(self.RightClick, self.popup)
		# oi. make everything clickable u.u
		self.lblStatus.bind(self.RightClick, self.popup)
		i = 0
		while (i < len(self.lblSplitName)):
			self.lblSplitName[i].bind(self.RightClick, self.popup)
			self.lblTimes[i].bind(self.RightClick, self.popup)
			self.lblDifference[i].bind(self.RightClick, self.popup)
			i += 1

	def initSplits(self):
		self.SplittingInProgress = False

		# Yeah
		self.OldTime = []
		self.TimeDifs = []
		i=0
		while i < len(self.SplitNames):
			self.lblSplitName[i].configure(text = self.SplitNames[i], anchor=W, font=self.SSFont, bg=self.SSBGColor, fg=self.SSFGColor)
			self.svrTimes[i].set(self.SplitTimes[i])
			self.OldTime.append(self.SplitTimes[i])
			i += 1

		# Old Times ?!
		self.SplitList = list(self.OldTime)

		# Current Splits
		tempTime = self.OldTime[0]
		self.SplitList[0] = self.OldTime[0]
		self.svrTimes[0].set(tempTime)
		self.lblTimes[0].configure(textvariable=self.svrTimes[0], font=self.SSFont, bg=self.SSBGColor, fg=self.SSFGColor)
		i = 1
		while i < len(self.OldTime):
			tempTime = self.AddTimes(tempTime, self.OldTime[i])
			self.SplitList[i] = tempTime
			self.svrTimes[i].set(tempTime)
			self.lblTimes[i].configure(bg=self.SSBGColor, fg=self.SSFGColor, font=self.SSFont, textvariable=self.svrTimes[i])
			i += 1

		# Temporary Values
		ix = 0
		while (ix < len(self.OldTime)):
			self.svrDifference[ix].set("+1:00")
			self.lblDifference[ix].configure(textvariable=self.svrDifference[ix], font=self.SSFont, bg=self.SSBGColor, fg=self.SSBGColor)
			ix += 1

def main():
    ShitSplit().mainloop() 

if __name__ == '__main__':
    main()