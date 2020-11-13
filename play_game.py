import json

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('spooky_mansion.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        # TODO: print any available items in the room...
        print(here["items"])
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_visable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action in ["help"]:
            print_instructions()
            continue
        if action in ["stuff"]:
            if stuff == []:
                print("you have nothing")
            else:
                print(stuff)
            continue
        if action in ["take"]:
            #find value for key in dictionary
            for items in here["items"]:
                stuff.append(items)
                here["items"].remove(items)
                print(stuff)
            continue
        if action in ["drop"]:
            print(stuff)
            remove = str(input("What do you want to drop out of the above? "))
            for xs in stuff:
                if remove == xs:
                    stuff.remove(xs)
                    here["items"].append(xs)
            continue
        if action in ["search"]:
            usable = []
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
                else:
                    continue
            continue
                
            
            

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if selected.get("required_key", False):
                if selected["required_key"] in stuff:
                    current_place = selected['destination']
                    continue
                else:
                    print("You try to open the door, but this door is locked")
                    continue
            else:
                current_place = selected['destination']
                continue
                
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_visable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to repeat instructions")
    print(" - Type 'drop' to drop an item")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()


