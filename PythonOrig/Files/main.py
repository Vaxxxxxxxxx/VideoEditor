import sys
from settings import Settings
from toolkit import Toolkit


def check_thread(end_thread_trigger):
    if end_thread_trigger[0] == True:
        print('EXIT - Done')
        sys.exit()


class DataAndRender:
    def __init__(self, params, end_thread_trigger):
        # Variable
        self.__end_thread_trigger = end_thread_trigger
        # Render flow
        # pass configuration data into settings
        self.__settings = Settings(params)
        # Declare the toolkit
        self.__toolkit = Toolkit(self.__settings, self.__end_thread_trigger)

        # Start rendering
        self.pattern_for_video_creation()
        # Print video ready
        # The print statements are important and displayed through the in-app console
        print('Video ready')



    def pattern_for_video_creation(self):
        # Select video rendering approach (mode)
        # Read settings.py for more information about modes
        match self.__settings.get_mode:
            case 0:

                # Merge audio files from the folder into one output.mp3
                self.__toolkit.create_audio_sequence()
                check_thread(self.__end_thread_trigger)

                # Create video based on the provided image
                self.__toolkit.add_background()
                check_thread(self.__end_thread_trigger)

                # Add audio to the video
                self.__toolkit.add_audio()
                check_thread(self.__end_thread_trigger)

            case 1:

                self.__toolkit.create_audio_sequence()
                check_thread(self.__end_thread_trigger)

                # Create video based on the provided image and overlap with effect
                self.__toolkit.add_background_and_effect()
                check_thread(self.__end_thread_trigger)

                self.__toolkit.add_audio()
                check_thread(self.__end_thread_trigger)

            case 2:
                self.__toolkit.create_audio_sequence()
                check_thread(self.__end_thread_trigger)

                if self.__settings.get_effect_style > 0:  # effect -> enabled

                    # create background + effect
                    self.__toolkit.add_background_and_effect()
                    check_thread(self.__end_thread_trigger)

                    # visualize an audio and merge with background + effect (uses game engine)
                    self.__toolkit.add_audiobar()
                    check_thread(self.__end_thread_trigger)

                else:  # effect -> disabled

                    # create background
                    self.__toolkit.add_background()
                    check_thread(self.__end_thread_trigger)

                    # visualize an audio and merge with background (uses game engine)
                    self.__toolkit.add_audiobar()
                    check_thread(self.__end_thread_trigger)

                self.__toolkit.add_audio()

            case 3:
                self.__toolkit.create_audio_sequence()
                check_thread(self.__end_thread_trigger)
                # Generate required with game engine
                self.__toolkit.create_responsiveness()
                check_thread(self.__end_thread_trigger)
                # Add audio to the video
                self.__toolkit.add_audio()
            case _:
                print("Mode -> Not Found!")
