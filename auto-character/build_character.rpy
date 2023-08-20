init python:
    import json

    # The CharacterBuilder class provides functionalities to create a character with specific attributes.
    class CharacterBuilder:
        def __init__(self):
            # Initializing a new GPTCharacter object upon creating a CharacterBuilder instance.
            self.character = GPTCharacter()

        def build_character(self):
            # Load attributes from a predefined path and ask the user for the character's name.
            self.character.load_attributes(ATTRIBUTE_PATH)
            self.character.name = renpy.input("What is the name of the character?")
            
            # Load attribute options and iterate through each attribute to set its value.
            attribute_options = self.load_attribute_options(OPTIONS_PATH)
            for attribute, meta in attribute_options.items():
                value = self.choose_option(self.character.name, meta['options'], meta['prompt'])
                if attribute in self.character.attributes:
                    self.character.set_dynamic_attribute(attribute, value)
                else:
                    self.character.set_fixed_attribute(attribute, value)
            
            # Return the built character.
            return self.character

        def choose_option(self, character_name, options, prompt):
            # Prompt the user to select an option based on the given prompt.
            sentence = f"How does {character_name} feel about their {prompt}? Choose an option:"
            renpy.say(None, sentence)
            
            # Create structured options for menu display.
            structured_options = [(option, i) for i, option in enumerate(options)]
            
            # Display the options to the user and get their selection.
            option_index = renpy.display_menu(structured_options)
            selected_option = options[option_index]
            
            # Confirm the user's selection.
            renpy.say(None, f"{character_name}'s {prompt} is {selected_option}.")
            
            return selected_option

        def load_attribute_options(self, filepath):
            # Load and return attribute options from a given filepath.
            try:
                with open(filepath, "r") as file:
                    return json.load(file)
            except Exception as e:
                renpy.say(None, f"Error loading attributes: {e}")
                return {}

    # The GPTCharacter class represents a character with various attributes.
    class GPTCharacter:
        def __init__(self):
            # Initialize basic character details.
            self.name = ""
            self.fixed_attributes = {}
            self.attributes = {}
    
        def load_attributes(self, filepath):
            # Load attributes from a given filepath and categorize them as fixed or dynamic.
            try:
                with open(filepath, "r") as file:
                    data = json.load(file)
                    for key, value in data.items():
                        if 'value' in value:
                            self.attributes[key] = value
                        else:
                            self.fixed_attributes[key] = value
            except Exception as e:
                renpy.say(None, f"Error loading attributes: {e}")
    
        def set_fixed_attribute(self, attribute_name, value):
            # Set a value for a fixed attribute.
            self.fixed_attributes[attribute_name] = value
    
        def set_dynamic_attribute(self, attribute_name, value):
            # Set a value for a dynamic attribute if it exists.
            if attribute_name in self.attributes:
                self.attributes[attribute_name]['value'] = value
                print(f"Set {attribute_name} to {value}")
    
        def get_attribute_value(self, attribute_name):
            # Get the value of an attribute, checking dynamic first then fixed attributes.
            if attribute_name in self.attributes:
                return self.attributes[attribute_name]['value']
            elif attribute_name in self.fixed_attributes:
                return self.fixed_attributes[attribute_name]
            else:
                return None
