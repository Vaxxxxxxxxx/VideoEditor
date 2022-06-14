"""
This class contain the list of ffmpeg commands that should be retrieved and sent into pipeline.
"""


class Video:
    @classmethod
    def get_ffmpeg_add_audio(cls, v_path, out_name):
        command1 = 'ffmpeg -progress pipe:1 -i ' + v_path + ' -i ../TempFrames/output.mp3 -shortest -map 0:v -map 1:a -r 24 -y -c copy ' + out_name
        return str(command1)

    @classmethod
    def get_ffmpeg_add_background(cls, i_path, audio_length, width, height):

        command1 = 'ffmpeg -progress pipe:1 -r 24 -loop 1 -i ' + i_path + ' -t 30 -s ' + str(width) + 'x' + str(
            height) + ' -pix_fmt yuv420p -y ../TempFrames/temp0.mp4'
        command2 = 'ffmpeg -progress pipe:1 -stream_loop -1 -i ../TempFrames/temp0.mp4 -t ' + str(
            audio_length) + ' -y -c copy ../TempFrames/temp.mp4'

        return str(command1), str(command2)

    @classmethod
    def get_ffmpeg_add_background_and_effect(cls, i_path, effect_length, effect_path, audio_length, width, height):

        command1 = 'ffmpeg -progress pipe:1 -loop 1 -i ' + str(i_path) + ' -stream_loop -1 -i ' + str(
            effect_path) + ' -t ' + str(effect_length) + ' -filter_complex "[0:v]scale=' + str(width) + ':' + str(
            height) + '[ou1];[1:v]scale=' + str(width) + ':' + str(
            height) + '[ou];[ou]colorkey=0x000000:0.5:0.5[ckout];[ou1][ckout]overlay[out];[out]format=yuv420p[output]" -map "[output]" -r 24 -y ../TempFrames/temp0.mp4'
        command2 = 'ffmpeg -progress pipe:1 -stream_loop -1 -i ../TempFrames/temp0.mp4 -t ' + str(
            audio_length) + ' -y -c copy ../TempFrames/temp.mp4'
        return str(command1), str(command2)

    @classmethod
    def get_ffmpeg_add_responsive_background(cls, width, height, e_path=None, audio_length=5):
        # With effect?
        # YES
        if e_path is not None:
            command1 = 'ffmpeg -stream_loop -1 -i ' + str(e_path) + ' -y -f rawvideo -vcodec rawvideo -s ' + str(
                width) + 'x' + str(
                height) + ' -pix_fmt bgra -r 24 -i - -filter_complex "[0:v]scale=' + str(width) + ':' + str(
                height) + '[ou1];[ou1]colorkey=0x000000:0.5:0.5[ckout];[1:v][ckout]overlay[out]" -map "[out]" -t ' + str(
                audio_length) + ' -an -b:v 1500k -vcodec libx264 -y ../TempFrames/temp.mp4'
            return str(command1)
        # NO
        else:
            command1 = 'ffmpeg -y -f rawvideo -vcodec rawvideo -s ' + str(width) + 'x' + str(
                height) + ' -pix_fmt bgra -r 24 -i - -t ' + str(
                audio_length) + ' -vf format=yuv420p -an -b:v 1500k -vcodec libx264 -y ../TempFrames/temp.mp4'
            return str(command1)

    @classmethod
    def get_ffmpeg_add_responsive_audiobar(cls, width, height, audio_length=5):
        command1 = 'ffmpeg -y -f rawvideo -vcodec rawvideo -s ' + str(width) + 'x' + str(
            height) + ' -pix_fmt bgra -r 24 -i - -t ' + str(
            audio_length) + ' -vf format=yuv420p -an -b 5000k -vcodec libx264 -y ../TempFrames/temp0.mp4'
        return str(command1)

    @classmethod
    def get_ffmpeg_overlap_audiobar_and_image(cls, screen_height, bar_height, style):
        # black bg
        if style == 1:
            command1 = 'ffmpeg -progress pipe:1 -i ../TempFrames/temp0.mp4 -i ../TempFrames/temp.mp4 -filter_complex "[0:v]colorkey=0x000000:0.5:0.5[ckout];[1:v][ckout]overlay=0:' + str(
                screen_height - bar_height) + '[out]" -map "[out]" -y ../TempFrames/temp00.mp4'
            return str(command1)
        # white bg
        else:
            command1 = 'ffmpeg -progress pipe:1 -i ../TempFrames/temp0.mp4 -i ../TempFrames/temp.mp4 -filter_complex "[0:v]colorkey=0xffffff:0.5:0.5[ckout];[1:v][ckout]overlay=0:' + str(
                screen_height - bar_height) + '[out]" -map "[out]" -y ../TempFrames/temp00.mp4'
            return str(command1)
