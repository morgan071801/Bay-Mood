#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import time
import threading
from datetime import datetime
from pathlib import Path
import os
import shutil

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def main():
    now= datetime.now()
    year_string = now.strftime("%Y")
    month_string = now.strftime("%m")
    day_string = now.strftime("%d")
    time_string = now.strftime("%H:%M:%S")
    year_path = '/home/pi/Journal/Journal_Entries/'+year_string
    month_path = '/home/pi/Journal/Journal_Entries/'+year_string+'/'+month_string
    day_path = '/home/pi/Journal/Journal_Entries/'+year_string+'/'+month_string+'/'+day_string
    current_path = '/home/pi/Journal/Code/Journal_Entries/'+time_string+'.wav'
    
    
   
        
       
        
   
    
    print(now)
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default=day_path+'/'+time_string+'.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Start Journaling.')
        board.button.wait_for_press()
        if not os.path.exists(year_path):
            os.makedirs(day_path)
        
        if not os.path.exists(month_path):
            os.makedirs(day_path)
        
        if not os.path.exists(day_path):
            os.makedirs(day_path)
   

        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')
        #shutil.move(current_path, day_path)
        print('Press button to play recorded sound.')
        board.button.wait_for_press()

        print('Playing...')
        play_wav(args.filename)
        print('Done.')

if __name__ == '__main__':
    main()
    
