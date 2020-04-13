# optical_music_recognition

A program that, given a standard smartphone image of printed monophonic sheet music, can then apply the
proper image preprocessing, music symbol extraction using our deep-learning model, and data post-processing
to give a final output of both printed sheet music and an instrumental audio track of the original sheet music.

By: Daniel Manwiller, Andreea Serban, Rishi Barad, John Day, and Adam Kahana

Pre-process Images: config.py, pre_process.py, adjust_photos.py, photos folder, output folder
Model Prediction and Post-Processing: ctc_predict.py, ctc_utils.py, musescore442.py, vocabulary_442.txt

Version and Package Dependencies:
1. Python version 2.7
2. Tensorflow version 1.12
3. Music21 version 5.7.2
4. MuseScore3 OpenSource Program Installed

How to pre-process an image:
1. Under the main function in pre_process.py, change the path to the image in filename. 
2. Run pre_process.py 
3. In the output/staffs directory, there are portions of the staffs from the original image.

How to run the model prediction and post-process the data:
1. On line 10 of musescore442.py change the file path to be that of the executable for MuseScore3
2. In an Anaconda or similar environment run the following command: python ctc_predict.py -image TestStaff.png -model Models/agnostic_model.meta -vocabulary Data/vocabulary_442.txt

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
10. vocabulary_442.txt -> Dictionary of agnostic encoding translations for the deep-learning model output.
11. TestStaff.png -> Test image for example of running deep-learning model prediciton
12. Models folder : Contains trained models for the deep-learning classification
