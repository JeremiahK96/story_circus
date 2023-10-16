"""Graphical User Interface for program using Tkinter"""

import os
import story_circus as sc
import tkinter as tk
import tkinter.scrolledtext as st


TITLE_FONT = ("Arial 30 bold")  # font used for all title labels
TITLE_PAD = "20px"              # padding used for titles and navigation frames

TEXT_FONT = ("Arial 20")        # font used for text and buttons

BUTTON_BG = "#dfdfdf"           # default background color for menu buttons
BUTTON_FG = "#202020"           # default foreground color for menu buttons
BUTTON_ALT = "#404040"          # highlight background color for menu buttons
BUTTON_PAD = "5px"              # padding used between grouped buttons


class Root:
    """Root window, used for splash screen and story menu."""

    def __init__(self):
        """Create the root window and launch main function."""
        self.w = tk.Tk()
        self.w.title("Story Circus " + sc.__version__)
        self.w.after(1, self.main())
        self.w.mainloop()

    def main(self):
        """Create the main label, show the splash, and process story data."""
        self.title = tk.Label(self.w, font = TITLE_FONT)
        self.title.pack(padx = TITLE_PAD, pady = TITLE_PAD)

        self.splash()

        self.recipes = sc.loadStoryRecipes()
        self.wordlists = sc.loadWordLists()
        sc.checkStoryCompatibilities(self.recipes, self.wordlists)

    def splash(self):
        """Welcome user with brief description of program."""
        self.title.config(
            text = "Story Circus " + sc.__version__ + " by " + sc.__author__
        )

        # Add temporary label for splash message.
        self.splash = tk.Label(
            self.w,
            text = \
                "This is a silly story generator.\n" + \
                "Enjoy fun stories with randomized elements!",
            font = TEXT_FONT
        )
        self.splash.pack()

        # Add temporary button to exit splash.
        self.start = tk.Button(
            self.w,
            text = "Start",
            font = TEXT_FONT,
            command = self.__start
        )
        self.start.pack(padx = TITLE_PAD, pady = TITLE_PAD)

    def __start(self):
        """Start main program, setup menu layout."""
        self.splash.destroy()
        self.start.destroy()

        # Add a frame to hold the option buttons.
        self.opt_frame = tk.Frame(self.w)
        self.opt_frame.pack()
        self.opt_buttons = []

        # Add a frame to hold the navigation buttons.
        self.nav_frame = tk.Frame(self.w)
        self.nav_frame.pack(padx = TITLE_PAD, pady = TITLE_PAD)
        self.nav_buttons = []

        self.__addNavButtons()
        self.__pickStoryRecipe()

    def __addNavButtons(self):
        """Add navigation buttons."""
        # Exit button, quits the program.
        button = tk.Button(
            self.nav_frame,
            text = "Quit",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            command = exit
        )
        button.grid(
            row = 0, column = 0,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )
        self.nav_buttons.append(button)

        # Back button, only used on Page 2.
        button = tk.Button(
            self.nav_frame,
            text = "Back",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            command = self.__pickStoryRecipe,
            state = tk.DISABLED
        )
        button.grid(
            row = 0, column = 1,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )
        self.nav_buttons.append(button)

        # Next button, disabled until a selection is made.
        button = tk.Button(
            self.nav_frame,
            text = "Next",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            state = tk.DISABLED
        )
        self.nav_buttons.append(button)
        button.grid(
            row = 0, column = 2,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )

    def __pickStoryRecipe(self):
        """Update title label, add buttons for story selection."""
        self.title.config(text = "Select a Story")

        # Get iterable object with all story names.
        names = map(lambda r: r.name, self.recipes)

        # Add buttons for setting the recipe, Next = pickWordList.
        self.__showOptions(names, self.__setRecipe, self.__pickWordList)

        # Disable the Back button on Page 1.
        self.nav_buttons[-2]["state"] = tk.DISABLED

    def __setRecipe(self, id):
        """After a button is clicked, set the recipe by its id."""
        self.recipe = self.recipes[id]
        self.__updateOptButtons(id)

    def __pickWordList(self):
        """Update title label, add buttons for wordlist selection.

        If there is only 1 option, this is skipped.
        """
        safe = self.recipe.safe_wordlists

        # If this recipe has only 1 compatible wordlist, use it.
        if len(safe) == 1:
            self.wordlist = self.wordlists[safe[0]]
            self.__playStory()

        else:
            self.title.config(text = "Select a Word List")

            # Create list of only the compatible wordlists.
            self.options = []
            for id in safe:
                self.options.append(self.wordlists[id])

            # Get iterable object with all compatible wordlist names.
            names = map(lambda w: w.name, self.options)

            # Add buttons for setting the wordlist, Next = playStory.
            self.__showOptions(names, self.__setWordList, self.__playStory)

            # Enable the Back button on Page 2.
            self.nav_buttons[-2]["state"] = tk.NORMAL

    def __setWordList(self, id):
        """After a button is clicked, set the wordlist by its id."""
        self.wordlist = self.options[id]
        self.__updateOptButtons(id)

    def __updateOptButtons(self, id):
        """After a button is clicked, invert its colors and enable Next."""
        # Allow user to click Next.
        self.nav_buttons[-1]["state"] = tk.NORMAL

        # Un-invert the previously selected button.
        if self.prev_id != None:
            self.opt_buttons[self.prev_id].configure(
                bg = BUTTON_BG,
                fg = BUTTON_FG
            )
        self.prev_id = id

        # Invert the selected button.
        self.opt_buttons[id].configure(
            bg = BUTTON_ALT,
            fg = BUTTON_BG
        )

    def __showOptions(self, options, choice_func, next_func):
        """Remove option buttons from menu, and add the new ones.

        Inputs:
            options = iterable object with option names for buttons
            choice_func = function to run for each option button
            next_func = function to run if user clicks Next
        """
        # Destroy and delete all option buttons.
        for i in range(len(self.opt_buttons) - 1, -1, -1):
            self.opt_buttons[i].destroy()
            del self.opt_buttons[i]

        # Forget previously-selected button.
        self.prev_id = None

        # Add buttons to set the recipe or wordlist.
        i = 0
        for opt in options:
            button = tk.Button(
                self.opt_frame,
                text = opt,
                font = TEXT_FONT,
                bg = BUTTON_BG,
                fg = BUTTON_FG,
                command = lambda c = i: choice_func(c)
            )
            button.pack(pady = BUTTON_PAD)
            self.opt_buttons.append(button)
            i += 1

        # Set the function for the Next button.
        self.nav_buttons[-1].configure(
            command = next_func,
            state = tk.DISABLED
        )

    def __playStory(self):
        """Play the story, and go back to Page 1."""
        Story(self)
        self.__pickStoryRecipe()


