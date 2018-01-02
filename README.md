

Story Listener is an AIY project designed for the VoiceHat kit.

It listens for a few key-phrases indicating that a bedtime story has started, and then records the story being told. When the story ends, it emails it to you.

# Usage

If you want to be constantly looking for stories, you can use the software as is. Alternatively, you can require the app to wait for a button press before it starts listening to you.

Once the AIY kit and app are listening to you, you can use the following voice commands:

"Once upon a time" - start recording a story
"Tell me a story" - start recording a story
"The end" - stop recording and email a transcript
"AIY turn off" - turn off the device (requires power cycle to restart)

All recorded stories are saved as .wav files and as .txt files. The files are saved to the '/home/pi/Documents' directory by default. If you want to change that, you'll need to edit the python source.
## Privacy Note

This app uses Google's Cloud Speech API to transcribe what you say into text, then email to an email address you provide. This has all of the privacy risks that you might expect, so please use it responsibly.

# HW and API Setup

Set up your AIY kit according to the instructions. Once that's done, set up the cloud API and get your key for it.

Instructions for that can be found here:
https://aiyprojects.withgoogle.com/voice/#project-overview

# e-mail setup

If you provide SMTP credentials, the app will automatically email you the text of a story. It still saves .txt and .wav files for each story.

To set this up, just do the following:

    cp story_listener.json /home/pi
    nano /home/pi/story_listener.json

Then enter in your email address, password, and the email address that you'd like to send your stories to.

I just hard-coded the email server into the app, so if you're using something other than gmail to send your email you'll have to edit the python script directly. You may also want to set up a an app-specific password instead of using your gmail password directly.

# Service Setup

The story listener can be set up as a service, so that it runs whenever you plug in the AIY kit. This way, you can set it up headless (no keyboard, mouser, or monitor) and let it run wherever you tell your stories.

Several paths are hard-coded into the service definition, so if you're running this as a user other than 'pi' or you put this directory somewhere other than '/home/pi/Documents/story_listener' then you'll have to adapt the 'story_listener.service' file and the 'story_starter.sh' file.

To do this, run the following from this directory:

    sudo mv story_listener.service /lib/systemd/system
    sudo systemctl enable story_listener.service
    sudo service story_listener start


