import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy import genfromtxt
import sys
#Read Video
timestamp=sys.argv[1]
filename = 'videos/'+timestamp+'.mp4'
cap = cv2.VideoCapture(filename)

frameCt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS);

height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)

videolen = int(frameCt / fps);

freq = 10.0


#Read data from csv
#Format is
#[['Longitude', 'Latitude', 'Speed', 'Distance', 'Time', 'Acc X', 'Acc Y', 'Acc Z', 'Heading', 'gyro_x', 'gyro_y', 'gyro_z']
df = genfromtxt('videos/'+timestamp+'.csv', delimiter=',')
data=[]


dims=range(5,12)
for i in xrange(len(dims)):
	data.append(df[1:,dims[i]])
	y=data[i]
	x=np.linspace(0,videolen,len(y))
	xvals = np.linspace(0,videolen,frameCt)
	data[i] = np.interp(xvals, x, y)
	
del data[3]
#BGR
color=[(0,0,255),(0,255,0),(255,0,0)]

print "===Video Details==="
print "Length = ", videolen, " seconds"
print "Total Frames = ", frameCt
print "fps = ", fps
print "height = ", height
print "width = ", width

print "===Data Details==="
print "Total Frames = ", len(data[0])
print "freq = ", freq

Y=[[0]]*len(data)
for i in xrange(len(data)):
	Y[i]+=data[i]


it=0
sty=500
stx=500
scale=10
	
it = 1
interval=500 # set display length interval
while True:

	flag, frame = cap.read()
	if (cv2.waitKey(1) == 27) or (flag==False):
        	print "Video Ended"
		break
   	
	for i in xrange(len(Y)):
		sty=100+((100*i))
		stx=100
		col = color[i%3]
		start=1
		if it>interval:
			start=it-interval
		cx=0	

		for j in xrange(start,it):
			#plot a line between every 2 adj points
			prevx=int(cx+stx)
			prevy=int(Y[i][j-1]*scale+sty)
			x=int(cx+1+stx)
			y=int(Y[i][j]*scale+sty)
			cx+=1
			cv2.line(frame,(prevx,prevy),(x,y),col,1) 
	
	cv2.imshow("video", frame)
    	it+=1
    
