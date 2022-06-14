import math
import os
from threading import Thread
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import main as render
import sys

'''
Hower Button class exists in order to replace button color when mouse enters/leaves the button
'''


class HoverButton(tkinter.Button):
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


'''
This class is responsible for an interface (GUI)
'''


class Videomusic(Tk):
    def __init__(self):
        super().__init__()
        # Colours used throughout the design
        self.background_col = '#202124'  # background
        self.dark_grey_col = '#141518'  # dark grey
        self.light_blue_col = '#72a4e8'  # light blue
        self.blue_col = '#609beb'  # blue
        self.white_text_col = '#f1f3f4'  # white text
        self.grey_text_col = '#bdc1c6'  # grey text

        # Window setup
        self.geometry("700x500")
        self.resizable(False, False)
        self.title('Visual Audio')
        self.iconbitmap('logo.ico')
        self.configure(bg=self.background_col)

        # Variables that will be sent into the toolkit.py and settings.py at the start of the rendering
        self.rb_bg_variable = None
        self.rb_effect_variable = None
        self.rb_audio_variable = None
        self.folder_path = None
        self.file_path = None
        self.number_of_tracks = None
        self.image_height = None
        self.image_width = None

        # Wrapper around variables that will be sent into the toolkit.py and settings.py at the start of the rendering
        self.configuration = []

        # Variables
        self.browse_button1 = None
        self.browse_button2 = None
        self.max_number_of_tracks = None

        # General window style
        self.canvas = Canvas(self, width=250, height=500, bg=self.dark_grey_col, bd=0, highlightthickness=0)
        self.canvas.place(x=450, y=0)


    # Function that is responsible for the browse image button, image size and its functionality
    def browse_image(self):

        # Each time user type in image width this function called
        def update_image_width(*args):
            try:
                # Go through some constraints
                # if everything is ok then update
                # else -> do nothing
                # get input
                self.image_width = temp_width_number.get()
                # value < 10 000 px
                if self.image_width < 10000:
                    # must be divisible by 2 (ffmpeg requirement)
                    # Section here convert value entered by user into suitable. This is done in a silent mode
                    # (however user still can see it in the configuration tab in gui)
                    # e.g 17 px will be converted into divisible by 2 (16)
                    self.image_width = int(self.image_width / 2) * 2
                    # Update width in the cofiguration tab
                    data_img_size.configure(text=str(self.image_width) + 'x' + str(self.image_height),
                                            foreground='green')
                    # Update preview image
                    self.preview_image()

                # limitation reached -> do nothing
                else:
                    pass
            except:
                pass

        # Each time user type in image hight this function called
        # Similar to the previous one
        def update_image_height(*args):
            try:
                # get input
                self.image_height = temp_height_number.get()
                # value < 10 000 px
                if self.image_height < 10000:
                    # must be divisible by 2 (ffmpeg requirement)
                    self.image_height = int(self.image_height / 2) * 2

                    data_img_size.configure(text=str(self.image_width) + 'x' + str(self.image_height),
                                            foreground='green')
                    # Update preview image
                    self.preview_image()
                # limitation reached -> do nothing
                else:
                    pass
            except:
                pass

        # Variables that will be updated
        # Width and height variables that must be filled in by the user
        temp_width_number = IntVar()
        temp_height_number = IntVar()
        # Width and height fields that must be filled in by the user
        entry_width = Entry(self, textvariable=temp_width_number, state='disabled', width=6, relief=FLAT,
                            justify=CENTER)
        entry_height = Entry(self, textvariable=temp_height_number, state='disabled', width=6, relief=FLAT,
                             justify=CENTER)
        #Positioning
        entry_width.place(x=310, y=79)
        entry_height.place(x=363, y=79)
        # Call update_image_width and update_image_height on entry update
        temp_width_number.trace_add("write", update_image_width)
        temp_height_number.trace_add("write", update_image_height)


        # Browse image button functionality
        def file_dialog():
            # Open file explorer (start -> root;)
            # It will allow to select only suitable files. However it is also possible to switch from png jpg to All files.
            # This option is left because theoretically this editor is able to support other video formats as well.
            filename = filedialog.askopenfilename(initialdir='/',
                                                  title='Select An Image',
                                                  filetypes=(
                                                            ('png jpg', ('*.png','*.jpg')),
                                                            ('All Files', '*.*'))
                                                            )

            # if image was selected successfully
            if filename:
                try:
                    self.file_path = filename
                    # Upload image photo
                    image = ImageTk.PhotoImage(file=r'' + filename)
                    # setup dimensions format
                    dimensions = "%dx%d" % (image.width(), image.height())
                    # extract width and height from the image
                    self.image_width = image.width()
                    self.image_height = image.height()
                    #Extract filename from the browsed path)
                    printed_filename = filename.split('/')
                    printed_filename = printed_filename[-1]
                    # print filename and dimensions
                    data_img_browse.configure(text=printed_filename, foreground='green')
                    data_img_size.configure(text=dimensions, foreground='green')

                    # update entry fields
                    entry_width.configure(state='normal')
                    entry_height.configure(state='normal')
                    entry_width.delete(-1, last=END)
                    entry_width.insert(0, self.image_width)
                    entry_height.delete(-1, last=END)
                    entry_height.insert(0, self.image_height)

                except:
                    # do nothing
                    pass

        # Browse button
        self.browse_button1 = HoverButton(self, width=20, activebackground=self.light_blue_col, text='Browse image', bg=self.blue_col,
                                          foreground=self.white_text_col, relief=FLAT, font=("Helvetica", 12),
                                          command=file_dialog)
        # Labels
        data_img_browse = Label(self, text="none", background=self.dark_grey_col, foreground='red', font=("Helvetica", 10))
        data_img_size = Label(self, text="none", background=self.dark_grey_col, foreground='red', font=("Helvetica", 10))
        # Positioning
        # filename
        data_img_browse.place(x=520, y=70)
        # dimensions
        data_img_size.place(x=528, y=100)
        self.browse_button1.place(x=20, y=70)

    # Function that is responsible for the browse audio button, number of tracks and its functionality
    def browse_audio(self):

        # Update number of tracks each time it is changed (if constraints passed)
        def update_number_of_tracks(*args):
            try:
                # if user specified more tracks that available then replace and apply user input with max available
                if temp_audio_tracks.get() > self.max_number_of_tracks:
                    num_of_tracks.configure(text=str(self.max_number_of_tracks), foreground='green')
                    entry_audio_tracks.delete(-1, last=END)
                    entry_audio_tracks.insert(0, self.max_number_of_tracks)
                    self.number_of_tracks = self.max_number_of_tracks
                # if user specified less tracks than possible then replace and apply user input with 0
                elif temp_audio_tracks.get() <= 0:
                    self.number_of_tracks = 0
                    num_of_tracks.configure(text=str(self.number_of_tracks), foreground='red')
                    entry_audio_tracks.delete(-1, last=END)
                    entry_audio_tracks.insert(0, str(self.number_of_tracks))
                # apply user input
                else:
                    num_of_tracks.configure(text=str(temp_audio_tracks.get()), foreground='green')
                    self.number_of_tracks = temp_audio_tracks.get()
            except:
                # do nothing
                pass

        # Variable that will be updated (entry variable)
        temp_audio_tracks = IntVar()
        # Reset max number of tracks
        self.max_number_of_tracks = 0
        # Create entry
        entry_audio_tracks = Entry(self, textvariable=temp_audio_tracks, state='disabled', width=8, relief=FLAT,
                                   justify=CENTER)
        # Positioning
        entry_audio_tracks.place(x=350, y=218)
        # Call update_number_of_tracks on entry update
        temp_audio_tracks.trace_add("write", update_number_of_tracks)

        # Browse audio button functionality
        def file_dialog():

            # Look for directory

            filename = filedialog.askdirectory(initialdir='/', title='Select Audio Folder')

            #If filename is correct
            if filename:
                try:
                    # apply audio path
                    self.folder_path = filename
                    # Retrieve and print folder name from the path
                    printed_filename = filename.split('/')
                    printed_filename = printed_filename[-1]
                    data_aud_folder_browse.configure(text=printed_filename, foreground='green')
                    # Calucluate the number of the tracks in the folder (mp3)
                    track_list = [self.folder_path + '/' + file for file in os.listdir(self.folder_path) if
                                  file.endswith(".mp3")]  # mp3 only!
                    # Set variables
                    self.max_number_of_tracks = len(track_list)
                    self.number_of_tracks = self.max_number_of_tracks
                    # Make entry active and insert max number of tracks
                    entry_audio_tracks.configure(state='normal')
                    entry_audio_tracks.delete(-1, last=END)
                    entry_audio_tracks.insert(0, str(self.number_of_tracks))

                    # folder contain > 0 tracks
                    if self.number_of_tracks > 0:
                        num_of_tracks.configure(text=self.number_of_tracks, foreground='green')
                    # folder contain 0 tracks
                    else:
                        num_of_tracks.configure(text=self.number_of_tracks, foreground='red')
                except:
                    # do nothing
                    pass


        # Labels
        data_aud_folder_browse = Label(self, text="none", background=self.dark_grey_col, foreground='red',
                                       font=("Helvetica", 10))
        num_of_tracks = Label(self, text="none", background=self.dark_grey_col, foreground='red', font=("Helvetica", 10))

        # Button
        self.browse_button2 = HoverButton(self, width=20, activebackground=self.light_blue_col, text='Browse audio', bg=self.blue_col,
                                          foreground=self.white_text_col, relief=FLAT, font=("Helvetica", 12),
                                          command=file_dialog)
        # Positioning
        data_aud_folder_browse.place(x=533, y=130)

        num_of_tracks.place(x=564, y=160)

        self.browse_button2.place(x=20, y=210)

    # This function is responsible for 'Convert image into responsive background' checkbox
    def check_button(self):

        # On click
        def sel():
            # get selection index
            selection_cb = self.rb_bg_variable.get()
            # update preview image
            self.preview_image()
            # index 0
            if selection_cb == 0:
                label.config(text='Off')
            # index else
            else:
                label.config(text='On')


        # Label (On/Off)
        label = ttk.Label(self, text='Off', background=self.dark_grey_col, foreground='green', font=("Helvetica", 10))

        # Creating style element
        s = ttk.Style()
        s.configure('TCheckbutton',
                    background=self.blue_col,
                    foreground=self.white_text_col,
                    font=("Helvetica", 12),
                    width=42,
                    anchor=CENTER,
                    )

        # Keep variable linked with a check button
        self.rb_bg_variable = IntVar()
        check_button_obj = ttk.Checkbutton(self, text='Convert image into responsive background',
                                           variable=self.rb_bg_variable, takefocus=False, style='TCheckbutton',
                                           command=sel)
        # Positioning
        label.place(x=600, y=252)
        check_button_obj.place(x=20, y=119)

    # Effect options positioning and functionality
    def radio_button_effect(self):

        # On click
        def sel():
            # get selection index
            selection_rbe = self.rb_effect_variable.get()
            # update image
            self.preview_image()


            # index 0
            if selection_rbe == 0:
                label.config(text='Off', foreground='green')
            # index 1
            elif selection_rbe == 1:
                label.config(text='Snow', foreground='green')
            # index 2
            elif selection_rbe == 2:
                label.config(text='Sparks', foreground='green')
            # TODO: support custom effects
            # index else
            else:
                label.config(text='Custom', foreground='yellow')

        # Creating style element
        s = ttk.Style()
        s.configure('TRadiobutton',
                    background=self.blue_col,
                    foreground=self.white_text_col,
                    anchor=CENTER,
                    font=("Helvetica", 12)
                    )

        # Keep variable linked with a check button
        self.rb_effect_variable = IntVar()
        # defalut variable
        self.rb_effect_variable.set(0)

        #Radiobuttons and its postioning
        r1_rbe = ttk.Radiobutton(self, style='TRadiobutton', text="Off", variable=self.rb_effect_variable, value=0,
                             command=sel, takefocus=False, width=10)
        r1_rbe.place(x=20, y=320)

        r2_rbe = ttk.Radiobutton(self, style='TRadiobutton', text="Snow", variable=self.rb_effect_variable, value=1,
                             command=sel, takefocus=False, width=10)
        r2_rbe.place(x=150, y=320)

        r3_rbe = ttk.Radiobutton(self, style='TRadiobutton', text="Sparks", variable=self.rb_effect_variable, value=2,
                             command=sel, takefocus=False, width=10)
        r3_rbe.place(x=280, y=320)

        # Label and it's positioning
        label = ttk.Label(self, text='Off', background=self.dark_grey_col, foreground='green', font=("Helvetica", 10))
        label.place(x=497, y=191)

    # Audiobar options positioning and functionality
    def radio_button_audiobar(self):
        # On click
        def sel():
            # get selection index
            selection_rba = self.rb_audio_variable.get()
            # Update image
            self.preview_image()
            # index 0
            if selection_rba == 0:
                label.config(text='Off', foreground='green')
            # index 1
            elif selection_rba == 1:
                label.config(text='Standard(White)', foreground='green')
            # index 2
            elif selection_rba == 2:
                label.config(text='Standard(Black)', foreground='green')
            # TODO: support custom effects
            # else
            else:
                label.config(text='Custom', foreground='yellow')

         # Keep variable linked with a check button
        self.rb_audio_variable = IntVar()
        # defalut variable
        self.rb_audio_variable.set(0)

        #Radiobuttons and its postioning
        r1_rba = ttk.Radiobutton(self, style='TRadiobutton', text="Off", variable=self.rb_audio_variable, value=0,
                             command=sel, takefocus=False, width=10)
        r1_rba.place(x=20, y=400)

        r2_rba = ttk.Radiobutton(self, style='TRadiobutton', text="White", variable=self.rb_audio_variable,
                             value=1,
                             command=sel, takefocus=False, width=10)
        r2_rba.place(x=150, y=400)

        r3_rba = ttk.Radiobutton(self, style='TRadiobutton', text="Black", variable=self.rb_audio_variable,
                             value=2,
                             command=sel, takefocus=False, width=10)
        r3_rba.place(x=280, y=400)

        # Label and it's positioning
        label = ttk.Label(self, background=self.dark_grey_col, foreground='green', font=("Helvetica", 10), text="Off")
        label.place(x=518, y=221)

    #Create video button was clicked
    #Checks if user input was correct
    #If OK then launch the main.py
    #Running on another thread
    # useless variable is not working and used as a workaround in order to start the process with the button passed as an argument
    def prepare_to_launch(self, useless, button):
        end_thread_trigger = [False]
        def end_thread():
            end_thread_trigger[0] = True
            print('Exit - Start \nYou can start a new render if you want to')
            button.configure(text='Create video', command=lambda: Thread(target=self.prepare_to_launch, args=(self, button)).start())

        # Replace the Create video button with inactive Rendering.. button
        button.configure(text='Press to STOP', state=NORMAL, command=end_thread)
        # Put necessary information into the configuration wrapper
        self.configuration = [self.folder_path, self.file_path, self.rb_effect_variable.get(),
                              self.rb_audio_variable.get(), self.rb_bg_variable.get(), self.number_of_tracks,
                              self.image_width, self.image_height]
        # Pre render checks
        # Trigger
        error = False
        # If number of tracks == 0 -> error
        if self.number_of_tracks == 0:
            error = True
        # If elements in the wrapper is None ->error
        for param in self.configuration:
            if param is None:
                error = True
                break
        # if no errors
        # identify render mode (look settings.py)
        if not error:
            if self.rb_bg_variable.get() == 1:
                mode = 3
            elif self.rb_audio_variable.get() >= 1:
                mode = 2
            elif self.rb_effect_variable.get() >= 1:
                mode = 1
            else:
                mode = 0

            # Pass render mode
            if len(self.configuration) == 8:
                self.configuration.append(mode)
            else:
                self.configuration[9] = mode

            # output success
            print('All parameters were provided!')
            print(self.configuration)
            # start rendering process
            render.DataAndRender(self.configuration, end_thread_trigger)
            # when rendering completed -> reset button
            button.configure(text='Create video', command=lambda: Thread(target=self.prepare_to_launch, args=(self, button)).start())
            # show the folder with an output
            directory = os.getcwd()
            parent_directory = os.path.dirname(directory)
            os.startfile(parent_directory)
            # exit thread
            sys.exit()
        # if errors
        else:
            # output error, and reset button back to default
            button.configure(text='Create video', command=lambda: Thread(target=self.prepare_to_launch, args=(self, button)).start())
            print('Not all parameters were provided!')
            print(self.configuration)
            # exit thread
            sys.exit()

    # Launch thread process if Create video button was clicked
    def button_generate_video(self):

        button = HoverButton(self, text='Create video', background=self.blue_col, foreground=self.white_text_col, height=1, width=20,font=("Helvetica", 15), activebackground=self.light_blue_col, relief=FLAT,command=lambda: Thread(target=self.prepare_to_launch, args=(self, button)).start())

        button.place(x=461, y=450)


    # Lables and positioning
    def labels(self):
        # Configuration side
        Label(self, text='Current configuration', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 15)).place(x=480, y=20)
        Label(self, text='Image file:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=70)
        Label(self, text='Image size:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=100)
        Label(self, text='Audio folder:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=130)
        Label(self, text='Number of tracks:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=160)
        Label(self, text='Effect:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=190)
        Label(self, text='Audio-bar:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=220)
        Label(self, text='Responsive background:', foreground=self.white_text_col, background=self.dark_grey_col,
              font=("Helvetica", 10)).place(x=455, y=250)
        # Left side titles
        Label(self, text='Select image:', foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 15)).place(x=20, y=30)
        Label(self, text="Select effect style:", foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 15)).place(x=20, y=280)
        Label(self, text="Select audio-bar:", foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 15)).place(x=20, y=360)
        Label(self, text="Select audio folder:", foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 15)).place(x=20, y=170)
        # Image size
        Label(self, text='Image size:', foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 12)).place(x=220, y=75)
        Label(self, text='x', foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 12)).place(x=350, y=75)
        # Number of tracks
        Label(self, text='Number of tracks:', foreground=self.white_text_col, background=self.background_col,
              font=("Helvetica", 12)).place(x=220, y=215)

    # preview image functionality
    def preview_image(self):

        # Background
        image_background = None

        # Audio-bar
        # Preset samples
        image_audiobar_tuple = '../Preview/Audiobar/Standard(White).png', '../Preview/Audiobar/Standard(Black).png'
        image_audiobar = None

        # Effects
        # Preset samples
        image_effect_tuple = '../Preview/Effects/Snow_effect.png', '../Preview/Effects/Sparks_effect.png'
        image_effect = None

        # Responsive
        # Preset samples
        image_responsive_obj = '../Preview/Responsive.png'
        image_responsive = None

        # If image browsed
        if self.image_width and self.image_height and self.file_path:

            # Image aspect ratio
            aspect_ratio = float(self.image_width) / self.image_height

            # Load image background
            image_background = Image.open(str(self.file_path))

            # Load checked effect
            if int(self.rb_effect_variable.get()) > 0:
                image_effect = Image.open(image_effect_tuple[self.rb_effect_variable.get() - 1])

            # Load browsed image
            if int(self.rb_audio_variable.get()) > 0:
                image_audiobar = Image.open(image_audiobar_tuple[self.rb_audio_variable.get() - 1])

            # Load responsive image
            if (int(self.rb_bg_variable.get())) > 0:
                image_responsive = Image.open(image_responsive_obj)

            # Resize and merge available sources

            # Limitations
            size = 245, 150
            # Scale landscape
            if self.image_width / 245 > self.image_height / 150:

                height = int(math.ceil(size[0] / aspect_ratio))
                image_background_cropped = image_background.resize((size[0], height), Image.ANTIALIAS)
                image_result = image_background_cropped
                # Resize and overlay if exist
                if image_effect:
                    image_effect_cropped = image_effect.resize((size[0], height), Image.ANTIALIAS)
                    image_result.paste(image_effect_cropped, (0, 0), image_effect_cropped)
                if image_audiobar:
                    image_audiobar_cropped = image_audiobar.resize((size[0], 40), Image.ANTIALIAS)
                    image_result.paste(image_audiobar_cropped, (0, height - 40), image_audiobar_cropped)
                if image_responsive:
                    image_responsive_cropped = image_responsive.resize((size[0], height), Image.ANTIALIAS)
                    image_result.paste(image_responsive_cropped, (0, 0), image_responsive_cropped)


            # Scale portrait
            else:
                width = int(math.ceil(size[1] * aspect_ratio))
                image_background_cropped = image_background.resize((width, size[1]), Image.ANTIALIAS)
                image_result = image_background_cropped
                # Resize and overlay if exist
                if image_effect:
                    image_effect_cropped = image_effect.resize((width, size[1]), Image.ANTIALIAS)
                    image_result.paste(image_effect_cropped, (0, 0), image_effect_cropped)

                if image_audiobar:
                    image_audiobar_cropped = image_audiobar.resize((width, 40), Image.ANTIALIAS)
                    image_result.paste(image_audiobar_cropped, (0, size[1] - 40), image_audiobar_cropped)

                if image_responsive:
                    image_responsive_cropped = image_responsive.resize((width, size[1]), Image.ANTIALIAS)
                    image_result.paste(image_responsive_cropped, (0, 0), image_responsive_cropped)

            # show the preview image
            video_preview = ImageTk.PhotoImage(image_result)
            label = Label(self, image=video_preview, width=246, height=150, bg=self.dark_grey_col)
            label.image = video_preview
            label.place(x=451, y=280)

    # Redirects print statemesnt into the program's console
    #https://stackoverflow.com/questions/53721337/how-to-get-python-console-logs-on-my-tkinter-window-instead-of-a-cmd-window-whil James Kent answer
    def console(self):
        t = Text(height=3, width=54, state=DISABLED, bg=self.background_col, fg=self.grey_text_col)
        t.place(x=7, y=442)
        # create instance of file like object
        pl = PrintLogger(t)

        # replace sys.stdout with our object
        sys.stdout = pl
        # self.after(1000, do_something)


class PrintLogger:  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.config(state=NORMAL)
        self.textbox.see(END)
        self.textbox.insert(END, text)  # write text to textbox
        self.textbox.config(state=DISABLED)
        # could also scroll to end of textbox here to make sure always visible

    def flush(self):  # needed for file like object
        pass

# GUI initialization and flow
def main():
    interface = Videomusic()
    interface.console()
    interface.labels()
    interface.radio_button_effect()
    interface.radio_button_audiobar()
    interface.browse_audio()
    interface.browse_image()
    interface.check_button()
    interface.button_generate_video()
    interface.preview_image()
    interface.mainloop()


if __name__ == '__main__':
    main()
