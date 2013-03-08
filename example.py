from detect import *
from pyfaces_api import *

#########################################
## Detect face, crop, resize, rotate ####
#########################################
cv.NamedWindow('Image_Window', cv.CV_WINDOW_AUTOSIZE)
image, faces = detect_face('prob_source\Eden-Espinosa.jpg') # read and detect face
cv.ShowImage('Image_Window', image)
count = 1
for face in faces:
    face_img = crop_resize(image, face) #crop, resize
    ##### Need normalization for illunimation!!!! #####
    rotated = rotate_face(face_img) # rotate based on eye position
    cv.ShowImage('Image_Window_'+str(count), rotated)
    count+=1
cv.WaitKey()

######################################################
## Generate ./prob folder face images for matching ###
######################################################
gen_prob()


# generate face img in prob folder based on prob_source

img, matches = rec_faces_in_img('gallery/6.jpg',True)
#img, matches = rec_faces_in_img('gallery/6.jpg')
#img, matches = rec_faces_in_img('gallery/poster.jpg')

print matches
highlight_faces(img, matches)

