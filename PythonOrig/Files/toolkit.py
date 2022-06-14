import math
import random
import librosa
import pygame
import subprocess as sp
from moviepy.editor import *
from subprocess import Popen
from audioInitializer import AudioInitializer
from responsiveAudio import ResponsiveAudio
from responsiveImage import ResponsiveImage
from video import Video
from effect import Effect


# Checks if stop button was clicked
def check_thread(end_thread_trigger, p):
    if end_thread_trigger[0]:
        print('EXIT - Done')
        p.terminate()
        sys.exit()


# Create a video sequence from frame buffers
def add_frame(fout, screen):
    test = screen.get_buffer()
    fout.write(test)


# This is a multitool class that contain list of rendering funcitons
class Toolkit:
    def __init__(self, settings, end_thread_trigger):
        self.__end_thread_trigger = end_thread_trigger
        # Settings class
        self.__settings = settings
        # class with FFmpeg commands
        self.__video = Video()
        self.__effect = Effect(settings.get_effect_style)
        # Keep the path to the last version of the file
        self.__latest_video_file = '../TempFrames/temp.mp4'
        # output.mp3 length
        self.__audio_length = None

    def add_audio(self):
        # print in app's console
        print("Adding audio - Start")
        # retrieve command from the Video class
        command1 = self.__video.get_ffmpeg_add_audio(self.__latest_video_file, '../video.mp4')
        # execute command and keep the log
        p = sp.Popen(command1, stdout=sp.PIPE, creationflags=0x08000000)
        # while rendering
        while True:
            # take ffmpeg output
            line = p.stdout.readline()
            # decode ffmpeg output
            out = line.decode('utf-8').rstrip()
            # output ffmpeg output
            print("Processing(_1_)..." + str(out))
            # execution finished
            if not line:
                # make sure that everything is done and continue the program
                p.wait()
                break

        # Update latest video file
        self.__latest_video_file = '../video.mp4'
        # print in app's console
        print("Adding audio - Done")

    def add_background(self):
        print("Generating video - Start")
        # retrieve command from the Video class
        command1, command2 = self.__video.get_ffmpeg_add_background(self.__settings.get_background_path, self.__audio_length,
                                                                    self.__settings.get_screen_width,
                                                                    self.__settings.get_screen_height)

        p = sp.Popen(command1, stdout=sp.PIPE, creationflags=0x08000000)
        while True:
            # take ffmpeg output
            line = p.stdout.readline()
            # decode ffmpeg output
            out = line.decode('utf-8').rstrip()
            # output ffmpeg output
            print("Processing(_1_)..." + str(out))
            # Check if the process need to be stopped
            check_thread(self.__end_thread_trigger, p)
            # execution finished
            if not line:
                # make sure that everything is done and continue the program
                p.wait()
                break

        p = sp.Popen(command2, stdout=sp.PIPE, creationflags=0x08000000)
        while True:
            # take ffmpeg output
            line = p.stdout.readline()
            # decode ffmpeg output
            out = line.decode('utf-8').rstrip()
            # output ffmpeg output
            print("Processing(_1_)..." + str(out))
            # execution finished
            if not line:
                # make sure that everything is done and continue the program
                p.wait()
                break

        # Update latest video file
        self.__latest_video_file = '../TempFrames/temp.mp4'
        print("Generating video - Done")

    def add_background_and_effect(self):
        print("Generating video - Start")
        # getting necessary variables and then retrieve command from the Video class
        effect_path = self.__effect.get_effect_path
        effect_video = VideoFileClip(effect_path)
        effect_length = math.floor(effect_video.duration)
        command1, command2 = self.__video.get_ffmpeg_add_background_and_effect(self.__settings.get_background_path, effect_length,
                                                                               effect_path,
                                                                               self.__audio_length, self.__settings.get_screen_width,
                                                                               self.__settings.get_screen_height)

        p = sp.Popen(command1, stdout=sp.PIPE, creationflags=0x08000000)
        while True:
            # take ffmpeg output
            line = p.stdout.readline()
            # decode ffmpeg output
            out = line.decode('utf-8').rstrip()
            # output ffmpeg output
            print("Processing(_1_)..." + str(out))
            # Check if the process need to be stopped
            check_thread(self.__end_thread_trigger, p)
            # execution finished
            if not line:
                # make sure that everything is done and continue the program
                p.wait()
                break

        p = sp.Popen(command2, stdout=sp.PIPE, creationflags=0x08000000)
        while True:
            # take ffmpeg output
            line = p.stdout.readline()
            # decode ffmpeg output
            out = line.decode('utf-8').rstrip()
            # output ffmpeg output
            print("Processing(_1_)..." + str(out))
            # execution finished
            if not line:
                # make sure that everything is done and continue the program
                p.wait()
                break

        self.__latest_video_file = '../TempFrames/temp.mp4'
        print("Generating video - Done")

    def create_audio_sequence(self):

        '''
        This is NOT the fastest approach, however it gives a huge flexibility for future updates
        It is possible to mix tracks , loop them, read metadata and so forth.
        '''

        # Variables to merge audio files into output.mp3
        processed_tracks = 0
        number_of_tracks = self.__settings.get_number_of_tracks
        audio_sequence = []
        audio_folder = self.__settings.get_music_folder

        # Mix all the tracks in the folder
        track_list = [audio_folder + '/' + file for file in os.listdir(audio_folder) if
                      file.endswith(".mp3")]  # mp3 support only!
        random.shuffle(track_list)  # mix

        # Pick tracks
        # if number_of_tracks > track_list:
        for track in track_list:
            audio_sequence.append(AudioFileClip(track))
            processed_tracks += 1
            # if the amount of tracks is equals to user's request -> stop merging tracks
            if processed_tracks == number_of_tracks:
                break

        # Concatenate tracks into mp3 file
        audio_track = concatenate_audioclips([audio for audio in audio_sequence])
        audio_track.write_audiofile('../TempFrames/output.mp3')
        # it is important to have audio length = integer (ffmpeg requirement) rounded to bottom (widio should exist only while music playing).
        self.__audio_length = math.floor(librosa.get_duration(filename='../TempFrames/output.mp3'))

    # add audio-bar
    def add_audiobar(self):
        print("Generating audiobar - Start")
        # Class that is responsible for audio bar design and scalability
        r_audio = ResponsiveAudio(self.__settings.get_audio_bar_style, self.__settings.get_mode, self.__settings.get_screen_width,
                                  self.__settings.get_screen_height, True)
        # Retrieve command from the Video class
        command1 = self.__video.get_ffmpeg_add_responsive_audiobar(r_audio.get_width, r_audio.get_height, self.__audio_length)

        # Variables
        fps = 24
        frame = 0
        print_counter = 0
        # Analise Audio
        print("Sound analysis - Start...")
        audio_info = AudioInitializer()
        print("Sound analysis - Done")
        # start pygame
        pygame.init()
        # create hidden window
        screen = pygame.display.set_mode([r_audio.get_width, r_audio.get_height], flags=pygame.HIDDEN)
        # Start rendering
        p = Popen(command1, stdin=sp.PIPE, creationflags=0x08000000)
        # use variable = p.stdin to avoid some crashes
        fout = p.stdin
        # while audio exist -> render
        while frame <= self.__audio_length * fps:
            # Check if the process need to be stopped
            check_thread(self.__end_thread_trigger, p)
            # notify user every second
            print_counter += 1
            if print_counter % 24 == 0:
                print('Processing...  ' + str(int(frame / fps)) + ' / ' + str(self.__audio_length))
            # reset buffer, update bars position and scaling
            r_audio.run(screen, fps, frame, audio_info)
            # add frame to the video sequence that is in creation
            add_frame(fout, screen)
            # Next frame
            frame += 1

        # quit
        pygame.display.quit()
        p.stdin.close()
        fout.close()
        # wait until is done
        p.wait()

        # notify user
        print("Generating audiobar - Done")
        print("Merge audiobar and background - Start")
        # retrieve command
        command2 = self.__video.get_ffmpeg_overlap_audiobar_and_image(r_audio.get_screen_h, r_audio.get_height, r_audio.get_style)
        # Render
        p = sp.Popen(command2, stdout=sp.PIPE, creationflags=0x08000000)
        while True:
            line = p.stdout.readline()
            out = line.decode('utf-8').rstrip()
            # Check if the process need to be stopped
            check_thread(self.__end_thread_trigger, p)
            print("Processing(_2_)..." + str(out))
            if not line:
                p.wait()
                break

        # Update latest file
        self.__latest_video_file = '../TempFrames/temp00.mp4'
        print("Merge audiobar and background - Done")

    # mode 3 create video
    def create_responsiveness(self):

        print("Generating video - Start")

        # Load class ResponsiveImage and Responsive Audio
        r_image = ResponsiveImage(self.__settings.get_background_style, self.__settings.get_background_path,
                                  self.__settings.get_screen_width, self.__settings.get_screen_height)
        r_audio = ResponsiveAudio(self.__settings.get_audio_bar_style, self.__settings.get_mode, self.__settings.get_screen_width,
                                  self.__settings.get_screen_height)

        # start pygame
        pygame.init()

        # Responsive background?
        if self.__settings.get_background_style == 0:  # NO
            # create screen
            screen = pygame.display.set_mode([r_audio.get_width, r_audio.get_height], flags=pygame.HIDDEN)
            # retrieve ffmpeg command
            command1 = self.__video.get_ffmpeg_add_responsive_audiobar(r_audio.get_width, r_audio.get_height, self.__audio_length)
            # set what to update
            video_elements = [r_audio]
        else:  # YES
            # create screen
            screen = pygame.display.set_mode([r_image.get_screen_w, r_image.get_screen_h], flags=pygame.HIDDEN)
            # retrieve ffmpeg command
            command1 = self.__video.get_ffmpeg_add_responsive_background(r_image.get_screen_w, r_image.get_screen_h,
                                                                         self.__effect.get_effect_path,
                                                                         self.__audio_length)
            # set what to update
            if self.__settings.get_audio_bar_style == 0:
                video_elements = [r_image]
            else:
                # order is important here
                video_elements = [r_image, r_audio]

        # Variables
        fps = 24
        frame = 0
        print_counter = 0
        # Analise Audio
        audio_info = AudioInitializer()
        # rendering
        p = Popen(command1, stdin=sp.PIPE, creationflags=0x08000000)
        fout = p.stdin
        # while audio exists
        while frame <= self.__audio_length * fps:
            # Check if the process need to be stopped
            check_thread(self.__end_thread_trigger, p)
            # notify user every second
            print_counter += 1
            if print_counter % 24 == 0:
                print('Processing...  ' + str(int(frame / fps)) + ' / ' + str(self.__audio_length))

            # Update video elements
            for element in video_elements:
                element.run(screen, fps, frame, audio_info)

            add_frame(fout, screen)
            # Next frame
            frame += 1

        # Done! Time to quit.
        pygame.display.quit()
        p.stdin.close()
        fout.close()
        p.wait()
        self.__latest_video_file = '../TempFrames/temp.mp4'
        print("Generating video - Done")
