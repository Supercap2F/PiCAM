from Tkinter import *
import ttk
import threading
import Queue
from picamera import PiCamera
import tkMessageBox
import time
from PIL import ImageTk, Image

class App:
    def __init__(self,master):
	# setup the queue
	self.IncomingQueue = Queue.Queue()
	self.OutgoingQueue = Queue.Queue()

	self.TopLogo=Label(master, width=480,  height=50)
	self.TopLogo.grid(row=0, column=0, columnspan=3, sticky=N)
	TopLogoImage=ImageTk.PhotoImage(Image.open('./MainLogo.png'))
	self.TopLogo.config(image=TopLogoImage)
	self.TopLogoImage=TopLogoImage

	
	self.ImagePreview = Label(master, width=200,height=200)
	self.ImagePreview.grid(row=1, column=0, rowspan=6, padx=(10,0), pady=(7,0), sticky=W+N)

        # add a status bar
        #self.StatusBar = Label(master, text="Please enter Values:");
        #self.StatusBar.grid(row=0, column=1, columnspan=2);

	vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
	

        # add the frames label
        self.FramesLabel=Label(master, text="Frames")
        self.FramesLabel.grid(row=1, column=1, columnspan=2, sticky=SW, pady=(15,0))

        # add the frames input
        self.FramesEntry=Entry(master,validate = 'key', validatecommand = vcmd)
        self.FramesEntry.grid(row=2, column=1, columnspan=2,padx=(0, 10), sticky=E+W)

        # add the interval label
        self.IntervalLabel=Label(master, text="Interval (in sec)")
        self.IntervalLabel.grid(row=3, column=1, columnspan=2, sticky=SW)

        # add the interval input
        self.IntervalEntry=Entry(master,validate = 'key', validatecommand = vcmd)
        self.IntervalEntry.grid(row=4, column=1, columnspan=2,padx=(0, 10), sticky=E+W)

        # add the quit button
        self.QuitButton = Button(master,text="Quit",command=master.quit)
        self.QuitButton.grid(row=5, column=1, sticky=E+W , pady=(30,0))

        # add the start button
        self.StartButton = Button(master,text="Start", command=self.StartRecording)
        self.StartButton.grid(row=5, column=2, sticky=E+W,padx=(0, 10) , pady=(30,0))

        # add the settings button
        self.SettingsButton = Button(master,text="Settings")
        self.SettingsButton.grid(row=6, column=1, columnspan=3, sticky=E+W, padx=(0,10), pady=(0,20))

        # add a progress bar
        self.ProgressBar = ttk.Progressbar(master, orient="horizontal", maximum=100 ,length=200, mode="determinate")
        self.ProgressBar.grid(row=8, column=0, columnspan=3, sticky=W+E, padx=10, pady=(0,10))

        self.ProgressBarLabel = Label(master, text="Press Start to Begin Capturing")
        self.ProgressBarLabel.grid(row=7, column=0, sticky=W+N, padx=10)
        
        master.grid_columnconfigure(0,weight=1)
        master.grid_columnconfigure(1,weight=1)
        master.grid_columnconfigure(2,weight=1)
        for n in range(8):
            master.grid_rowconfigure(n,weight=1)

	
	self.ProcessQueueLoop()
        


    def StartRecording(self):
	if(self.FramesEntry.get()=="" or self.IntervalEntry.get()==""):
		tkMessageBox.showwarning("No input","Please fill in all fields")
		return

	self.PreviewRunFlag=False
	    
        s=float(self.FramesEntry.get())
	self.CameraTotalFrames=int(round(s))
	f=float(self.IntervalEntry.get())
	self.CameraInterval=int(round(f*10)) # convert sec to decisec 
	self.CameraCount=0
			
	self.FramesEntry.config(state=DISABLED)
	self.IntervalEntry.config(state=DISABLED)
	self.StartButton.config(state=DISABLED)
	self.ImagePreview.focus() #focus on a random widget
        self.ProgressBar["maximum"] = self.CameraTotalFrames-1
        self.ProgressBar["value"] = 0

	CaptureInfo = [1080, 720, self.CameraInterval, self.CameraTotalFrames]
	self.OutgoingQueue.put(CaptureInfo)

    def ProcessQueueLoop(self):
	try:
		Queuedtask = self.IncomingQueue.get_nowait() 
		if Queuedtask[0] == "uppreview":
                        image=Image.open(Queuedtask[1])
                        image=image.resize((200,200))
                        photo=ImageTk.PhotoImage(image)
                        self.ProgressBar["value"]=int(Queuedtask[2])
                        if Queuedtask[1] != './preview.jpg':
                            self.ProgressBarLabel.config(text="Captured: " + Queuedtask[1])
			self.ImagePreview.config(image=photo)
                	self.ImagePreview.photo=photo
		elif Queuedtask[0] == 'normalmode':
                        self.ProgressBarLabel.config(text="Capture Finished")
			self.FramesEntry.config(state=NORMAL)
                	self.IntervalEntry.config(state=NORMAL)
                	self.StartButton.config(state=NORMAL)
			
		else:
			print "unknown task"

	except Queue.Empty:
		pass
	root.after(100,self.ProcessQueueLoop)
            
                                                
    # function to check input to make sure the value is only numbers 
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
	if(action=='1'):
		if text in '0123456789.-+':
			try:
				float(value_if_allowed)
				return True
			except ValueError:
				tkMessageBox.showwarning("Invalid Entry","Please enter only numbers")
				return False
		else:
			tkMessageBox.showwarning("Invalid Entry","Please enter only numbers")
			return False
	else:
		return True

