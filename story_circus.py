"""
Story Circus
by Jeremiah Knol
10-15-2023

Final Project for:
    SDEV140-12K-LB-202320-LA-81X
    Intro. to Software Development
    Ivy Tech Community College

This is a silly random story generator.
The story blueprints and random word lists are loaded from files.
Users can select the story and word list they would like to generate.
"""

import os
import random

__version__ = "v2.0"
__author__ = "Jeremiah Knol"

# Data file directories for story recipes and word lists.
STORY_DIR = "data/"
WORDS_DIR = "data/"


class StoryRecipe:
    """Story blueprint.

    Public instance variables:
        name = title of story, shown in menu
        labels = dictionary of labels in this story
            - key = label
            - value = list of sublabels for label
        recipe = list of story sections, in order
            - Items of type "str" are displayed as-is.
            - Items of type "RecipeLabel" are displayed as a random choice.
        safe_wordlists = list of wordlist IDs which are compatible
    """

    def __init__(self, filename):
        """Read story data from file. Format and store it.

        The first line of the file is the title of the story.
        The rest of the file is the story itself.

        The story is split into a list of plaintext and RecipeLabel objects.
        Each object is appended to self.recipe.

        Each label creates a key in self.labels.
        Each sublabel is added to that label's list of sublabels.
        """
        self.name = ""
        self.labels = {}
        self.recipe = []
        self.safe_wordlists = []

        with open(filename, 'r') as file:
            self.name = file.readline().strip()
            story = file.read().strip()

        self.__splitRecipe(story)

    def __splitRecipe(self, story):
        start = 0   # The position we are looking at within the story.
        while True:
            label_begin = story.find('{', start)

            # If there are no more labels, the rest is plaintext. Add to story.
            if label_begin == -1:
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
        """Find compatible wordlists for this recipe; mark them by index.

        A wordlist is considered compatible if it declares each label used in
        the story, and if each label also has each sublabel used in the story.
        """
        self.safe_wordlists = []

        # Use i to loop so we keep track of the index of the wordlist.
        for i in range(len(wordlists)):
            if self.__labelsAreCompatible(wordlists[i]):
                self.safe_wordlists.append(i)

    def __labelsAreCompatible(self, wordlist):
        for label in self.labels:
            if label not in wordlist.labels.keys():
                return False
            for sublabel in self.labels[label]:
                if sublabel not in wordlist.words[label].labels:
                    return False
        return True


class RecipeLabel:
    """Label section of a StoryRecipe object's recipe list.

    Public instance variables:
        label = the label, comes before ':' if there is a suffix
        id = the id, comes after ':' and before '/' if there is a sublabel
        sublabel = the sublabel, comes after '/'

    Examples of valid label content:
        "{LabelName}"
        "{Person:1}"
        "{Animal:3/Sound}"
    """

    def __init__(self, content):
        self.id = None
        self.sublabel = None

        # Get the label, which comes before ':'.
        tmp = content[1:-1].split(':')
        self.label = tmp.pop(0)

        # If there is a suffix, get id, which comes before '/'.
        if tmp:
            tmp = tmp[0].split('/')
            self.id = tmp.pop(0)

            # If there is a sublabel after '/', get it.
            if tmp:
                self.sublabel = tmp[0]


class WordList:
    """Labels and their word options for filling in a story.

    Public instance variables:
        name = title of wordlist, shown in menu
        labels = dictionary of labels in this wordlist
            - key = label
            - value = list of sublabels for label
        words = dictionary of WordLabel objects from wordlist
    """

    def __init__(self, filename):
        """Read wordlist data from file. Format and store it.

        The first line of the file is the title of the wordlist.
        The rest of the file is the wordlist itself.

        A label is declared by placing it on its own line.
        Each label is followed by a list of word options for that label.
        These lines can be indented however you like.
        Adding a blank line closes the label so you can add another.
        """
        self.name = None
        self.labels = {}
        self.words = {}

        with open(filename, 'r') as file:
            self.name = file.readline().strip()
            self.__readWords(file)

    def __readWords(self, file):
        label = None
        line = file.readline()
        while line:
            line = line.strip()

            # If line is blank, the next non-blank line is a label.
            if line == "":
                label = None

            # If previous line was blank, this one is a label.
            elif label == None:
                label = line.split('/')
                self.labels[label[0]] = label[1:]
                self.words[label[0]] = WordLabel(label)

            # Otherwise, this line is a word option for the label.
            else:
                self.words[label[0]].addWordOption(line)

            line = file.readline()


class WordLabel:
    """Label section of a StoryRecipe object's recipe list.

    Public instance variables:
        labels = list of labels, first element is main, the rest are sublabels
        words = list of word options, as dictionaries
        ids = dictionary of remembered choices popped from pool
        pool = copy of words to pop choices from

    Examples of valid label content:
        "{LabelName}"
        "{Person:1}"
        "{Animal:3/Sound}"
    """

    def __init__(self, labels):
        self.labels = labels
        self.words = []
        self.ids = None
        self.pool = None

    def addWordOption(self, words):
        """Add a word option to the list of words.

        Inputs:
            words = words for each sublabel, in order, each separated by '/'

        A dictionary is created with each sublabel as a key, and each word
        connected to its sublabel. This dictionary is added to the word list.
        """
        opts = words.split('/')
        options = {}
        for i in range(len(self.labels)):
            options[self.labels[i]] = opts[i]
        self.words.append(options)

    def reset(self):
        """Clear the remembered words, and reset the pool for them."""
        self.ids = {}
        self.pool = self.words.copy()

    def expanded(self, id, sublabel):
        """Expand this word label, by id and sublabel.

        Returns the expanded label as a string.

        If sublabel is None, the main label will be used.
        If id is None, any random choice can be chosen.
        If id doesn't exist, it is created and given a random choice from pool.
        If id does exist, its random choice is remembered and used again.
        """
        if sublabel == None:
            sublabel = self.labels[0]
        if id == None:
            return random.choice(self.words)[sublabel]
        if id not in self.ids.keys():
            x = random.randrange(len(self.pool))
            self.ids[id] = self.pool.pop(x)
        return self.ids[id][sublabel]


class Story:
    """Single rendering of a story.

    Public instance variables:
        story = string to store the textual story in
        recipe = list of plaintext and RecipeLabel objects in display order
        labels = dictionary of WordLabel objects for filling in RecipeLabels
    """

    def __init__(self, recipe, wordlist):
        self.story = ""
        self.recipe = recipe.recipe
        self.labels = wordlist.words

        # Reset WordLabel objects for this story.
        for wordlabel in self.labels.keys():
            self.labels[wordlabel].reset()

    def generate(self):
        """Generate the story, expanding plaintext and RecipeLabel objects."""
        for section in self.recipe:
            if type(section) is str:
                self.story += section
            else:
                label = section.label
                id = section.id
                sublabel = section.sublabel
                self.story += self.labels[label].expanded(id, sublabel)


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
