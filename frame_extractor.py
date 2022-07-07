import os
import cv2

path = "/Users/tanmaygoyal/Downloads/test_videos/" # TO BE EDITED
output = path+"dataset/"
list_videos = []

for filename in os.listdir(path):
    if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
        list_videos.append(path+filename)

already_processed = []

if os.path.exists(output):
    # getting a list of already processed videos
    with open(output + 'videos.txt') as f:
        lines = f.readlines()
        for line in lines:
            already_processed.append(line)

else:
    os.makedirs(output)


videos = output + "videos/"
os.makedirs(videos , exist_ok = True)

counter = len(already_processed) # for naming purposes of video

for filename in list_videos:
    if filename + '\n' not in already_processed:
        
        with open(output + 'videos.txt' , 'a') as f:
            f.write(filename + '\n')

        os.chdir(videos)
        os.system("ffmpeg -i {} -vf mpdecimate,setpts=N/FRAME_RATE/TB out_{}.mp4".format(filename ,counter))
        
        new_path_GT = output + "GT/" + str(counter).zfill(7)
        new_path_LR = output + "LR/" + str(counter).zfill(7)
        
        os.makedirs(new_path_GT , exist_ok = True)
        os.makedirs(new_path_LR , exist_ok = True)
        
        os.chdir(new_path_GT)
        
        vidcap = cv2.VideoCapture(videos + "/out_" + str(counter)+".mp4")
        print(vidcap)

        count = 0

        print(vidcap.isOpened())

        while(vidcap.isOpened()):
            ret, image = vidcap.read()
            
            if(ret):
                half_image = cv2.resize(image ,(0,0), fx = 0.5 , fy = 0.5 , interpolation = cv2.INTER_CUBIC)
                cv2.imwrite(new_path_GT + "/frame%d.png" % count, image)
                cv2.imwrite(new_path_LR + "/frame%d.png" % count, half_image)
                count += 1
            else:
                break

        vidcap.release()
        print("Video done")
        os.remove(videos[:-1] + "/out_" + str(counter)+".mp4")
        counter+=1

os.rmdir(videos)
