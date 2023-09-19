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

import random

VERSION = "v0.1"

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


def main():
    """Welcome user and enter the main program loop."""
    Welcome()

    mode = NEW_GAME

    while mode != QUIT:

        if mode == NEW_GAME:
            story_type = getStoryType()
            word_list = getWordList(story_type)

        story = generateStory(story_type, word_list)
        printStory(story)

        mode = getNextMode()


def Welcome():
    """Display the title splash, and explain the program to the user."""
    print("Story Circus", VERSION)
    print()
    print("This is a silly story generator.")
    print("Enjoy fun stories with randomized elements!")


def getStoryType():
    """Allow user to select the story layout."""
    print()
    print("Choose the story you would like to hear.")
    return pickFromList(TEMP_STORY_STYLES)


def getWordList(story_type):
    """Allow user to select the word list for the chosen story layout."""
    print()
    print("Choose the word list you would like me to use.")
    return pickFromList(TEMP_WORD_LISTS)


def getNextMode():
    """Ask the user what to do after the story has finished."""
    print()
    print("What would you like to do now?")
    opts = (REPLAY, NEW_GAME, QUIT)
    return pickFromList(opts)


def pickFromList(options):
    """Allow user to select an option from a list.

    All options are numbered. The user must enter the number for their choice.

    Arguments:
        options -- list or tuple containing the options
    """

    # Print out the options.
    i = 0
    for i in range(0, len(options)):
        print("%2i. %s" %(i + 1, options[i]))

    # Wait until user enters the number for a valid option.
    choice = 0
    while choice < 1 or choice > len(options):
        text = input("Enter the number for your option: ")
        if text.isdigit():
            choice = int(text)

    return options[choice - 1]


def generateStory(story_type, word_list):
    return "The quick red fox jumps over the lazy brown dog."


def printStory(story):
    print()
    print(story)


if __name__ == "__main__":
    main()
