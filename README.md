# optical_music_recognition

A program that, given a standard smartphone image of printed monophonic sheet music, can then apply the
proper image preprocessing, music symbol extraction using our deep-learning model, and data post-processing
to give a final output of both printed sheet music and an instrumental audio track of the original sheet music.

By: Daniel Manwiller, Andreea Serban, Rishi Barad, John Day, and Adam Kahana

Pre-process Images: config.py, pre_process.py, adjust_photos.py, photos folder, output folder

How to pre-process an image:
1. Under the main function in pre_process.py, change the path to the image in filename. 
2. Run pre_process.py 
3. In the output/staffs directory, there are portions of the staffs from the original image. 

Breakdown of the files: 
1. config.py -> Configurations of some parameters that were used in the pre_process.py and adjust_photos.py
2. pre_process.py -> Pre-process already adjusted images
3. adjust_photos.py -> Adjusts a photo to further analysis
4. ctc_predict.py -> Edited from [1]. Added functionality to itegrate with musescore442.py 
5. ctc_utils.py -> From [1]. Needed for ctc_predict.py
6. musescore442.py -> Converts Agnostic encoding translation to TinyNotation string and ports it to MuseScore
7. photos folder : Used for testing the pre-process implmentations. 
8. output folder : 
  Images of the edge dectection methods used to adjust the photo: 1canny.jpg, 2with_contours.png, 3adjusted_photo.png
  Images of the staff lines detected and the highlighted start of the staff and end of the detected staff: 5lines.png,           
9. staffs.png
  The separate cropped out staff lines after the original photo has been adjusted (staffs folder) 


