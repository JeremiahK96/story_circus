###############################################################################
# Story Circus
# by Jeremiah Knol
#
# Final Project for:
#    SDEV140-12K-LB-202320-LA-81X
#    Intro. to Software Development
#    Ivy Tech Community College
#
# This is a silly random story generator.
# The story blueprints and random word lists are loaded from files.
# Users can select the story and word list they would like to generate.
###############################################################################

import os
import random

# Add files for story types and word lists, and read from them.
VERSION = "v0.2"


class StoryRecipe:
    """Data and functions needed for a story blueprint."""

    name = None     # name of the story shown in menu
    labels = []     # list of labels required for this story
    recipe = []     # list of strings and labels to display in order

    def __init__(self, filename):
        """Read story data from file. Format and store it."""
        file = open(filename, 'r')
        self.name = file.readline().strip()
        self.labels = self.__readLabels(file).split()
        story = file.read().strip()
        file.close()
        self.__splitRecipe(story)

    def __readLabels(self, file):
        """Read the next non-blank line."""
        while True:
            x = file.readline().strip()
            if x:
                return x

    def __splitRecipe(self, story):
        """Split story into plaintext and labels. Append to self.recipe."""
        start = 0
        while True:
            label_start = story.find('{', start)

            # If there are no more labels...
            if label_start < 0:
                self.recipe.append(story[start:])
                return

            label_end = story.find('}', label_start + 1)

            # It this is a label...
            if label_start == start:
                self.recipe.append(story[label_start:label_end + 1])
                start = label_end + 1

            # Otherwise, this must be plain text...
            else:
                self.recipe.append(story[start:label_start])
                start = label_start


class WordList:
    """Data and functions needed for a wordlist."""

    name = None     # name of the wordlist shown in the menu
    labels = []     # list of labels included in this wordlist
    words = {}      # dict matching label to its list of random word options

    def __init__(self, filename):
        file = open(filename, 'r')
        self.name = file.readline().strip()
        self.__readWords(file)
        file.close()

    def __readLabels(self, file):
        """Read the next non-blank line."""
        while True:
            x = file.readline().strip()
            if x:
                return x

    def __readWords(self, file):
        """Read each label and its random word options."""
        label = None
        line = file.readline()
        while line:
            line = line.strip()

            # If line is blank, the next non-blank line is a label.
            if line == "":
                label = None

            # If previous line was blank, this one is a label.
            elif label == None:
                label = line
                if label not in self.labels:
                    self.labels.append(label)
                    self.words[label] = []

            # Otherwise, this line is a word option for the label.
            else:
                self.words[label].append(line)

            line = file.readline()


# Game modes.
# The values are displayed to and selected by the user after each story.
NEW_GAME = "Pick a new story"
REPLAY   = "Listen to the same story again"
QUIT     = "That's all for now"

# Placeholders. These should actually be read from files...
TEMP_STORY_STYLES = (
        "Animal Play",
        "Fun at the Party",
        "Rhyme Time"
        )
TEMP_WORD_LISTS = (
        "Animal Play",
        "Fun at the Party",
        "Rhyme Time"
        )

STORY_DIR = "data/"
WORDS_DIR = "data/"


def main():
    """Welcome user and enter the main program loop."""
    Welcome()

    recipes = loadStoryRecipes()
    wordlists = loadWordLists()

    mode = NEW_GAME
    while mode != QUIT:

        if mode == NEW_GAME:
            recipe = pickStoryRecipe(recipes)
            wordlist = pickWordList(wordlists, recipe)

        story = generateStory(recipe, wordlist)
        printStory(story)

        mode = getNextMode()


def Welcome():
    """Display the title splash, and explain the program to the user."""
    print("Story Circus", VERSION)
    print()
    print("This is a silly story generator.")
    print("Enjoy fun stories with randomized elements!")


def loadStoryRecipes():
    """Load data from all .story files into a list. Return the list."""
    recipes = []

    for file in os.listdir(STORY_DIR):
        if len(file) > 5 and file[-6:] == ".story":
            recipes.append(StoryRecipe(STORY_DIR + file))

    return recipes


def loadWordLists():
    """Load data from all .words files into a list. Return the list."""
    wordlists = []

    for file in os.listdir(WORDS_DIR):
        if len(file) > 5 and file[-6:] == ".words":
            wordlists.append(WordList(WORDS_DIR + file))

    return wordlists


def pickStoryRecipe(recipes):
    """Allow user to select the story layout."""
    print()
    print("Choose the story you would like to hear.")
    names = map(lambda r: r.name, recipes)
    return recipes[pickFromList(names)]


def pickWordList(wordlists, story_type):
    """Allow user to select the word list for the chosen story layout."""
    print()
    print("Choose the word list you would like me to use.")
    names = map(lambda r: r.name, wordlists)
    return wordlists[pickFromList(names)]


def getNextMode():
    """Ask the user what to do after the story has finished."""
    print()
    print("What would you like to do now?")
    opts = (REPLAY, NEW_GAME, QUIT)
    return opts[pickFromList(opts)]


def pickFromList(options):
    """Allow user to select an option from a list.

    All options are numbered. The user must enter the number for their choice.
    If there is only 1 option, it is chosen automatically.

    Arguments:
        options -- iterable containing the options

    Returns:
        the chosen number minus one, as an int
    """

    # Print out the options.
    i = 0
    for opt in options:
        i += 1
        print("%2i. %s" %(i, opt))

    # If there is only 1 option, return it.
    if i == 1:
        print("Choosing option 1 automatically...")
        return 0

    # Wait until user enters the number for a valid option.
    choice = 0
    while choice < 1 or choice > i:
        text = input("Enter the number for your option: ")
        if text.isdigit():
            choice = int(text)

    return choice - 1


def generateStory(story_type, word_list):
    return "The quick red fox jumps over the lazy brown dog."


def printStory(story):
    print()
    print(story)


if __name__ == "__main__":
    main()
