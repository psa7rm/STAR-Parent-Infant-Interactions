# STAR_Parent_Infant_Interactions

Dataset: Please access the shared outlook file sent from DuBay for the private data mp3 files & metadata excel files.

STAR_data_cleaning.py
   
- Python script focused on the preprocessing of the audio data, including conversion from audio to analysis-ready formats, segmentation, and feature extraction (Used for the metadata processing for the image data for the cnn model, later adapted for the raw matrix files in the lstm model). Segmentation was done due to the mp3 files varying in length, ranging from five minutes to three hours. We used the mp3 files that were broken into parts from the onedrive that were broken into hours. These files were then segmented and labeled based on the metadata excel files that were time stamped and labeled with the corresponding classification by other student workers.

- Metadata note: the metadata had overlap, so to ensure that the segmentation of the longer files were properly done, we added an overlap class to times where both the parent and infant were speaking, and if there was overlap between a human {adult or infant} and background, then we just labeled it the human speaking.
- For the CNN model we segmented the metadata increments further into 3-second segments to produce more training files.

Audio Classification (to better understand the architecture of each model, reference the presentation and final paper in the github): 

Multiclass Problem - { 0: adult, 1:infant, 2:background, 3:overlap } // advised to drop overlap class, due to its lack of training points

Model 1: CNN - ResNet50 (utilized image spectrograms - STAR_resnet_audio_classification.{py, ipynb})

Model 2: RNN - LSTM (utilized raw matrices spectrograms - STAR_lstm_audio_classification.{py, ipynb})

Randomly sampling segmented image/csv files in order to reduce bias and increase validation.

Prospects:

Improve the accuracy of the neural networks, possibly enacting ensemble models that can increase the accuracy of the predictions.

Class predictions with a 60% or above with test data. Ensure that the predictions are consecutive to a specific segmented audio file series in order to store the predicted values in a list/array that will aid in implementing the turn taking analysis.

Now, when doing the predictions portion, ensure that the unlabled files being predicted are from the same mp3 file, so that when it is time to implement the turn taking analysis, you will be able to implement if statements that can test whether or not the last person with the highest probability of speaking in the predictions, is or isn't the next human speaking, and if it is simply background noise, then it is not considered a switch off between adult-infant.

Turn taking analyis: if statements based on conversational switches between the parent and infant within the prediction list/array above (ensuring switches are within a 3-5 seconds of each other).

Highly recommend colabpro/AWS to run the image/csv files. Used a mixture of rivanna, AWS, and Azure to process raw data files.
