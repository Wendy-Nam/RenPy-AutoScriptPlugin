# Initialize Python environment with necessary constants and configurations
init -1 python:
    # Constants for API and model usage
    API_KEY = "" # replace it with your API key 
    MODEL_NAME = 'gpt-3.5-turbo-16k-0613' # replace it with your model name

    # Directory paths for story configurations
    DIR_PATH = ".../RenPy-AutoScriptPlugin/" # replace it with the absolute path of your plugin
    STORY_CONFIG_PATH = DIR_PATH + "Stories/Cyberpunk-Hacker's-Quest/" # replace it with the path of your story
    
    # Interval for summarization (can be adjusted as needed)
    SUMMARIZE_INTERVAL = 3

    # File paths for various game configurations
    STORY_INSTRUCTIONS_FILE = STORY_CONFIG_PATH + "story_instructions.txt"
    ATTRIBUTE_PATH = STORY_CONFIG_PATH + "character_attributes.json"
    OPTIONS_PATH = STORY_CONFIG_PATH + "character_options.json"
    ENDING_CONFIG_FILE = STORY_CONFIG_PATH + "end_conditions.json"
    SAVE_FILE_PARTNER = DIR_PATH + "saved-files/partner_data.json"
    SAVE_FILE_CONVERS = DIR_PATH + "saved-files/conversation_history.json"
    
    # Function to determine status based on attribute values
    def get_status(attribute_details, value):
        for range_str, status in attribute_details["status"].items():
            # Check for a range like "0-10"
            if "-" in range_str:
                start, end = map(int, range_str.split("-"))
                if start <= value <= end:
                    return status
            # Check for a single value like "0"
            elif value == int(range_str):
                return status
        # Default status if no matching range or value found
        return "Unknown"
    
    def save_to_json(obj):
        """Converts an object to a JSON-serializable format."""
        data = {}
        for attr_name in dir(obj):
            if not callable(getattr(obj, attr_name)) and not attr_name.startswith("__"):
                attr_value = getattr(obj, attr_name)
                data[attr_name] = attr_value
        return data
    
    def load_from_json(data, obj):
        """Populates an object's attributes from a JSON-serializable format."""
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
    
    # Save the current game state
    def save_game():
        if gameGPT and gameGPT.partner:
            partner_data = save_to_json(gameGPT.partner)
            with open(SAVE_FILE_PARTNER, 'w+') as file:
                json.dump(partner_data, file)
            with open(SAVE_FILE_CONVERS, 'w+') as file:
                json.dump(gameGPT.conversation_history, file)
            print("Game saved.")
    
    # Function to clear all persistent variables and saved data
    def destroy_saved_data():
        for attr in dir(persistent):
            if not callable(attr) and not attr.startswith("_"):
                setattr(persistent, attr, None)
        open(SAVE_FILE_CONVERS, 'w+').close()
        open(SAVE_FILE_PARTNER, 'w+').close()
        return


# Default values for player and partner names
default player_name = None
default partner_name = None
default persistent.player_name = None
default persistent.story_theme = None
default persistent.partner_data = None
define player = Character("[player_name]", color="#296229")
define partner = Character("[partner_name]", color="#2e0d3d")

# UI components for the game
init -1:
    # Screen for auto script preferences
    screen autoscript_preference(character):
        hbox:
            # Various action buttons for game management and character details
            textbutton "| Reset Game |" action [Show('reset_game')]
            textbutton "| Save Game |" action [Function(save_game)]
            textbutton "| Character Info |" action NullAction():
                hovered Show("character_info", character=character)
                unhovered Hide("character_info")
            textbutton "| Character Status |" action NullAction():
                hovered Show("character_status", character=character)
                unhovered Hide("character_status")

    # Screen for confirming game reset
    screen reset_game:
        frame:
            align (0.5, 0.5)
            padding (20, 20)
            background "#bcbcbcff"
            vbox:
                text "Are you sure you want to reset the game?"
                hbox:
                    # Decision buttons for game reset
                    textbutton "Yes" action [Function(destroy_saved_data), SetVariable('gameGPT.is_running', False), Hide('reset_game')]
                    textbutton "No" action Hide('reset_game')

    # Screen displaying character information
    screen character_info(character):
        frame:
            align (0.5, 0.5)
            padding (30, 30)
            background "#ff000014"
            vbox:
                text "{b}[character.name]'s Information{b}" size 35 line_spacing 10
                for attribute, value in character.fixed_attributes.items():
                    text "{}: {}".format(attribute.capitalize(), value) size 25 line_spacing 10

    # Screen displaying character status based on attributes
    screen character_status(character):
        frame:
            align (0.5, 0.5)
            padding (30, 30)
            background "#00a2ff14"
            vbox:
                text "{b}[character.name]'s Status{b}" size 35
                for attribute, details in character.attributes.items():
                    hbox:
                        vbox:
                            text "{}:".format(attribute.replace("_", " ").capitalize()) size 25
                            text get_status(details, details["value"]) size 18 color "#d9f57b6c"
                        text str(details["value"]) size 25

# Game starting label
label AutoScript:
    # Clear all persistent variables if theme changed
    if persistent.story_theme != STORY_CONFIG_PATH:
        $ destroy_saved_data()
        $ persistent.story_theme = STORY_CONFIG_PATH
        $ print("Theme changed. Game data cleared.")
    # Check if player name is saved
    if persistent.player_name is None:
        jump PutYourName
    else:
        $ player_name = persistent.player_name
        "Welcome Back, [player_name]."
        $ partner_character = GPTCharacter()
        # Check if partner data exists
        if (os.stat(SAVE_FILE_CONVERS).st_size == 0):
            jump CreateAutoCharacter
        else:
            jump StartGame

# Label for name input
label PutYourName:
    # Capture player's name
    $ player_name = renpy.input("What is your name? ").strip()
    $ persistent.player_name = player_name
    jump CreateAutoCharacter
    return

# Label for creating an auto-generated character
label CreateAutoCharacter:
    $ bd = CharacterBuilder()
    $ partner_character = bd.build_character()
    $ persistent.partner_name = partner_character.name
    $ partner_name = persistent.partner_name
    jump StartGame
    return

# Main game loop label
label StartGame:
    # Initialize and run the GPT script
    $ persistent.story_theme = STORY_CONFIG_PATH
    $ gameGPT = AutoScriptGPT(player=player, partner=partner_character)
    # Display the autoscript preference screen
    show screen autoscript_preference(character=partner_character)
    "Starting the game..."
    $ gameGPT.run()
    return