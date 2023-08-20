init python:
    import json
    import requests

    class AutoScriptGPT:
        # Initialization of the AutoScriptGPT class
        def __init__(self, player, partner):
            self.player = player
            self.partner = partner
            self.is_running = True
            self.conversation_history = []
            self.load_config()
            self.load_game()
            self.parser = AutoScriptParser(self.player, self.partner)
            self.initial_prompt = self.generate_initial_prompt()

        # Load game configuration from the provided files
        def load_config(self):
            with open(ENDING_CONFIG_FILE, 'r') as f:
                self.ending_config = json.load(f)
            with open(STORY_INSTRUCTIONS_FILE, "r") as f:
                self.story_instructions = f.read().format(self=self)
                
        # Generate the initial prompt for the game based on the loaded configurations
        def generate_initial_prompt(self):
            attribute_details = "; ".join([
                f"Modify {attribute_name} by: 'increase/decrease {attribute_name} [value]' (Range: {attribute_data['range'][0]}-{attribute_data['range'][1]})"
                for attribute_name, attribute_data in self.partner.attributes.items()
            ])
            # Construct and return the initial prompt
            return f"""
Event-Based Visual Novel Guide:

Story: {self.story_instructions}
Attributes: {attribute_details} (e.g. increase/decrease health by 10)

Rules:

1. Keep the story moving forward; avoid repetition.
2. Present up to 3 menu choices with hidden outcomes.
3. Do not use '[ ]'.
4. Frequent attribute modifications are encouraged.

Follow this STRICT format:

*Modify Attributes*
[Insert changes here or state 'None' if no changes]

*Dialog*
{self.partner.name}: [Dialog]
{self.player.name}: [Reply]

*Narration*
[Concisely describe settings, actions, or events without using ':']

*Menu*
1. [option 1]
2. [option 2]
3. [option 3]

Avoid additional space between lines.
"""
        # Main method to run the game loop
        def run(self):
            # The starting point is either the initial_prompt or the last item in conversation history.
            starting_point = self.initial_prompt if not self.conversation_history else self.conversation_history[-1]
            # Initialize with the starting point
            res = self.getResponse(starting_point)
            self.conversation_history.append(res)
            while self.is_running:
                narrator("Click the next button and wait for a minute...")
                op = self.parser.parse_auto_dialog(res)
                res = self.getResponse(op)
                self.conversation_history.append(res)
                # Check conditions only if still running to optimize performance
                if self.is_running and len(self.conversation_history) >= SUMMARIZE_INTERVAL:
                    self.summarize_and_append()
                self.check_game_ending()
            
        # Check if game should end based on the ending configurations
        def check_game_ending(self):
            for ending in self.ending_config:
                attribute_value = self.partner.get_attribute_value(ending['attribute'])
                if attribute_value is not None and eval(f"{attribute_value} {ending['condition']} {ending['value']}"):
                    custom_ending = self.generate_custom_ending()
                    print(custom_ending)
                    self.parser.parse_auto_dialog(custom_ending)
                    narrator(ending['message'])
                    destroy_saved_data()
                    self.is_running = False
                    return

        # Load previously saved game state
        def load_game(self):
            if os.path.exists(SAVE_FILE_PARTNER) and (os.stat(SAVE_FILE_CONVERS).st_size != 0):
                with open(SAVE_FILE_PARTNER, 'r') as file:
                    data = json.load(file)
                    self.partner = load_from_json(data, self.partner)
                if os.path.exists(SAVE_FILE_CONVERS) and (os.stat(SAVE_FILE_CONVERS).st_size != 0):
                    with open(SAVE_FILE_CONVERS, 'r') as file:
                        self.conversation_history = json.load(file)
                narrator("Game data loaded.")
            else:
                narrator("No saved game data found.")
        
        # This method helps in generating a summary for the game progression
        def summarize_and_append(self):
            summarized_storyline = self.summarize_storyline('\n'.join(str(x) for x in self.conversation_history[1:]))
            print("Summarized Storyline: ", summarized_storyline)
            self.conversation_history = [self.initial_prompt, summarized_storyline]
    
        # Summarize the storyline for the player
        def summarize_storyline(self, pre_summary_context) -> str:
            prompt =  f"""Recap of the journey:
        
            {pre_summary_context}
        
            Based on the above, provide a short summary:
            1. Highlight key decisions and events.
            2. Detail characters' emotional journeys.
            3. Include vital dialogues and interactions.
        
            After summarizing, continue the story from the last decision.
        
            """
            return self.getResponse(prompt)

        # Generate a custom ending for the game based on character attributes
        def generate_custom_ending(self):
            partner_attributes = [attr for attr in dir(self.partner) if not callable(getattr(self.partner, attr)) and not attr.startswith('__')]
            status_context = "\n".join([f"Partner {attr.capitalize()}: {getattr(self.partner, attr)}" for attr in partner_attributes])
            conversation_context = "\n".join(self.conversation_history[-5:])  # Last 5 conversations for context
            prompt = f"""Based on the journey and current status:
            {status_context}

            Recent events:
            {conversation_context}
            
            Craft a suitable ending for the story, considering the choices made, the emotions felt, the events that have unfolded, and the current status.
            
            """
            ending = self.getResponse(prompt)
            return ending
        
        # Communicate with the GPT model to get the desired response
        def getResponse(self, prompt) -> str:
            self.conversation_history.append(prompt)
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
            context = '\n'.join([f"Partner {attr.capitalize()}: {getattr(self.partner, attr)}" for attr in dir(self.partner) if not callable(getattr(self.partner, attr)) and not attr.startswith("__")])
            data = {
                "model": MODEL_NAME,
                'messages': [{'role': 'system', 'content': context}]
            }
            data['messages'].extend([{'role': 'user', 'content': message} for message in self.conversation_history])
            try:
                response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except requests.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                self.conversation_history.pop()
                narrator("An error occurred while communicating with the GPT model. Please try again.")
                return ""
            except Exception as err:
                self.conversation_history.pop()
                print(f"Other error occurred: {err}")
                return ""


# # RenPy persistent data setup
# init -2 python:
#     import renpy.store
#     renpy.store.persistent = {}