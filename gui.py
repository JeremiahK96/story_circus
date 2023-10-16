"""Graphical User Interface for program using Tkinter"""

import story_circus as sc
import tkinter as tk


TITLE_FONT = ("Arial 30 bold")
TEXT_FONT = ("Arial 20")


class Root:

    def __init__(self):

        self.w = tk.Tk()

        self.w.title("Story Circus " + sc.__version__)
        self.w.attributes('-type', 'dialog')

        self.label = tk.Label(
            self.w,
            font = TITLE_FONT
        )
        self.label.pack()

        self.w.after(1, self.main())

        self.w.mainloop()

    def main(self):
        self.welcome()

    def welcome(self):
        self.label.config(
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
            command = self.start
        )
        self.start.pack()

    def start(self):
        self.splash.destroy()
        self.start.destroy()


def oldmain():
    sc.Welcome()
    sc.waitForEnter()

    recipes = sc.loadStoryRecipes()
    wordlists = sc.loadWordLists()
    sc.checkStoryCompatibilities(recipes, wordlists)

    mode = sc.NEW_GAME
    while mode != sc.QUIT:

        if mode == sc.NEW_GAME:
            recipe = sc.pickStoryRecipe(recipes)
            wordlist = sc.pickWordList(wordlists, recipe)

        story = sc.Story(recipe, wordlist)
        story.generate()
        story.display()
        sc.waitForEnter()

        mode = sc.getNextMode()


if __name__ == "__main__":
    Root()
