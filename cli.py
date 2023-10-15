"""Command Line Interface for program"""

import story_circus as sc

def main():
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
    main()
