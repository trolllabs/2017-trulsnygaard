import argparse, time, cv2
from DetectPupil import DetectPupil
from calibrate import calibrate

#       construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-x", "--resx",         type=int, default=640,
	help="resolution in x")
ap.add_argument("-y", "--resy",         type=int, default=480,
	help="resolution in x")
ap.add_argument("-a", "--arduino",      type=int, default=1,
	help="connect to Arduino? 1/0")
ap.add_argument("-cb", "--calibrate",   type=int, default=0,
	help="calibrate? 0/1")
ap.add_argument("-d", "--display",      type=int, default=0,
	help="display? eye = 1, environment = 0")
ap.add_argument("-n", "--num",          type=int, default=1,
	help="The first picture has this number when taking snapshots. ")
args = vars(ap.parse_args())

num = args["num"]


# __________________Calibration ___________________

left = 250
right = 500
upper = 300
lower = 100

#       Override the above values if -cb = 1
if args["calibrate"] == 1:
        c = calibrate(,left,right,lower,upper)
        c.start()
        left, right, lower, upper = c.calibrate()
        c.stop()

# ______________________Initializing________________

#       Pupil detection
time.sleep(0.2)
pupil = DetectPupil((args["resx"],args["resy"]),32,args["arduino"],left, right, lower, upper)
pupil.start()
time.sleep(0.2)

#       Display positioning
cv2.namedWindow("Display",cv2.WINDOW_NORMAL)
cv2.moveWindow("Display",0,0)
cv2.resizeWindow("Display",512,args["resy"]*(1024/2)/args["resx"])

#       Environment display
if not args["display"]:
    from wireless import stream
    Environment = stream()
    Environment.start()

# ______________________Running____________________

while True:
        
#       Read position and size of pupil, and the current frame.
#       (x,y) is for "frame", (x_conv,y_conv) is for environment.
    x,y,x_conv,y_conv,r,frame = pupil.read()
 
#       Display the wireless image if not otherwise specified   
        if not args["display"]:           
            environment = Environment.read()
            if environment is not None:
                #cv2.circle(environment,(x_conv,y_conv),10,(0,0,255),3)
                cv2.moveWindow("Display",0,0)
                cv2.imshow("Display", environment)

#       Show the eye if -d = 1
        elif args["display"]:
            if frame is not None:
                    cv2.circle(frame,(x,y),r,(0,0,255),3)
                    cv2.imshow("Display", frame)

#       Stop the threads and exit the loop if "q" is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pupil.stop()
            if not args["display"]:
                    Environment.stop()
            break

#       If "a" is pressed, take a snapshot of the displayed image.
        if cv2.waitKey(33) & 0xFF == ord('a'):                
                if not args["display"]:
                        cv2.imwrite("/home/pi/images/environment%1d.jpg" % num,environment)
                elif args["display"]:
                        cv2.imwrite("/home/pi/images/eye%1d.jpg" % num,frame)
                num = num + 1



cv2.destroyAllWindows()
