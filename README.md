# Story Circus

Story Circus is a random story generator app which can create fun and silly stories for your enjoyment!

## Downloading

There are two options for downloading. You can either download a .zip file from the Releases page, or you can clone the repository with the following command:

```console
git clone https://github.com/JeremiahK96/story_circus/
```

## Running the Program

You can run the program using either the CLI or GUI interface.

### GUI Program Instructions

To open the GUI, open the `gui.py` file with your tool of choice, whether that's through your IDE or on the command line:

```console
python ./gui.py
```

Click "Start", and you will see a list of story options to pick from. Click on the one you want to read, and then click "Next". Depending on the story you choose, it might have multiple word lists or "flavors" to pick from. If so, you can select one in the same fashion, and click "Next".

A new window will open with the story printed out for you to read. After you finish the story, you can click "Repeat Same Story" to generate the same story again with new words, or "Pick New Story" to go back the the story selection screen.

At any time, you can click "Quit" to exit the program.

### CLI Program Instructions

The command line version is run by executing the `cli.py` file. It plays very similarly to the GUI version, except that you must make your choices by inputting the number and pressing Enter on your keyboard. The terminal screen is cleared often, and pauses after each story until you press Enter again, to help make it easier to read.

## Adding Stories

All of the stories are read from files in the `data/` directory, and if you create your own files, they will automatically show up in the selection menu. In order to add a story, you need to create two files, a `.story` file, and a `.words` file.

### `.story` Files

The `.story` files are used to define the story layout, similar to how a "fill in the blanks" game works on the back of a cereal box.

The first line of the file is the title of the story. After this line, you can have any number of blank lines, and then all remaining lines make up the story itself. For the story, you should type out all the text required for the story itself, complete with newlines wherever you need them.

To add random elements into your story, you need to add labels. Labels are sections in the story that will be replaced with a random option from that label's pool of words. All labels are opened with a left curly brace, and closed with a right curly brace. A simple example for a label could be `{Person}` or `{FunnySound}`. Take a look at the example files to see what can be done.

### `.words` Files

The `.words` files are used to list all the word options for each label in your story. These are stored in a separate file to allow you to create multiple "flavors" of the same story, or to share generic `.words` files between multiple `.story` files. The program will automatically figure out which files are compatible with each other, so make sure you include all the labels you need for your `.story` file.

The first line of the file is the title for the word list. After this, you can have any number of blank lines, and then the first populated line will be a label name as it is written in the `.story` file. For the above example, this should be `Person` or `FunnySound`. In the lines that follow after the label, you can add as many optional words as you want, and any of them can be chosen to fill in the story! Make sure you leave a blank line after the last word option to close out the label, and then you can add another label in the same fashion. You can indent the lines however you like, because all leading whitespace is ignored.

There is nothing wrong with having more labels than you need in your `.words` list, as long as you aren't missing any from your `.story` list.

### More Powerful Labels Features

Basic labels don't give you much control, because they simply pick any random value and then forget about it. To increase the potential of labels, there are two optional features you can use: IDs and sub-labels.

#### IDs for Labels

In a `.story` file, you can give any label an ID by using a colon between the label name and its ID. For example, `{Person:1}`, `{Color:3}`, or `{FoodItem:6}`. Labels with IDs have a "memory", because if you use them multiple times in the same story, they will always show the same option each time. Also, if you have multiple IDs for the same label, they will never be the same. This allows you the ability to make longer stories with long-term characters.

#### Sub-Labels

You can create sub-labels in a `.story` file by using a backslash between the label name and its sub-label. For example, `{Animal:2/Sound}` or `{Object:3/Weight}`. This can be used to connect multiple words to each other that should match, or can be used to intentionally mismatch things.

In order for this to work, you need to modify the `.words` file to match all the sub-labels used in the story. For each label that needs sub-labels, you put them all on the same line separated by backslashes, with the label first. Then all the word options need to be expanded in the exact same way to match the sublabels. So for an animal, you might do something like this:

```
Animal/Color/Sound/Smell
    bear/brown/growl/musky
    hyena/tan/laugh/damp
```

Each word option needs to match the layout of the label and sub-labels exactly.
