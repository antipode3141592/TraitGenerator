"""For randomly generating characters with various traits."""
import csv
import random
from tkinter import Tk, ttk, Label, Entry, Checkbutton, Button, IntVar, StringVar, Text, N, W, E, S, WORD, END, font

def getRandomArchetype(archetypeList, regions = ['All']):
    """Return a random selection from the provided list"""
    if 'All' in regions:
        choice = random.choice(archetypeList)
        return choice
    return random.choice([archetype for archetype in archetypeList if archetype['Region'] in regions])

def getRandomGender(genderList):
    """Return a random selection from the provided list"""
    return random.choice(genderList)

def getRandomTrait(traitList, currentList):
    """Return a random selection from the provided list if not in list.  If all ready in list, recurse"""
    randomTrait = random.choice(traitList)
    if randomTrait not in currentList:
        return randomTrait
    getRandomTrait(traitList, currentList)

def getRandomTraits(masterTraitList, traitCount):
    """Return a list of traits of length traitCount"""
    returnList = []
    for _ in range(traitCount):
        returnList.append(getRandomTrait(masterTraitList, returnList))
    return returnList

def printCharacter(outputTraits, masterAdverbList, index, archetype, gender):
    """Pretty Print to console the character"""
    characterString = characterToString(outputTraits, masterAdverbList, index, archetype, gender)
    print(characterString)
    return characterString

def characterToString(outputTraits, masterAdverbList, index, archetype, gender):
    """Return a string representation of the character"""
    _outputString = f"Character {index + 1}, {archetype['Archetype']} (pg. {archetype['Page']}), {gender} : \n"
    for trait in outputTraits:
        _outputString = _outputString + str(random.choice(masterAdverbList)) + " " + trait['Trait']
        if trait != outputTraits[len(outputTraits)-1]:
            _outputString = _outputString + ', '
    _outputString = _outputString + '\n\n'
    return _outputString

def generate(characterCount, textBox, characterRegions=['All']):
    """Generate characterCount number of characters"""
    #if 'All' is in characterRegions, set characterRegions to 'All'
    if 'All' in characterRegions:
        characterRegions = ['All']
    #clear the text box
    textBox.delete(1.0, END)
    for index in range(characterCount):
        characterTraits = getRandomTraits(MASTER_TRAIT_LIST, 3)
        archetype = getRandomArchetype(MASTER_ARCHETYPE_LIST, characterRegions)
        gender = getRandomGender(MASTER_GENDER_LIST)
        characterText = printCharacter(characterTraits, MASTER_ADVERB_LIST, index, archetype, gender)
        textBox.insert(END, characterText)

def regionSelected():
    """Update the list of regions"""
    SELECTED_REGIONS.clear()
    for value in REGION_CHECKBOXES.values():
        if value.get() == '1':
            if value not in SELECTED_REGIONS:
                SELECTED_REGIONS.append(value._name)

###############################################################################################
# Definitions
CHARACTER_COUNT = 3
TRAIT_COUNT = 3
CHARCTER_TRAITS = []
TRAIT_LIST_FILE = 'Traits.csv'
ARCHETYPE_LIST_FILE = 'Archetypes.csv'
REGIONS_LIST_FILE = 'Regions.csv'
MASTER_TRAIT_LIST = []
MASTER_GENDER_LIST = ['He/Him', 'She/Her', 'They/Them', 'He/They', 'She/They']
MASTER_ARCHETYPE_LIST = []
MASTER_ADVERB_LIST = ['Always', 'Commonly', 'Consistently', 'Constantly', 'Continuously',
                      'Extremely', 'Frequently', 'Generally', 'Infrequently', 'Never', 'Normally',
                      'Occasionally', 'Often', 'Ordinarily', 'Overtly', 'Persistently', 'Rarely',
                      'Recurrently', 'Regularly', 'Repeatedly', 'Reputedly', 'Seldom', 'Slightly', 'Sometimes',
                      'Somewhat', 'Typically', 'Unwittingly', 'Usually', 'Very']
MASTER_REGION_LIST = []

# tkinter variables
REGION_CHECKBOXES = {}
SELECTED_REGIONS = []

###############################################################################################
# Setup workspace
ws = Tk()
ws.title("Talislanta Character Generator")
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 720
ws.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
ws.configure(bg="#567", padx=10, pady=10)

mainframe = ttk.Frame(ws, padding="10 10 10 10", relief='ridge', borderwidth=5)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S), ipadx=5, ipady=5)

underlined_font = font.Font(family="TkDefaultFont", size=12, underline=True)

###############################################################################################
# Load Data
#load traits csv
with open(TRAIT_LIST_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        MASTER_TRAIT_LIST.append(line)
#load archetypes csv
with open(ARCHETYPE_LIST_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        MASTER_ARCHETYPE_LIST.append(line)
#load archetypes csv
with open(REGIONS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        MASTER_REGION_LIST.append(line)

# Quantity
Label(mainframe, text="Quantity").grid(row=0, column=0)
_quantity = IntVar()
quantityBox = Entry(mainframe, text=_quantity)
quantityBox.grid(row=0, column=1)
_quantity.set(CHARACTER_COUNT)

# Region Selection
Label(mainframe, text="Regions", font=underlined_font).grid(row=1, column=2)

i = 0
j = 2
for region in MASTER_REGION_LIST:
    regionName = region['Region']
    REGION_CHECKBOXES[regionName] = StringVar(value=regionName, name=regionName)
    Checkbutton(mainframe, text=region['Region'], variable=REGION_CHECKBOXES[regionName], command=regionSelected).grid(row=j, column=i)
    i += 1
    if i >= 5:
        i = 0
        j += 1

# PC/NPC Selection via checkbox

#display text window for the characters to be displayed


# Generate Character(s) Button

generateButton = Button(mainframe, text="Generate", command=lambda: generate(int(quantityBox.get()), characterTextBox, SELECTED_REGIONS))
generateButton.grid(row=j+1, column=2, padx=5, pady=5)


Label(mainframe, text="Characters", font=underlined_font).grid(row=j+2, column=2)
characterTextBox = Text(mainframe, wrap=WORD)
TEXTBOX_HEIGHT = 5
characterTextBox.grid(row=j+3, column=0, columnspan=5, rowspan=TEXTBOX_HEIGHT, ipadx=5, ipady=5)

ws.mainloop()
