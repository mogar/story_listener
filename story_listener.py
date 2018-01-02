#!/usr/bin/env python3

""" Run a recognizer using Google Assistant Library to record bedtime stories."""


import os
import time
import subprocess
import smtplib, json

aiy_path = os.environ["AIYPATH"]
os.sys.path.append(aiy_path)
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

STORY_TELL = 'tell me a story'
STORY_ONCE = 'once upon a time'
STORY_END = 'the end'
AIY_TURN_OFF = 'aiy turn off'

STORY_FN = 'bedtime_story'


USE_BUTTON = False


class StoryDump(aiy.audio._WaveDump):
    """A processor that saves recorded audio to a file"""

    def __init__(self, filepath, max_duration):
        super().__init__(filepath, max_duration)
        self.done = False

    def add_data(self, data):
        max_bytes = self._bytes_limit - self._bytes
        data = data[:max_bytes]
        if data and not self.done:
            self._wave.writeframes(data)
            self._bytes += len(data)

    def finish(self):
        self.done = True
        self._wave.close()

    def is_done(self):
        return self.done or (self._bytes >= self._bytes_limit)

def email_story(story_txt_file):
    with open('/home/pi/story_listener.json') as auth_f:
        email_info = json.loads(auth_f.read())

        story_f =  open(story_txt_file, 'r')
        story_text = story_f.read()
        story_f.close()
         

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_info["user"], email_info["pw"])
            server.sendmail(email_info["user"], email_info["to"], story_text)
            server.quit()
        except:
            pass

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase(STORY_TELL)
    recognizer.expect_phrase(STORY_ONCE)
    recognizer.expect_phrase(STORY_END)
    recognizer.expect_phrase(AIY_TURN_OFF)

    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.OFF)

    button = aiy.voicehat.get_button()

    aiy.audio.set_tts_volume(30)
    aiy.audio.get_recorder().start()

    story_wav = None
    story_txt = None

    print('waiting for stories...')
    while True:
        if story_wav is None or story_wav.is_done():
            led.set_state(aiy.voicehat.LED.OFF)
            if USE_BUTTON:
                button.wait_for_press() 

        text = recognizer.recognize()
        if text is None:
           pass
        else:
            if story_txt is not None:
                story_txt.write(text + "\n")

            text = text.lower()
            print(text)
            if (STORY_TELL in text) or (STORY_ONCE in text):
                if story_wav is None or story_wav.is_done():
                    # start recording
                    story_fn = STORY_FN + time.strftime('_%d%m%Y-%H%M%S')
                    story_fn = '/home/pi/Documents/' + story_fn
                    print(story_fn)

                    story_wav =  StoryDump(story_fn + '.wav', 20*60) # max 20 min
                    aiy.audio.get_recorder().add_processor(story_wav)

                    story_txt = open(story_fn + '.txt', 'w')

                    led.set_state(aiy.voicehat.LED.ON)
                    #aiy.audio.say('story time!')

            elif STORY_END in text:
                if story_wav is not None and not story_wav.is_done():
                    # end recording
                    story_wav.finish()
                    story_txt.close()
                    email_story(story_fn + '.txt')
                    story_txt = None
                    aiy.audio.say('that was a good story')

            elif AIY_TURN_OFF in text:
                subprocess.call(["sudo", "shutdown", "-h", "now"])


if __name__ == '__main__':
    main()