class Story:
    """Story window, used to show story."""

    def __init__(self, root):
        """Create the story window and launch its main function."""
        self.root = root
        self.recipe = root.recipe
        self.wordlist = root.wordlist

        self.title = self.recipe.name
        if self.title != self.wordlist.name:
            self.title += " (" + self.wordlist.name + ")"

        self.w = tk.Toplevel()
        self.w.title(self.title)

        # Freeze parent window until this one closes.
        self.w.transient(root.w)
        self.w.grab_set()

        self.w.after(1, self.main())
        self.w.mainloop()

    def main(self):
        """Set label, add scrolling textbox, and add navigation buttons."""
        self.title = tk.Label(
            self.w,
            text = self.title,
            font = TITLE_FONT
        )
        self.title.pack(padx = BUTTON_PAD, pady = BUTTON_PAD)

        self.story_text = st.ScrolledText(
            self.w,
            wrap = tk.WORD,
            width = 40,
            height = 10,
            font = TEXT_FONT,
            state = tk.DISABLED
        )
        self.story_text.pack()

        # Add frame to put navigation buttons in.
        frame = tk.Frame(self.w)
        frame.pack()

        # Exit button, quits the program.
        tk.Button(
            frame,
            text = "Quit",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            command = exit
        ).grid(
            row = 0, column = 0,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )

        # New Story button, closes this window and returns to root one.
        tk.Button(
            frame,
            text = "Pick New Story",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            command = self.w.destroy
        ).grid(
            row = 0, column = 1,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )

        # Repeat Story button, generates a new story with the same rules.
        tk.Button(
            frame,
            text = "Repeat Same Story",
            font = TEXT_FONT,
            bg = BUTTON_BG,
            fg = BUTTON_FG,
            command = self.__generateStory
        ).grid(
            row = 0, column = 2,
            padx = BUTTON_PAD, pady = BUTTON_PAD
        )

        self.__generateStory()

    def __generateStory(self):
        """Generate story for the chosen recipe and wordlist."""
        story = sc.Story(self.recipe, self.wordlist)
        story.generate()

        # Disable read-only mode on textbox, delete all the text.
        self.story_text["state"] = tk.NORMAL
        self.story_text.delete("1.0", tk.END)

        # Insert the story into textbox, enable read-only mode.
        self.story_text.insert(tk.INSERT, story.story)
        self.story_text["state"] = tk.DISABLED


if __name__ == "__main__":
    Root()
