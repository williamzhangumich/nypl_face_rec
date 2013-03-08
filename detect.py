from cv2 import cv
import sys
import os
from pyfaces_api import api_pyface
import re
from face_rotate import *

# Minimum face size to be detected and recognized
# if prob_source pics have high resolution, should set this high
FACE_SIZE = 100

# height/width ratio of face captures
# Could influence plenty of things (e.g. eye detection)
# If you modify this, you would probably need to purge the prob folder
HW_RATIO = 1.1

# Num of significant eigenvectors
# This should probably be a variable, need further research
NUM_EIGENVECTOR = 8
# Threshold for distance, need more experiment, 0.5 is too high
DISTANCE_THRESHOLD = 0.5

# In rotation, offset is based on eye location
# larger offset would capture a larger face area
OFFSET = 0.25

# A multiplier for deteting a larger face region
# Because we want to still be able to capture whole faces after rotation
MARGIN_MULTIPLIER = 0.08

def detect_face(path):
    """
    Load target img in greyscale and detect faces
    usage: face(image file path)
    return img_object, faces
    faces = [((x,y,w,h), r), ......]
    """
    image=cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
    
    # haar face cascade
    storage = cv.CreateMemStorage()
    haar=cv.Load('cascades/haarcascade_frontalface_alt.xml')
    detected = cv.HaarDetectObjects(image, haar, storage, 1.2, 2,
                                    cv.CV_HAAR_DO_CANNY_PRUNING, (FACE_SIZE,FACE_SIZE))
    # return list of faces
    faces = []
    if detected:
        for face in detected:
            faces.append(face)
    return image, faces

def crop_resize(image, face):
    """
    return a cropped face img resized to FACE_SIZE*FACE_SIZE
    face: ((x,y,w,h), r)
    - essentially, these step should include normalization for illumination!!
    """
    x,y,w,h = face[0]
    
    # Use the multiplier to get a slightly larger area
    # to make sure we have whole faces after rotation
    rect_x = int(x-MARGIN_MULTIPLIER*w)
    rect_y = int(y-MARGIN_MULTIPLIER*h)
    rect_w = int(w + MARGIN_MULTIPLIER*w*2)
    rect_h = int(w + MARGIN_MULTIPLIER*h*2)
    
    # Crop out faces
    face_rect = cv.GetSubRect(image,(rect_x,rect_y,rect_w,rect_h))
    thumbnail = cv.CreateImage((FACE_SIZE, int(FACE_SIZE*HW_RATIO)), image.depth, image.nChannels)
    cv.Resize(face_rect, thumbnail)
    
    # Re-orient and crop again
    # The first crop made sure that only one face and two eyes in second crop
    rotated = rotate_face(thumbnail, face, False)
    
    ###################################################
    ## Should add codes to normalize illumination!! ###
    ###################################################
    
    # Normalize contrast
    #cv.EqualizeHist(image, image)
    # Gamma correction
    #corrected = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_32F, 3)
    #cv.ConvertScale(image, corrected, 1.0/255, 0)
    #cv.Pow(corrected, corrected, CORRECTION_VALUE)
    
    return rotated

def rotate_face(img, face=None, show=False):
    """
    Given the face thumbnail, detect eye position and adjust orientation
    - if show=False then highlight eyes in a frame
    - revert to haar face cascate detected face if eye detection fails
    - the face argument is not required, only used to generate proper error message
    """
    storage = cv.CreateMemStorage()
    # Eye detection
    haar=cv.Load('cascades/haarcascade_eye.xml')
    detected = cv.HaarDetectObjects(img, haar, storage, 
                                    1.2, 2, 0, (5,5))
    # highlight eyes if show=True
    if show:
        print detected
        cv.NamedWindow('eye_window', cv.CV_WINDOW_AUTOSIZE)
        for ((x,y,w,h), r) in detected:
            cv.Rectangle(img,(x,y),(x+w,y+h),(255,0,0),3,1)
        cv.ShowImage('eye_window', img)
    
    num_eyes = len(detected)
    
    ################################################
    ### Need to improve eye detecting performance ##
    ### to get a more normalized face             ##
    ################################################
    
    # if eye detection is successful
    if num_eyes==2:
        # determin which detected eye is left eye
        if detected[1][0][0]<detected[0][0][0]:
            x1, y1, w1, h1 = detected[1][0]
            x2, y2, w2, h2 = detected[0][0]
        else:
            x1, y1, w1, h1 = detected[0][0]
            x2, y2, w2, h2 = detected[1][0]

        # convert to PIL image to use the rotate module
        PIL_img = Image.fromstring("L", cv.GetSize(img), img.tostring())  
        # use the rotate+crop funcition for PIL img
        PIL_rotated = CropFace(PIL_img, 
                               (x1+w1/2.0, y1+h1/2.0), 
                               (x2+w2/2.0, y2+h2/2.0), 
                               (OFFSET,OFFSET), dest_sz=(FACE_SIZE,int(FACE_SIZE*HW_RATIO)))
        # convert back to opencv img instance
        cv_rotated = cv.CreateImageHeader(PIL_rotated.size, cv.IPL_DEPTH_8U, 1)
        cv.SetData(cv_rotated, PIL_rotated.tostring())
        return cv_rotated
    else:
        # if rotate failed, we want to cancel the margin multiplier effect
        # i.e, use the haar face cascate detected face (which could be quite inaccurate)
        
        w, h = cv.GetSize(img)
        rect_w = w/(1+2.0*MARGIN_MULTIPLIER)
        rect_x = (w - rect_w)/2
        rect_h = h/(1+2.0*MARGIN_MULTIPLIER)
        rect_y = (h-rect_h)/2
        
        face_rect = cv.GetSubRect(img,(int(rect_x),int(rect_y),int(rect_w),int(rect_h)))
        thumbnail = cv.CreateImage((FACE_SIZE, int(FACE_SIZE*HW_RATIO)), img.depth, img.nChannels)
        cv.Resize(face_rect, thumbnail)
        
        print 'eye detection failed, unable to rotate face: ', face, '%d eyes detected'%num_eyes
        return thumbnail

