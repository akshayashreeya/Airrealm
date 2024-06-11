import subprocess
from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainApplication(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)

        # Set the title of the window
        self.title("Air Realm")

        # Set the window size
        self.geometry("900x600")

        self.resizable(False, False)
        
        # Container to hold all pages
        self.container = CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold references to all pages
        self.pages = {}
        
        # Create pages
        self.create_pages()
        
        # Show Page 1 by default
        self.show_page("Page 1")
        
    def create_pages(self):
        """Create all pages and add them to the dictionary."""
        # Create page 1
        page1 = Page(self.container, "Page 1", self, self.page1_start_button_clicked)
        self.pages["Page 1"] = page1
        page1.grid(row=0, column=0, sticky="nsew")
        
        # Create page 2
        page2 = Page(self.container, "Page 2", self, self.page2_start_button_clicked)
        self.pages["Page 2"] = page2
        page2.grid(row=0, column=0, sticky="nsew")
        
        # Create page 3
        page3 = Page(self.container, "Page 3", self, self.page3_start_button_clicked)
        self.pages["Page 3"] = page3
        page3.grid(row=0, column=0, sticky="nsew")
        
        # Create page 4
        page4 = Page(self.container, "Page 4", self, self.page4_start_button_clicked)
        self.pages["Page 4"] = page4
        page4.grid(row=0, column=0, sticky="nsew")
        
        # Create page 5
        page5 = Page(self.container, "Page 5", self, self.page5_start_button_clicked)
        self.pages["Page 5"] = page5
        page5.grid(row=0, column=0, sticky="nsew")
        
    def show_page(self, page_name):
        """Show the page corresponding to the given page name."""
        page = self.pages.get(page_name)
        if page:
            page.tkraise()

    # Define separate methods for each page's start button click event
    def page1_start_button_clicked(self):
        print("Start/End button clicked on Page 1")
        hand_tracking_path = resource_path("HandTracking.py")
        if hasattr(self, 'hand_tracking_process') and self.hand_tracking_process is not None:
            self.hand_tracking_process.terminate()
            self.hand_tracking_process = None
            self.pages["Page 1"].toggle_button_text()
        else:
            if os.path.exists(hand_tracking_path):
                self.hand_tracking_process = subprocess.Popen(["python", hand_tracking_path])
                self.pages["Page 1"].toggle_button_text()
            else:
                print(f"Error: {hand_tracking_path} does not exist.")

    def page2_start_button_clicked(self):
        print("Start/End button clicked on Page 2")
        mouse_path = resource_path("mouse.py")
        if hasattr(self, 'mouse_process') and self.mouse_process is not None:
            self.mouse_process.terminate()
            self.mouse_process = None
            self.pages["Page 2"].toggle_button_text()
        else:
            if os.path.exists(mouse_path):
                self.mouse_process = subprocess.Popen(["python", mouse_path])
                self.pages["Page 2"].toggle_button_text()
            else:
                print(f"Error: {mouse_path} does not exist.")

    def page3_start_button_clicked(self):
        print("Start/End button clicked on Page 3")
        presentation_path = resource_path("presentation.py")
        if hasattr(self, 'presentation_process') and self.presentation_process is not None:
            self.presentation_process.terminate()
            self.presentation_process = None
            self.pages["Page 3"].toggle_button_text()
        else:
            if os.path.exists(presentation_path):
                self.presentation_process = subprocess.Popen(["python", presentation_path])
                self.pages["Page 3"].toggle_button_text()
            else:
                print(f"Error: {presentation_path} does not exist.")

    def page4_start_button_clicked(self):
        print("Start button clicked on Page 4")
        movie_path = resource_path("movie2.py")
        if hasattr(self, 'movie_process') and self.movie_process is not None:
            self.movie_process.terminate()
            self.movie_process = None
            self.pages["Page 4"].toggle_button_text()
        else:
            if os.path.exists(movie_path):
                self.movie_process = subprocess.Popen(["python", movie_path])
                self.pages["Page 4"].toggle_button_text()
            else:
                print(f"Error: {movie_path} does not exist.")

    def page5_start_button_clicked(self):
        print("Start button clicked on Page 5")
        game_path = resource_path("game.py")
        if hasattr(self, 'game_process') and self.game_process is not None:
            self.game_process.terminate()
            self.game_process = None
            self.pages["Page 5"].toggle_button_text()
        else:
            if os.path.exists(game_path):
                self.game_process = subprocess.Popen(["python", game_path])
                self.pages["Page 5"].toggle_button_text()
            else:
                print(f"Error: {game_path} does not exist.")

