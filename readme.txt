This package is to help recognizing faces for NYPL image collections. 

Key functions include:
- Face detection (opencv, haar cascade)
- Face image cropping, resizing
- Face re-orientation based on eye position 
- Face recognition with pyface api
- References for scraping image from Playbill Vault

Developed by William Zhang at New York Public Library of Performing Arts, Spring break 2013

Files and Folders:
example.py: program functionality run-down
detect.py: contains most key functions related to face detection and normalization
face_rotate.py: a script to rotate faces (http://docs.opencv.org/modules/contrib/doc/facerec/tutorial/facerec_video_recognition.html#aligning-face-images)
pyfaces_api.py: pyface api to recognize (match) faces
./gallery: includes a few sample images to be recognized
./prob_source: seed images to generate ./prob folder faces for recognition, these files should be properly named!!!
./prob: collection of faces to be compared with, should be normalized, well positioned and cropped
     
./cascades: includes haar cascade files for faces and eyes
./eigenfaces: stores pyface auto generated eigenface images 
./pyfaces: pyface package, with slight adjustment compared to official release (https://code.google.com/p/pyfaces/)
./sample: pyface sample images, could give ideas about how to crop, resize and normalize training sets of pictures.
./scrape: include reference and simple scraping codes for Playbill Vault
./temp: will be used to hold temporary images that are used in the recognition process.

For specific usages, please refer to example.py

TO-DO List:
Generally, we want the returned images of gen_prob() to look like those in ./sample/
1. Normalize illumination
2. Improve eye detection (reduce the more than 2 eyes cases and impute 1 eye cases?)
3. Adjust the parameters defined at the beginning of detect.py, could require much research and experiment
4. Collect seed images for prob_source folder. Scraping is an option but we would want these images to be as normalized as possible
5. If the performance is still limited, could try other algorithms like fisher 
