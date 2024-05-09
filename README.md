# STAR_Parent_Infant_Interactions

Dataset: Please access the shared outlook file sent from DuBay for the private data mp3 files & metadata excel files.

Audio Classification: 

Multiclass Problem - { 0: adult, 1:infant, 2:background, 3:overlap } // advised to drop overlap class, due to its lack of training points

Model 1: CNN - ResNet50 (utilized image spectrograms)
Model 2: RNN - LSTM (utilized raw spectrograms)

Randomly sampling segmented image/csv files in order to reduce bias and increase validation.

Prospects:

Debrief Dr. DuBay and new lab student on findings.

Class predictions with a 60% or above with test data. Ensure that the predictions are consecutive to a specific segmented audio file series in order to store the predicted values in a list/array that will aid in implementing the turn taking analysis.

Turn taking analyis: if statements based on conversational switches between the parent and infant within the prediction list/array above (ensuring switches are within a 3-5 seconds of each other).

Highly recommend colabpro/AWS to run the image/csv files. Used a mixture of rivanna, AWS, and Azure to process raw data files.

Detailed File Descriptions:

1. STAR_final_paper.pdf

- A comprehensive paper detailing the research conducted on the machine learning audio classification of parent-infant interactions. It includes:

- Abstract and Introduction: Overview of the project's goal to classify audio for early autism interventions in Latinx communities.

- Data Description: Information on the dataset used, consisting of about 200 hours of audio from Latinx families.

- Methodology: Describes the machine learning models used, data preprocessing, and model development (CNN and LSTM).

- Results: Presents the findings, accuracy, and performance of the models.

- Discussion and Conclusion: Discusses the implications of the findings and the potential for future research and application.


2. STAR_findings_presentation.pdf
   
- A presentation format of the research findings, structured to cover:

- Purpose and Background: Justifies the research and links it to the broader mission of improving autism interventions.

- Scope: Outlines the data used and the target variables and predictors.

- Methodology: Summarizes the technical approaches, including the CNN and LSTM architectures used.

- Results: Highlights the performance metrics of each model.

- Final Thoughts: Discusses takeaways, applications, future work, and acknowledgements.

3. STAR_resnet_audio_classification.py and STAR_lstm_audio_classification.py
   
- Python scripts containing the implementation of the CNN and LSTM models, respectively. These would include the setup of model architectures, training procedures, and possibly the evaluation metrics used.

4. STAR_data_cleaning.py
   
- Python script focused on the preprocessing of the audio data, including conversion from audio to analysis-ready formats, segmentation, and feature extraction.
  
