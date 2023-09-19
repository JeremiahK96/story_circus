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
    return ""


def getWordList(story_type):
    return ""


def generateStory(story_type, word_list):
    return "The quick red fox jumps over the lazy brown dog."


def printStory(story):
    print()
    print(story)


def getNextMode():
    return "QUIT"


if __name__ == "__main__":
    main()
