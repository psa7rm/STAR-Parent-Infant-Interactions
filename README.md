# STAR_Parent_Infant_Interactions

Dataset: Please access the shared outlook file sent from DuBay for the private data mp3 files & metadata excel files.

STAR_data_cleaning.py
   
- Python script focused on the preprocessing of the audio data, including conversion from audio to analysis-ready formats, segmentation, and feature extraction (Used for the metadata processing for the image data for the cnn model, later adapted for the raw matrix files in the lstm model).

Audio Classification: 

Multiclass Problem - { 0: adult, 1:infant, 2:background, 3:overlap } // advised to drop overlap class, due to its lack of training points

Model 1: CNN - ResNet50 (utilized image spectrograms - STAR_resnet_audio_classification.{py, ipynb})

Model 2: RNN - LSTM (utilized raw spectrograms - STAR_lstm_audio_classification.{py, ipynb})

Randomly sampling segmented image/csv files in order to reduce bias and increase validation.

Prospects:

Debrief Dr. DuBay and new lab student on findings.

Class predictions with a 60% or above with test data. Ensure that the predictions are consecutive to a specific segmented audio file series in order to store the predicted values in a list/array that will aid in implementing the turn taking analysis.

Turn taking analyis: if statements based on conversational switches between the parent and infant within the prediction list/array above (ensuring switches are within a 3-5 seconds of each other).

Highly recommend colabpro/AWS to run the image/csv files. Used a mixture of rivanna, AWS, and Azure to process raw data files.
