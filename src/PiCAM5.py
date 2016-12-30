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

	
	self.ImagePreview = Label(master, width=200,height=200);
	
	self.ImagePreview.grid(row=0, column=0, rowspan=50, padx=10, pady=30, sticky=N);

        # add a status bar
        #self.StatusBar = Label(master, text="Please enter Values:");
        #self.StatusBar.grid(row=0, column=1, columnspan=2);

	vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
	

        # add the frames label
        self.FramesLabel=Label(master, text="Frames");
        self.FramesLabel.grid(row=0, column=1, columnspan=2, sticky=SW);

        # add the frames input
        self.FramesEntry=Entry(master,validate = 'key', validatecommand = vcmd);
        self.FramesEntry.grid(row=1, column=1, columnspan=2,padx=(0, 10));

        # add the interval label
        self.IntervalLabel=Label(master, text="Interval (in sec)");
        self.IntervalLabel.grid(row=2, column=1, columnspan=2, sticky=SW);

        # add the interval input
        self.IntervalEntry=Entry(master,validate = 'key', validatecommand = vcmd);
        self.IntervalEntry.grid(row=3, column=1, columnspan=2,padx=(0, 10));

        # add the quit button
        self.QuitButton = Button(master,text="Quit",command=master.quit);
        self.QuitButton.grid(row=4, column=1, sticky=E+W);

        # add the start button
        self.StartButton = Button(master,text="Start", command=self.StartRecording);
        self.StartButton.grid(row=4, column=2, sticky=E+W,padx=(0, 10));

        # add a progress bar
        self.ProgressBar = ttk.Progressbar(master, orient="horizontal", maximum=100 ,length=200, mode="determinate");
        self.ProgressBar.grid(row=5, column=0, columnspan=3, sticky=W+E, padx=10);
        self.ProgressBar["value"] = 50;
        
        master.grid_columnconfigure(0,weight=1)
        master.grid_columnconfigure(1,weight=1)
        master.grid_columnconfigure(2,weight=1)
        master.grid_rowconfigure(0,weight=1)
        master.grid_rowconfigure(1,weight=1)
        master.grid_rowconfigure(2,weight=1)
        master.grid_rowconfigure(3,weight=1)
        master.grid_rowconfigure(4,weight=1)
        master.grid_rowconfigure(5,weight=1)
        master.grid_rowconfigure(6,weight=1)

	
	self.ProcessQueueLoop()
        


    def StartRecording(self):
	if(self.FramesEntry.get()=="" or self.IntervalEntry.get()==""):
		tkMessageBox.showwarning("No input","Please fill in all fields");
		return;

	self.PreviewRunFlag=False;
	    
        s=self.FramesEntry.get();
	self.CameraTotalFrames=int(s)
	f=self.IntervalEntry.get();
	self.CameraInterval=int(f)
	self.CameraCount=0;
			
	self.FramesEntry.config(state=DISABLED);
	self.IntervalEntry.config(state=DISABLED);
	self.StartButton.config(state=DISABLED);
	self.ImagePreview.focus(); #focus on a random widget

        print self.CameraInterval
        print self.CameraTotalFrames
        #self.camera.resolution = (1080,720);

	CaptureInfo = [1080, 720, self.CameraInterval, self.CameraTotalFrames]
	self.OutgoingQueue.put(CaptureInfo)

    def ProcessQueueLoop(self):
	try:
		task = self.IncomingQueue.get_nowait() 
		if task[0] == "uppreview":
                        #if task[2] == "jpg":
                        image=Image.open(task[1])
                        image=image.resize((200,200))
                        photo=ImageTk.PhotoImage(image)
                        
                	self.ImagePreview.config(image=photo);
                	self.ImagePreview.photo=photo;
		elif task[0] == 'normalmode':
			self.FramesEntry.config(state=NORMAL);
                	self.IntervalEntry.config(state=NORMAL);
                	self.StartButton.config(state=NORMAL);
			
		else:
			print "unknown task"

	except Queue.Empty:
		pass
	    
	root.after(100,self.ProcessQueueLoop)

    def IncomingQueueWrite(self, task):
	self.IncomingQueue.put(task)

    def OutgoingQueueWrite(self, task):
	self.OutgoingQueue.put(task)
            
                                                

    # function to check input to make sure the value is only numbers 
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
	if(action=='1'):
		if text in '0123456789.-+':
			try:
				float(value_if_allowed)
				return True
			except ValueError:
				tkMessageBox.showwarning("Invalid Entry","Please enter only numbers");
				return False
		else:
			tkMessageBox.showwarning("Invalid Entry","Please enter only numbers");
			return False
	else:
		return True

#################
# Program setup #
#################
root=Tk();
app=App(root);
root.attributes("-fullscreen",True); # fullscreen app
################################
# Camera and threading stuff   #
################################
camera = PiCamera(); # setup the camera
runThread=True

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while runThread:
		try:
	 		task = app.OutgoingQueue.get_nowait()
			for i in range(task[3]):
                                currentTime=int(round(time.time()*1000)) # get the current time in ms
				camera.resolution = (task[0], task[1])
				camera.capture('./lapse/img%03d.jpg' % i)
				f = ['uppreview','./lapse/img%03d.jpg' % i, 'jpg']  # will need to be changed later
				app.IncomingQueue.put(f)
				
                                diffTime=0L
				while(diffTime<=task[2]):
                                    diffTime=int(round(time.time()*1000))-currentTime
			s = ['normalmode']
			app.IncomingQueue.put(s)
		
		except Queue.Empty: # this will run if there is nothing to capture
			camera.resolution = (200,200)
			camera.capture('preview.jpg')
			a = ['uppreview','./preview.jpg'] 
			app.IncomingQueue.put(a)
			currentTime=int(round(time.time()*1000)) # get the current time in ms
                        diffTime=0L
			while(diffTime<=10):
                            diffTime=int(round(time.time()*1000))-currentTime




# Create new threads
threadone = myThread(1, "Thread-1")
# Start new Threads
threadone.start()


root.mainloop();
runThread=False
root.destroy();


            