def gen_prob():
    """
    Loop through all photos in prob_source folder and generate face thumbnails in prob folder
    photos in gallery folder will be matched up against the photos in prob
    Thus photos in prob (prob_source) have to be properly named after the artists!!!
    - images could be of any format (will be converted to jpg thumbnails)
    """
    files_in_dir = os.listdir('./prob_source')
    for f in files_in_dir:
        print "generating prob based on : ", f
        image, faces = detect_face('./prob_source/'+f)
        count = 1
        for face in faces:
            # Uncomment next line will display thumbnails
            #cv.ShowImage('Image_Window_'+str(count), crop_resize(image, face))
            name = f.split('.')[0]
            crop_img = crop_resize(image, face)
            if isinstance(crop_img,int):
                print f, face, "is not valid - %d eyes detected"%crop_img
                continue
            cv.SaveImage('./prob/'+name+'.jpg', crop_img)
            count+=1
        cv.WaitKey()

def rec_faces_in_img(path, clean_temp=False):
    """
    Detect faces in the picture of a given path, for each face, match with imgs in prob folder.
    return [(face_position, matched_file, distance),....]
    - Use clean_temp=True to clean temp files in ./temp
    - images could be of any format (will be converted to jpg thumbnails)
    """
    face_matches = []
    image, faces = detect_face(path)
    i = 1
    for face in faces:
        print "face: ", i
        # create and save the face thumbnail
        cv.SaveImage('temp/temp%d.jpg'%i, crop_resize(image, face))
        # use pyface api to match thumbnail agains prob
        (matchedfile, distance, runtime) = api_pyface('temp/temp%d.jpg'%i, 'prob', NUM_EIGENVECTOR, DISTANCE_THRESHOLD)
        face_matches.append({'face_pos':face, 'match':matchedfile, 'dist':distance})
        i+=1
    #print face_matches
    if clean_temp:
        for f in os.listdir('./temp'):
            if re.search(r'.*\.jpg', f):
                os.remove('temp/'+f)
    return image, face_matches
        
def highlight_faces(img, face_matches):
    """
    Takes in rec_faces_in_img(path) result and highlight all recognized faces
    """
    cv.NamedWindow('Image_Window', cv.CV_WINDOW_AUTOSIZE)
    font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 1) 
    for face in face_matches:
        ((x,y,w,h), r) = face['face_pos']
        cv.Rectangle(img,(x,y),(x+w,y+h),(255,0,0),3,1)
        cv.PutText(img,re.findall(r'prob\\(.*)',str(face['match']))[0], (x,y),font, 100)
    
    cv.ShowImage('Image_Window', img)
    cv.WaitKey()
    
if __name__ == "__main__":
    """
    process an image, display cropped, resized and rotated thumbnail
    usage: python detect.py path
    """
    if len(sys.argv)<=1:
        print "usage: python detect.py path"
        exit()
    cv.NamedWindow('Image_Window', cv.CV_WINDOW_AUTOSIZE)
    image, faces = detect_face(sys.argv[1])
    for ((x,y,w,h), r) in faces:
        cv.Rectangle(image,(x,y),(x+w,y+h),(255,0,0),3,1)
    cv.ShowImage('Image_Window', image)
    count = 1
    for face in faces:
        face_img = crop_resize(image, face)
        rotated = rotate_face(face_img)
        cv.ShowImage('Image_Window_'+str(count), rotated)
        count+=1
    cv.WaitKey()