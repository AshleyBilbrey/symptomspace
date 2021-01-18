# symptomspace
http://symptom.space
Welcome to symptom.space! This is a demo project for HackDavis 2021! This is a project intended to streamline the existing COVID-19 survey procedures, and provide a more safe environment for all. To be clear, the presented code is only a demo and not the official symptom survey. Therefore, feel free to mess around and answer some questions wrong while exploring what we have created.

Thank you to HackDavis, Doordash, Twilio, and GoogleCloud for helping power this project!

NOTE: Project temporarily is giving everyone scanner permission for the purpose of demo. Ordinarily this will be locked.

Why symptom.space over the existing symptom surveys?
- Validated surveys confirm when they were filled and their authenticity, while the current system is prone to error.
- Streamlined process. This means less waiting time indoors, which due to the close proximity of students despite regulations will help curb transmissions.
- Logged visiting locations allows people to be notified if they were indoors with someone who has been tested positive for COVID. Through psuedo contact trace, we can notify people of their danger.
- Provided option to report self as having COVID.

Thank you for looking at our project! From:
Ashley Bilbery,
Karim Abou Najm,
Ian Chuang,
and Sarah Yunair.

Notes if you want to run this yourself:
- Download the necessary libraries from requirements.txt;
- Replace .txt.sample files with .txt files, which will be populated with your own secrets! This includes api keys and cryptography;
- Twilio is disabled by default. The text messages that would have been sent are also in the console;
- You can re-enable Twilio by turning the two Falses into Trues in main.py;
- Passwords of new users will be found in the terminal upon the running of the Flask server in main.py and attempting to create a new user;
- Remember to change the Google auth keys in location.html and map.html. Hotlinking with our Google API keys will be disabled at some point...

Thanks again!

Best,
symptom.space
