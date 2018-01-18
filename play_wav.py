#!/usr/bin/env python3

"""Play a wave file using AIY. Mostly this is to play back a story from the story_recorder"""

import os

aiy_path = os.environ["AIYPATH"]
os.sys.path.append(aiy_path)
import aiy.audio
import argparse

parser = argparse.ArgumentParser(description="Play a wav file.")
parser.add_argument('--file', dest='f', help='path to wav file', required=True)
args = parser.parse_args()

aiy.audio.play_wave(args.f)

