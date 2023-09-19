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
    Welcome()

    mode = "NEW_GAME"

    while mode != "QUIT":

        if mode == "NEW_GAME":
            story_type = getStoryType()
            word_list = getWordList(story_type)

        story = generateStory(story_type, word_list)
        printStory(story)

        mode = getNextMode()


def Welcome():
    print("Story Circus", VERSION)
    print()
    print("This is a silly story generator.")
    print("Enjoy fun stories with randomized elements!")


def getStoryType():
    print()
    print("Choose the story you would like to hear.")
    return pickFromList(TEMP_STORY_STYLES)


def getWordList(story_type):
    print()
    print("Choose the word list you would like me to use.")
    return pickFromList(TEMP_WORD_LISTS)


def pickFromList(options):
    i = 0
    for i in range(0, len(options)):
        print("%2i. %s" %(i + 1, options[i]))

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


def getNextMode():
    return "QUIT"


if __name__ == "__main__":
    main()
