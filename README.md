Note: Planed rework in the near future.

After shadowing an orthopaedic surgeon, I identified the significant amount of time spent documenting patient consultations between appointments. This inspired me to independently design and develop MediScript, a lightweight, fully offline medical transcription and patient management system designed to streamline clinical documentation while maintaining local control over sensitive patient data.

MediScript performs near real-time transcription of patient consultations using Vosk's lightweight English speech recognition model. The system stores patient information and consultation transcripts locally, with the capability to be configured for integration with a medical centre's database.

To improve the readability and usability of transcripts, I developed an NLP processing pipeline using NLTK to analyse conversational context, improve transcription accuracy through context-aware word correction, and classify the likely speaker within each part of the conversation, such as the doctor, patient, or another participant.

A significant technical challenge was enabling continuous near real-time transcription. The selected Vosk model did not natively support the live transcription workflow required by the application, so I designed and implemented an in-house solution that processed the incoming conversation into smaller audio clips, enabling continuous transcription.
