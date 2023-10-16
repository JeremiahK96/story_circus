"""Graphical User Interface for program using Tkinter"""

import os
import story_circus as sc
import tkinter as tk
import tkinter.scrolledtext as st


TITLE_FONT = ("Arial 30 bold")
TITLE_PAD = "20px"

TEXT_FONT = ("Arial 20")

BUTTON_BG = "#dfdfdf"
BUTTON_FG = "#202020"
BUTTON_ALT = "#404040"
BUTTON_PAD = "5px"


class Root:

    def __init__(self):

        self.w = tk.Tk()
        self.w.title("Story Circus " + sc.__version__)

        if os.name != 'nt':
            self.w.attributes('-type', 'dialog')

        self.w.after(1, self.main())

        self.w.mainloop()

    def main(self):
        self.title = tk.Label(
            self.w,
            font = TITLE_FONT
        )
        self.title.pack(padx = TITLE_PAD, pady = TITLE_PAD)

        self.welcome()

        self.recipes = sc.loadStoryRecipes()
        self.wordlists = sc.loadWordLists()
        sc.checkStoryCompatibilities(self.recipes, self.wordlists)

    def welcome(self):
        self.title.config(
            text = "Story Circus " + sc.__version__ + " by " + sc.__author__
        )

        self.splash = tk.Label(
            self.w,
            text = \
                "This is a silly story generator.\n" + \
                "Enjoy fun stories with randomized elements!",
            font = TEXT_FONT
        )
        self.splash.pack()

        self.start = tk.Button(
            self.w,
            text = "Start",
            font = TEXT_FONT,
            command = self.__start
        )
        self.start.pack(padx = TITLE_PAD, pady = TITLE_PAD)

    def __start(self):
        self.splash.destroy()
        self.start.destroy()

        self.opt_frame = tk.Frame(self.w)
        self.opt_frame.pack()
        self.opt_buttons = []

        self.nav_frame = tk.Frame(self.w)
        self.nav_frame.pack(padx = TITLE_PAD, pady = TITLE_PAD)
        self.nav_buttons = []

        self.__addNavButtons()

        self.__pickStoryRecipe()

    def __addNavButtons(self):
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
        self.title.config(text = "Select a Story")

        names = map(lambda r: r.name, self.recipes)
        self.__showOptions(names, self.__setRecipe, self.__pickWordList)
        self.nav_buttons[-2]["state"] = tk.DISABLED

    def __setRecipe(self, id):
        self.recipe = self.recipes[id]
        self.__updateOptButtons(id)

    def __pickWordList(self):
        self.title.config(text = "Select a Word List")

        safe = self.recipe.safe_wordlists
        if len(safe) == 1:
            self.wordlist = self.wordlists[safe[0]]
            self.__playStory()
        else:
            self.options = []
            for id in safe:
                self.options.append(self.wordlists[id])
            names = map(lambda w: w.name, self.options)
            self.__showOptions(names, self.__setWordList, self.__playStory)
            self.nav_buttons[-2]["state"] = tk.NORMAL

    def __setWordList(self, id):
        self.wordlist = self.options[id]
        self.__updateOptButtons(id)

    def __updateOptButtons(self, id):
        self.nav_buttons[-1]["state"] = tk.NORMAL

        if self.prev_id != None:
            self.opt_buttons[self.prev_id].configure(
                bg = BUTTON_BG,
                fg = BUTTON_FG
            )
        self.prev_id = id

        self.opt_buttons[id].configure(
            bg = BUTTON_ALT,
            fg = BUTTON_BG
        )

    def __showOptions(self, options, choice_func, next_func):
        for i in range(len(self.opt_buttons) - 1, -1, -1):
            self.opt_buttons[i].destroy()
            del self.opt_buttons[i]
        self.prev_id = None

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

        self.nav_buttons[-1].configure(
            command = next_func,
            state = tk.DISABLED
        )

    def __playStory(self):
        Story(self)
        self.__pickStoryRecipe()


class Story:

    def __init__(self, root):
        self.root = root
        self.recipe = root.recipe
        self.wordlist = root.wordlist

        self.title = self.recipe.name
        if self.title != self.wordlist.name:
            self.title += " (" + self.wordlist.name + ")"

        self.w = tk.Toplevel()
        self.w.title(self.title)

        if os.name != 'nt':
            self.w.attributes('-type', 'dialog')

        self.w.transient(root.w)
        self.w.grab_set()

        self.w.after(1, self.main())

        self.w.mainloop()

    def main(self):
        self.title = tk.Label(
            self.w,
            text = self.title,
            font = TITLE_FONT
        )
        self.title.pack()

        self.story_text = st.ScrolledText(
            self.w,
            wrap = tk.WORD,
            width = 40,
            height = 10,
            font = TEXT_FONT,
            state = tk.DISABLED
        )
        self.story_text.pack()

        frame = tk.Frame(self.w)
        frame.pack()

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
        story = sc.Story(self.recipe, self.wordlist)
        story.generate()

        self.story_text["state"] = tk.NORMAL
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.INSERT, story.story)
        self.story_text["state"] = tk.DISABLED


if __name__ == "__main__":
    Root()
