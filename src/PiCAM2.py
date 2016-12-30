from Tkinter import *
import ttk
from picamera import PiCamera
import tkMessageBox

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
        


    def StartRecording(self):
	if(self.FramesEntry.get()=="" or self.IntervalEntry.get()==""):
		tkMessageBox.showwarning("No input","Please fill in all fields");
		return;
		
	self.FramesEntry.config(state=DISABLED);
	self.IntervalEntry.config(state=DISABLED);
	self.StartButton.config(state=DISABLED);
	self.ImagePreview.focus(); #focus on a random widget

        camera = PiCamera();
        camera.resolution = (1080,720);
        while(count<num):
            camera.capture('./lapse/img%03d.jpg' % count);
            print('Captured img%03d.jpg' % count);
            count+=1;
            sleep(interval);


        print("Hi there, everyone!");



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


root=Tk();
#full screen app
#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1);
#root.geometry("%dx%d+0+0" % (w,h))
#root.focus_set();
#root.blind("<Escape>", root.quit)

app=App(root);

root.attributes("-fullscreen",True);
camera = PiCamera();
app.IntervalEntry.focus();

def UpdatePreview():
        camera.resolution = (200,200);
        camera.capture('preview.gif');
        photo = PhotoImage(file="preview.gif");
	app.ImagePreview.config(image=photo);
	app.ImagePreview.photo=photo;
	root.after(500,UpdatePreview); # change the first argument to adjust the time of delay in ms

root.after(0,UpdatePreview);
root.mainloop();
root.destroy();



            
