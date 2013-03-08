from detect import *
from pyfaces_api import *

# generate face img in prob folder based on prob_source
gen_prob()
img, matches = rec_faces_in_img('gallery/6.jpg')
#img, matches = rec_faces_in_img('gallery/poster.jpg')

print matches
highlight_faces(img, matches)

