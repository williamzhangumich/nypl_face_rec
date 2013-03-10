from detect import *
from pyfaces_api import *
import time

#################################################
## PART 1: Detect face, crop, resize, rotate ####
#################################################
cv.NamedWindow('Image_Window', cv.CV_WINDOW_AUTOSIZE)
#image, faces = detect_face('prob_source\Eden-Espinosa.jpg') # read and detect face

# Try the next one to see a failed eye detection...
#image, faces = detect_face('prob_source\Joel-Grey.jpg') # 1 eye...
image, faces = detect_face('prob_source\Kristoffer-Cusick.jpg') # 4 eyes....
# There should be ways to eliminated these failures

# Show original image
cv.ShowImage('Image_Window', image)
for face in faces:
    # crop, resize
    # note crop_resize calls rotate_face(img, face=None, show=False) to re-orient based on eye position!
    # Use show=True to highlight the eyes
    face_img = crop_resize(image, face,True) 
    # This will highlight eyes
    
    ##############################################
    ##### Need normalization for illunimation!!!! 
    #############################################
    
    # More notes on rotate_face(img, face=None, show=False)
    # Rotate based on eye position and make a much more accurate capture of face
    # Rotation could be unsuccessful (warning will be provided)
    # If so, will simple provide the haar face cascade detected face
    # Normally, you could just use rotated = rotate_face(face_img) because default is
    # the face argument is not required, it is the position of this face on original img, used to provide error message
    
    # Show the final image to be stored in prob
    cv.ShowImage('Final_Image_Window', face_img)
    
cv.WaitKey()
# Close images to continue


################################################
## PART 2: Face recognition with pyface api ####
################################################

# Demonstration of pyface api, using pyface provided sample faces in ./sample folder
# It matches the target image in ./sample/gallery with all faces in sample/prob foler
# Spit out matched_file_name, distance, and run_time
# Note that image format should not matter
# IMPORTANT: these face images in ./sample are under ideal illumination and cropping conditions
# which is why the matching could be so accurate. When doing further normalization, refer to these photos 
print "matching with pyface api"
matched_file, distance, run_time = api_pyface('sample/gallery/andy2.png', 'sample/prob', 6, 0.3)
print "Matched with %s with a distance of %f in %f seconds"% (matched_file, distance, run_time)
print "-"*20
time.sleep(5)


##############################################################
## PART 3: Generate ./prob folder face images for matching ###
##############################################################

# Here, we want to generate our own ./prob folder based on seed images in ./prob/source
# Ideally, the seed images should have identical lighting, contrast, background, etc...
# And we want to make our ./prob photos close to those in ./sample/prob, which would require:
# - Illumination normalization (which I don't have time for)
# - Adjusting and experimenting on various parameters defined as constants at the beginning of detect.py
# - - for example, FACE_SIZE, which determines the minimal pixel size of a face being recognized (thus the size of prob imgs)
# - Keep an eye on the outputs. If there are too many "eye detection failed, unable to rotate face", it's gonna be really bad..
# ./prob_source folder images should be named after the person in the picture!!!!!
gen_prob() 
# I imagine you would want to do gen_prob() for each set of pictures,
# run recognitions, purge ./prob, and run gen_prob() again for next set

print "-"*20
time.sleep(5)

##########################################################################
## PART 4: Big wrapper to process a photo (detect+normalize+recognize) ###
##########################################################################

# rec_faces_in_img(path) will detect faces in image at the path
# rezie, rotate, (normalize), crop all faces (generate a temp face img in ./temp folder)
# and use pyface api to compare the temp face with images in ./prob
# Returns (img_obj, mathces), where matches is a list like this:
# [{'face_pos':face_position, 'match':matchedfile, 'dist':distance}, .....]

# 1.jpg is just the photo of Idina-Menzel that is in prob
# Should return match and a distance of 0
# use clean_temp=True to auto purge temp folder
img, matches = rec_faces_in_img('gallery/1.jpg',True) 
print matches
# A tool to highlight matched person on image
# Just showing you should be able to do a lot based on the wrapper
highlight_faces(img, matches)

# Another img already in prob
img, matches = rec_faces_in_img('gallery/2.jpg', False)
print matches
highlight_faces(img, matches)

# 3.jpg is a pic of Kristin-Chenoweth, different from that in ./prob
# Returned the right match but with a distance of 0.327, which is too high, actually
# Did not have time to go through lots of experiment but it seems that currently, the mathing precision is bad
# Illunimation seems to be a huge problem (it is matching darker imgs with darker imgs...)
# Definitely need to add more normalization, test on different parameters to:
# - get less rotation failures
# - get smaller distances
img, matches = rec_faces_in_img('gallery/3.jpg')
print matches
highlight_faces(img, matches)


