# symptomspace
Welcome to symptom.space! This is a demo project for HackDavis 2021! This is a project intended to streamline the existing COVID-19 survey procedures. To be clear, this is only a demo right now and not the official symptom survey. Therefore, feel free to mess around and answer some questions wrong.

Thank you to HackDavis, Doordash, Twilio, and GoogleCloud for helping power this project!

Why symptom.space over the existing symptom surveys?
- We validate surveys to be valid and current, while the current system is prone to error.
- Streamlined process. This means hopefully less waiting time in line for the dining commons.
- We keep logs of where people have been and when, so if someone reports themselves as positive, we can imediately psuedo contact trace and notify people via text.
- (Anyone who reports themselves as positive is kept anonymous!)

Thank you for looking at our project! From: 
Ashley Bilbery,
Karim Abou Najm,
Ian Chuang,
and Sarah Yunair.

Notes if you want to run this yourself, and in production:
- Replace .txt.sample files with .txt files with you own secrets! This includes api keys and cryptography.
- Twilio is disabled by defualt. The text messages that would have been sent are also in the console.
- You can re-enable Twilio by turning the two Falses into Trues in main.py
- Remember to change the Google auth keys in location.html and map.html. Hotlinking with our Google API keys will be disabled at some point...