class Page(CTkFrame):
    def __init__(self, parent, page_name, controller, start_button_command):
        CTkFrame.__init__(self, parent)
        self.page_name = page_name
        self.controller = controller
        self.is_started = False

        # Label to display the page name
        label = CTkLabel(self, text=page_name)
        label.pack(side="bottom", pady=10)
        
        # Create a frame for the buttons
        button_frame = CTkFrame(self)
        button_frame.pack(pady=10)  # Add padding to separate from label

        # Create buttons on each page individually
        button_texts = ["Hand test", "Mouse", "Presentation", "Movie", "Game"]
        for button_num in range(5):
            button = CTkButton(button_frame, text=button_texts[button_num], command=lambda num=button_num+1: self.button_clicked(num))
            button.pack(side="left", padx=5, pady=5)
            button.configure(width=150, height=30)
            button.grid_propagate(False)

        if page_name == "Page 1":
            # Create a frame for the text
            text_frame = CTkFrame(self)
            text_frame.pack(pady=100, padx=50)

            # Add text specific to Page 1
            text = "Our revolutionary application represents the pinnacle of innovation, integrating state-of-the-art\ndeep learning algorithms to seamlessly translate dynamic hand gestures into precise computer\ncommands. Through the sophisticated utilization of OpenCV and MediaPipe libraries, our\nsolution delivers an unparalleled user experience, transcending the limitations of traditional\ninput methods. By empowering users to interact with computers intuitively, we redefine the very\nessence of human-computer interaction, setting new standards for efficiency and convenience.\n\nWith a simple click of the start button, users embark on a journey of exploration, evaluating\ncamera compatibility for flawless hand detection. This functionality not only enhances productivity\nbut also fosters a deeper connection between users and technology. Our system embodies\nunprecedented convenience, revolutionizing the way individuals engage with digital environments."


            label = CTkLabel(text_frame, text=text, justify="left", font=("Helvetica", 15))
            label.pack(padx=20, pady=20)

        if page_name == "Page 2":
            # Create a frame for the text
            text_frame = CTkFrame(self)
            text_frame.pack(pady=100, padx=50)

            # Add text specific to Page 1
            text = "A sophisticated feature designed to revolutionize mouse interactions with unparalleled precision\nand ease. Utilizing just two fingers—the index and middle—users can effortlessly navigate their\ndigital environment. By opening both fingers, cursor movement becomes fluid and intuitive,\nenabling seamless navigation across the screen. Executing various actions is equally\nstraightforward: a double-click is initiated by joining the fingers, spreading them apart triggers\na left-click, and closing them executes a click-and-hold. Need to select files or text? Simply close\nthe fingers slightly and move them up and down for precise selection.For right-click functionality,\ngently close the middle finger while using GestureControl. This innovative tool isn't just about\nconvenience; it's about enhancing professionalism and productivity. Its seamless integration into\nworkflows ensures that every interaction feels natural and refined, empowering users to accomplish\n tasks with unparalleled efficiency. Experience the future of mouse control with GestureControl\nwhere simplicity meets sophistication, and productivity reaches new heights."
            label = CTkLabel(text_frame, text=text, justify="left", font=("Helvetica", 15))
            label.pack(padx=20, pady=20)
        if page_name == "Page 3":
            # Create a frame for the text
            text_frame = CTkFrame(self)
            text_frame.pack(pady=100, padx=50)

            # Add text specific to Page 1
            text = "Immerse yourself in a world where your movements drive the narrative. Swipe left to transition\nto the next slide, swipe right to go back, and gesture up or down to zoom in or out. With\nPresentation.py, every movement becomes a gesture of expression, amplifying your message\nand captivating your audience's attention.\n\nExperience the power of natural interaction as Presentation.py tracks your hand movements\nin real-time, translating them into seamless commands. Whether you're delivering a keynote\naddress, leading a workshop, or pitching your latest project, Presentation.py empowers you to\ncommand the stage with confidence and precision."
            label = CTkLabel(text_frame, text=text, justify="left", font=("Helvetica", 15))
            label.pack(padx=20, pady=20)
        if page_name == "Page 4":
            # Create a frame for the text
            text_frame = CTkFrame(self)
            text_frame.pack(pady=100, padx=50)

            # Add text specific to Page 1
            text = "Navigate through your favorite movies and videos with effortless precision. Simply swipe right\nto skip forward by 1 minute, or swipe left to rewind by 1 minute. With Movie.py, controlling\nplayback has never been easier or more intuitive.\n\nAdjust the volume seamlessly with just a flick of your wrist. Swipe up and hold to increase the\nvolume, and swipe down and hold to decrease it. Experience the perfect balance of sound with\nintuitive gesture control.\n\nPause and play your media with a simple gesture. Just raise your index finger to pause, and lower\nit to resume playback."
            label = CTkLabel(text_frame, text=text, justify="left", font=("Helvetica", 15))
            label.pack(padx=20, pady=20)

        if page_name == "Page 5":
            # Create a frame for the text
            text_frame = CTkFrame(self)
            text_frame.pack(pady=100, padx=50)

            # Add text specific to Page 1
            text = "Engage in seamless movement through your virtual worlds with intuitive hand gestures. Lead\nthe way by extending your index finger forward to move your character forward, bringing your\ngaming experience to life with natural movements.\n\nNavigate complex terrain effortlessly with precise control. Combine your index and middle\nfingers to move left, and utilize the power of three—index, middle, and ring fingers—to\nnavigate right. With Game.py, traversing virtual landscapes becomes second nature.\n\nBacktrack through your adventures with ease by extending all four fingers—index, middle, ring,\nand little fingers—to move backward. Whether you're exploring vast landscapes or engaging in\nepic battles, Game.py puts you in control like never before."
            label = CTkLabel(text_frame, text=text, justify="left", font=("Helvetica", 15))
            label.pack(padx=20, pady=20)


        # Create start/end button
        self.start_end_button = CTkButton(self, text="Start", command=start_button_command)
        self.start_end_button.pack(side="bottom", padx=5, pady=5, anchor="center")

    def button_clicked(self, button_num):
        """Function to be called when a button is clicked."""
        self.controller.show_page(f"Page {button_num}")

    def toggle_button_text(self):
        """Toggle the text of the start/end button."""
        self.is_started = not self.is_started
        if self.is_started:
            self.start_end_button.configure(text="End")
        else:
            self.start_end_button.configure(text="Start")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
"""
Displays a text frame with specific content for Page 3 of the application.

The text frame is created using a CTkFrame widget and the text is displayed using a CTkLabel widget. The text is justified to the left and uses the "Helvetica" font with a size of 15.
"""
