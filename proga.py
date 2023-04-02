import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image
import numpy as np

c = 0
pts1 = np.float32([[0,0],[0,0],[0,0],[0,0]])
pts2 = np.float32([[0,0],[1000,0],[1000,1000],[0,1000]])

bluemin=67,98,153
bluemax=135,195,220

def findcolor(colmin, colmax):
    frame = cv2.imread('C:\\Users\\shkos\\Desktop\\2.jpg')
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv=cv2.blur(hsv,(5,5))
    mask=cv2.inRange(hsv,(colmin),(colmax))
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=4)
    
    contours=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours=contours[0]

    if contours:
        sorted(contours,key=cv2.contourArea,reverse=True)
        cv2.drawContours(frame,contours,-1,(255,0,0),3)
        (x,y,w,h)=cv2.boundingRect(contours[0])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imwrite("C:\\Users\\shkos\\Desktop\\3.jpg",frame)
        return x, y
    else:
        cv2.imwrite("C:\\Users\\shkos\\Desktop\\3.jpg",frame)
        x,y=None,None
        return x,y

def klik(event):
    global c, pts1
    print(pts1[0])
    c+=1
    print(event.x, event.y)
    if c % 4 == 1:
        pts1[0]=[event.x,event.y]
    if c % 4 == 2:
        pts1[1]=[event.x,event.y]
    if c % 4 == 3:
        pts1[2]=[event.x,event.y]
    if c % 4 == 0:
        pts1[3]=[event.x,event.y]
    print(c)
    print(pts1)
    return event.x, event.y

class App:

    def __init__(self, window, window_title, video_source):

        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)

        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height+200)
        self.canvas.pack()
        self.window.resizable(width=False, height=False)

        self.btn_1=tkinter.Button(window, text="преобразование", width=44, command=self.button1)
        self.btn_1.pack(side='left', expand=True)

        self.btn_2=tkinter.Button(window, text="координаты", width=44, command=self.button2)
        self.btn_2.pack(side='right', expand=True)

        self.canvas.bind('<Button-1>',klik)


        self.delay = 10
        self.update()

        self.window.mainloop()


    def button1(self):
        global pts1, pts2
        ret, frame = self.vid.get_frame()
        frame = cv2.flip(frame,1)
        if ret:
            cv2.imwrite("C:\\Users\\shkos\\Desktop\\1.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        self.photo = cv2.imread('C:\\Users\\shkos\\Desktop\\1.jpg')
        self.photo = cv2.cvtColor(self.photo, cv2.COLOR_RGB2BGR)
        M = cv2.getPerspectiveTransform(pts1,pts2)
        dst = cv2.warpPerspective(self.photo,M,(1000,1000))
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)
        cv2.imwrite('C:\\Users\\shkos\\Desktop\\2.jpg', dst)
        self.photo = Image.open('C:\\Users\\shkos\\Desktop\\2.jpg')
        self.photo1 = self.photo.resize((267,200), Image.ANTIALIAS)
        self.photo2 = PIL.ImageTk.PhotoImage(self.photo1)
        self.label = tkinter.Label(image=self.photo2)
        self.label.image = self.photo2
        self.label.place(x=30,y=480, anchor = tkinter.NW)

    def button2(self):
        x=findcolor(bluemin, bluemax)
        self.photo = Image.open('C:\\Users\\shkos\\Desktop\\3.jpg')
        self.photo1 = self.photo.resize((267,200), Image.ANTIALIAS)
        self.photo2 = PIL.ImageTk.PhotoImage(self.photo1)
        self.label = tkinter.Label(image=self.photo2)
        self.label.image = self.photo2
        self.label.place(x=410,y=480, anchor = tkinter.NW)
        my_label=tkinter.Label(bd=4,text='',relief='solid',font='Times 10 bold', bg='white', fg='black')
        my_label.pack()
        my_label['text']=f'x={x[0]} y={x[1]}'
        print(x)

    def update(self):
        ret, frame = self.vid.get_frame()
        frame = cv2.flip(frame,1)
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = 640
        self.height = 480

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv2.resize(frame,(640,480))
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

App(tkinter.Tk(), "Видео с камеры",0) 
#'C:\\Users\\shkos\\Downloads\\Fotochki_i_vidosy_iz_laby\\3.mp4'