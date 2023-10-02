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

    def __init__(self, filename):
        """Read story data from file. Format and store it."""
        self.name = None     # name of the story shown in menu
        self.labels = []     # list of labels required for this story
        self.recipe = []     # list of strings and labels to display in order

        # list of IDs of compatible wordlists
        self.safe_wordlists = []

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
            label_begin = story.find('{', start)

            # If there are no more labels...
            if label_begin < 0:
                self.recipe.append(story[start:])
                return

            label_end = story.find('}', label_begin + 1)

            # It this is a label...
            if label_begin == start:
                self.recipe.append(story[label_begin:label_end + 1])
                start = label_end + 1

            # Otherwise, this must be plain text...
            else:
                self.recipe.append(story[start:label_begin])
                start = label_begin

    def checkWordListCompatibility(self, wordlists):
        """Find compatible wordlists for this recipe, mark them."""
        for i in range(len(wordlists)):
            for label in wordlists[i].labels:
                if label not in self.labels:
                    break
            else:
                self.safe_wordlists.append(i)


class WordList:
    """Data and functions needed for a wordlist."""

    def __init__(self, filename):
        """Read wordlist data from file. Format and store it."""
        self.name = None      # name of the wordlist shown in the menu
        self.labels = []      # list of labels included in this wordlist
        self.words = {}       # dict matching label to its list of random words

        # Open file, read data, and save it into this object.
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

# Data file directories for story recipes and word lists.
STORY_DIR = "data/"
WORDS_DIR = "data/"


def main():
    """Welcome user and enter the main program loop."""
    Welcome()

    recipes = loadStoryRecipes()
    wordlists = loadWordLists()
    checkStoryCompatibilities(recipes, wordlists)

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

    for file in sorted(os.listdir(STORY_DIR)):
        if len(file) >= 6 and file[-6:] == ".story":
            recipes.append(StoryRecipe(STORY_DIR + file))

    return recipes


def loadWordLists():
    """Load data from all .words files into a list. Return the list."""
    wordlists = []

    for file in sorted(os.listdir(WORDS_DIR)):
        if len(file) >= 6 and file[-6:] == ".words":
            wordlists.append(WordList(WORDS_DIR + file))

    return wordlists


def checkStoryCompatibilities(recipes, wordlists):
    """Check label compatibility between recipes and wordlists."""
    for recipe in recipes:
        recipe.checkWordListCompatibility(wordlists)


def pickStoryRecipe(recipes):
    """Allow user to select the story layout."""
    print()
    print("Choose the story you would like to hear.")
    names = map(lambda r: r.name, recipes)
    return recipes[pickFromList(names)]


def pickWordList(wordlists, recipe):
    """Allow user to select the word list for the chosen story layout."""
    print()
    print("Choose the word list you would like me to use.")
    ids = []
    names = []
    for i in recipe.safe_wordlists:
        ids.append(i)
        names.append(wordlists[i].name)
    choice = pickFromList(names)
    return wordlists[ids[choice]]


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


def generateStory(recipe, wordlist):
    """Generate a story using a recipe and wordlist."""
    story = ""

    for section in recipe.recipe:
        story += expandRandomWord(section, wordlist)

    return story


def expandRandomWord(section, wordlist):
    """Expand random word in section.

    If section is not a label, just return it as it is.
    Otherwise, return a random word for its label in wordlist.
    """
    begin = section.find('{')
    if begin == -1:
        return section
    end = section.find('}', begin + 1)

    full_label = section[begin + 1:end]
    label_end = full_label.find(':')

    # If this label has no suffix, just pick a random option.
    if label_end == -1:
        return random.choice(wordlist.words[full_label])

    label = full_label[:label_end]
    suffix = full_label[label_end + 1:]

    # Temporary: Desctuctively pop an option so it won't be picked again.
    i = random.randrange(0, len(wordlist.words[label]))
    return wordlist.words[label].pop(i)


def printStory(story):
    print()
    print(story)


if __name__ == "__main__":
    main()
