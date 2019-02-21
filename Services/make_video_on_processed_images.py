import time
import glob
import cv2

class create_video():

    def create(self,img_dir):
        i=0
        img_array = []
        for i in range(400):
            filename = img_dir + '/processed_%04d.png'%i
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width , height)
            img_array.append(img)
            i=i+1
            now=time.time()
            print(i)
            if i==2000:
                break
        out = cv2.VideoWriter('/home/tatras/project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

        for j in range(len(img_array)):
           out.write(img_array[j])
        out.release()



# create_video().create(img_dir="/home/tatras/cam_pics")
