import cv2
import os

# Note: give the script sufficient permissions to write the images to your directory of choice
# EX: sudo chmod calibration_script.py 777

def gstreamer_pipeline(
    capture_width=3264,
    capture_height=2464,
    framerate=21,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "format=(string)NV12, width=(int)%d, height=(int)%d, "
        "framerate = (fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
        )
    )

def show_camera():
    pic_num = 0
    path = './calib_images'
    print(gstreamer_pipeline(flip_method=2))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_NORMAL)
    while cap.isOpened():
        ret_val, img = cap.read()
        if ret_val:
            keyCode = cv2.waitKey(30) & 0xFF
            if keyCode == 27:
                print("Closing...")
                break
            elif keyCode == 32:
                print("saving image: " + os.path.join(path , 'imx219_calib_'+str(pic_num)+'.jpg'))
                #cv2.imwrite(os.path.join(path , 'imx219_calib_'+str(pic_num)+'.jpg'), img)
                if not cv2.imwrite(os.path.join(path , 'imx219_calib_'+str(pic_num)+'.jpg'), img):
                    print("failed to save img")
                cv2.imshow("CSI Camera", img)
                pic_num+=1
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    show_camera()