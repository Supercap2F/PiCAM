from mtTkinter import *
import ttk
import threading
from picamera import PiCamera
import tkMessageBox
from time import sleep

class App:
    def __init__(self,master):
        #self.grid();
        # Make a canvas where a camera preview will be
        #self.CanvasPreview = Canvas(master,width=200,height=200);
        #self.CanvasPreview.grid(row=0, column=0, rowspan=10);

	photo = PhotoImage(file="img.gif");
	self.ImagePreview = Label(master, image=photo,width=200,height=200);
	self.ImagePreview.photo = photo;
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

        self.PreviewRunFlag = True
        print "\nthingys\n"
        


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
        self.CaptureFrames();

        
        
    def CaptureFrames(self):
	    if self.CameraCount < self.CameraTotalFrames:
		self.camera.capture('./lapse/img%03d.jpg' % self.CameraCount);
                print('Captured img%03d.jpg' % self.CameraCount);
                self.CameraCount+=1;
                root.after(self.CameraInterval, self.CaptureFrames);
                
            else:   
                print "test"
                self.FramesEntry.config(state=NORMAL);
                self.IntervalEntry.config(state=NORMAL);
                self.StartButton.config(state=NORMAL);
                self.PreviewRunFlag=True;
            
                                                

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
app.PreviewRunFlag = False
################################
# Camera and threading stuff   #
################################
app.camera = PiCamera(); # setup the camera



ThreadRunFlag = True

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "Starting " + self.name
        thread1(self.name)
        print "Exiting " + self.name


def thread1(threadname):
	while ThreadRunFlag:
            print app.PreviewRunFlag
            sleep(0.1);
            if(app.PreviewRunFlag):
                app.camera.resolution = (200,200);
                app.camera.capture('preview.gif');
                photo = PhotoImage(file="preview.gif");
                app.ImagePreview.config(image=photo);
                app.ImagePreview.photo=photo;
                print "thread running"

# Create new threads
threadone = myThread(1, "Thread-1")
threadone.daemon=True

# Start new Threads
threadone.start()

root.mainloop();


ThreadRunFlag = False  # set the thread to stop running 
threadone.join();      # wait for thread to end

root.destroy();


            
