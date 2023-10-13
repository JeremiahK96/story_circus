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

__version__ = "v1.1"
__author__ = "Jeremiah Knol"


class StoryRecipe:
    """Data and functions needed for a story blueprint."""

    def __init__(self, filename):
        """Read story data from file. Format and store it."""
        self.name = ""      # name of the story shown in menu
        self.labels = {}    # key=label, value=list of sublabels for label
        self.recipe = []    # RecipeText and RecipeLabel objects, in order
        self.safe_wordlists = []    # IDs of compatible wordlists

        file = open(filename, 'r')
        self.name = file.readline().strip()
        story = file.read().strip()
        file.close()

        self.__splitRecipe(story)

    def __splitRecipe(self, story):
        """Split story into RecipeText and RecipeLabel objects.

        Each object is appended to self.recipe.
        Each label creates a key in self.labels."""
        start = 0   # The position we are looking at within the story.
        while True:
            label_begin = story.find('{', start)

            # If there are no more labels, the rest is plaintext. Add to story.
            if label_begin < 0:
                self.recipe.append(story[start:])
                break

            # If this is not a label, get the plaintext before the label.
            if label_begin != start:
                self.recipe.append(story[start:label_begin])
                start = label_begin
                continue

            # Otherwise, we know that this is a label.
            label_end = story.find('}', label_begin + 1)
            full_label = story[label_begin:label_end + 1]

            # Add the label to the story recipe.
            label = RecipeLabel(full_label)
            self.recipe.append(label)

            # Save label and sublabel so we can check wordlist compatibility.
            lab = label.label
            sub = label.sublabel
            if lab not in self.labels.keys():
                self.labels[lab] = []
            if sub and sub not in self.labels[lab]:
                self.labels[lab].append(sub)

            start = label_end + 1

    def checkWordListCompatibility(self, wordlists):
        """Find compatible wordlists for this recipe, mark them."""
        self.safe_wordlists = []

        # Use i to loop so we keep track of the index of the wordlist.
        for i in range(len(wordlists)):

            for label in self.labels:

                if label not in wordlists[i].labels.keys():
                    break

                for sublabel in self.labels[label]:
                    if sublabel not in wordlists[i].labels[label]:
                        break

                # If no break, continue, otherwise break again.
                else:
                    continue
                break

            # If no breaks, this wordlist is compatible.
            else:
                self.safe_wordlists.append(i)


class RecipeLabel:
    """Label section of a StoryRecipe.recipe list.

        Examples of valid label content:
            "{LabelName}"
            "{Person:1}"
            "{Animal:3/Sound}"
        """

    def __init__(self, content):
        self.content = content
        self.id = ""
        self.sublabel = ""

        # Get the label, which comes before ':'.
        tmp = self.content[1:-1].split(':')
        self.label = tmp.pop(0)

        # If there is a suffix, get id, which comes before '/'.
        if tmp:
            tmp = tmp[0].split('/')
            self.id = tmp.pop(0)

            # If there is a sublabel after '/', get it.
            if tmp:
                self.sublabel = tmp[0]


class WordList:
    """Data and functions needed for a wordlist."""

    def __init__(self, filename):
        """Read wordlist data from file. Format and store it."""
        self.name = None    # name of the wordlist shown in the menu
        self.labels = {}    # key=label, value=list of sublabels
        self.words = {}     # key=label, value=list of random word options

        # Open file, read data, and save it into this object.
        file = open(filename, 'r')
        self.name = file.readline().strip()
        self.__readWords(file)
        file.close()

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
                labels = line.split('/')
                label = labels.pop(0)
                self.labels[label] = labels
                self.words[label] = []

            # Otherwise, this line is a word option for the label.
            else:
                self.words[label].append(line)

            line = file.readline()


class RandomLabel:
    """Randomized label data and functions for this label's expansion."""

    def __init__(self, label, words):
        self.label = label
        self.words = words  # list of label/sublabel word option combos
        self.ids = {}       # memory ids for this label, popped from pool
        self.pool = self.words.copy()   # remaining word options for ids

    def byID(self, id):
        """Expands this label by id.

        If the id does not exist, pop an option from the pool and create it.
        """
        if id not in self.ids.keys():
            i = random.randrange(len(self.pool))
            self.ids[id] = self.pool.pop(i)

        return self.ids[id]


class RandomLabelDict:
    """Dictionary of RandomLabel objects, with function to expand them."""

    def __init__(self, recipe, wordlist):
        self.random_labels = {}
        for label in recipe.labels:
            new_label = RandomLabel(label, wordlist.words[label])
            self.random_labels[label] = new_label

    def expandLabel(self, full_label):
        """Expand a label in this list, handling any extra features."""

        # Find the label and suffix.
        label_end = full_label.find(':')
        label = full_label[1:label_end]
        id = full_label[label_end + 1:-1]

        # Find the RandomLabel which matches this label.
        rand_label = self.random_labels[label]

        # Handle the simple case. Just the label, no suffix.
        if label_end == -1:
            return random.choice(rand_label.words)

        # Handle cases where the suffix is an id for the label.
        return rand_label.byID(id)


class Story:
    """Single-use story object. Create, generate, display, and discard."""

    def __init__(self, recipe, wordlist):
        self.story = None
        self.recipe = recipe.recipe
        self.labels = RandomLabelDict(recipe, wordlist)

    def generate(self):
        """Generate the story, expanding all random labels."""
        self.story = ""

        for section in self.recipe:
            if type(section) is str:
                self.story += section
            else:
                self.story += self.labels.expandLabel(section.content)

    def display(self):
        """Print the generated story."""
        clearScreen()
        print(self.story)


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
    waitForEnter()

    recipes = loadStoryRecipes()
    wordlists = loadWordLists()
    checkStoryCompatibilities(recipes, wordlists)

    mode = NEW_GAME
    while mode != QUIT:

        if mode == NEW_GAME:
            recipe = pickStoryRecipe(recipes)
            wordlist = pickWordList(wordlists, recipe)

        story = Story(recipe, wordlist)
        story.generate()
        story.display()
        waitForEnter()

        mode = getNextMode()


def Welcome():
    """Display the title splash, and explain the program to the user."""
    print("Story Circus", __version__, "by", __author__)
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
    clearScreen()
    print("Choose the story you would like to hear.")
    names = map(lambda r: r.name, recipes)
    return recipes[pickFromList(names)]


def pickWordList(wordlists, recipe):
    """Allow user to select the word list for the chosen story layout."""
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


def waitForEnter():
    """Wait until User presses the Enter key."""
    print()
    input("Press enter to continue...")


def clearScreen():
    """Clear the terminal output."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":
    main()