#################
# Program setup #
#################
root=Tk()
root.title("PiCAM")
if root.winfo_screenwidth() == 480 and root.winfo_screenheight() == 320:
    root.attributes("-fullscreen",True) # fullscreen app
else:
    root.geometry("480x320")
    root.resizable(width=False, height=False)

app=App(root)
                     
# Camera and threading stuff   
camera = PiCamera()  # setup the camera
runThread=True       # the main thread is set to run


################################################################################
# This thread runs in a loop, and passes tasks to and from the GUI (aka app)   #
################################################################################
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while runThread:
		try:
	 		task = app.OutgoingQueue.get_nowait()             # check if there are any tasks to preform 
			for i in range(task[3]):                          # if the task is capturing (it will fork to except if not)
                                currentTime=int(round(time.time()*10))  # get the current time in ms
				camera.resolution = (task[0], task[1])                 # setup the camera for the proper res
				camera.capture('./lapse/img%03d.jpg' % i)              # capture the image 
				f = ['uppreview','./lapse/img%03d.jpg' % i,i]          # send the GUI the image to display 
				app.IncomingQueue.put(f)                               #
                                diffTime=0L                                            # wait for the required interval 
				while(diffTime<=task[2]):                              # 
                                    diffTime=int(round(time.time()*10))-currentTime  # 
				if runThread != True:                                  # if the program is quit, stop the thread 
				    return()                                           #
			s = ['normalmode']                                             # switch the gui to be enabled again 
			app.IncomingQueue.put(s)                                       #
		
		except Queue.Empty:                              # this will run if there is nothing to capture
			camera.resolution = (200,200)            # set the res 
			camera.capture('preview.jpg')            # 
			a = ['uppreview','./preview.jpg',0]        # send the gui the image to preview 
			app.IncomingQueue.put(a)                 #
			currentTime=int(round(time.time()*1000)) # wait for a amount of time (10ms) before running again
                        diffTime=0L                              # 
			while(diffTime<=10):                     #
                            diffTime=int(round(time.time()*1000))-currentTime
			if runThread != True:                    # if the program is quit, stop the thread 
				return()                          




# Create and start the thread 
threadone = myThread(1, "Thread-1")
threadone.start()
root.style=ttk.Style()
root.style.theme_use('clam')

root.mainloop() # enter the main program loop
runThread=False # turn off the thread from looping (when the program is closed)
root.destroy()


            
