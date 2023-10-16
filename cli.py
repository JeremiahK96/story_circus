"""Command Line Interface for program"""

import story_circus as sc
import os

# Game modes.
# The values are displayed to and selected by the user after each story.
NEW_GAME = "Pick a new story"
REPLAY   = "Listen to the same story again"
QUIT     = "That's all for now"


def main():
    """Main program loop."""
    Welcome()
    waitForEnter()

    recipes = sc.loadStoryRecipes()
    wordlists = sc.loadWordLists()
    sc.checkStoryCompatibilities(recipes, wordlists)

    mode = NEW_GAME
    while mode != QUIT:

        if mode == NEW_GAME:
            recipe = pickStoryRecipe(recipes)
            wordlist = pickWordList(wordlists, recipe)

        story = sc.Story(recipe, wordlist)
        story.generate()
        display(story)
        waitForEnter()

        mode = getNextMode()

def Welcome():
    """Display the title splash, and explain the program to the user."""
    print("Story Circus", sc.__version__, "by", sc.__author__)
    print()
    print("This is a silly story generator.")
    print("Enjoy fun stories with randomized elements!")


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


def display(story):
    """Display the generated story."""
    clearScreen()
    print(story.story)


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
