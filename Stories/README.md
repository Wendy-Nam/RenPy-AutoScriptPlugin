# Configuration Template Instruction.

👇 <b><u>Please use these instructions as a reference, when asking chatGPT to generate new configuration files based on the theme you're planning.</b></u>

If the current list of options and attributes is limited, don't hesitate to request additional options and attributes, especially if you're aiming for a rich and immersive story setting.

(💡 You can also ask GPT to suggest a theme suitable for a text-based game format)

## Template Instructions for Creating a Role-Playing Game Application (For Asking chatGPT)

I'm creating a text-based RPG similar to 'Princess Maker.' I've defined attributes, dynamic status values, and game-ending conditions using JSON files: 'character_options.json,' 'character_attributes.json,' and 'end_conditions.json.' Also, there's 'story_instructions.txt' for the final story theme. Below, you'll find a prototype JSON file structure and a concluding text file. Please follow the given format while adjusting content to match the chosen theme.

1.character_attributes.json

```
{
    "<Attribute Name>": {
        "value": <Integer representing the current value>,
        "range": [<Minimum Value>, <Maximum Value>],
        "status": {
        "<Range Start1>-<Range End1>": "<Status Description1>",
        "<Range Start2>-<Range End2>": "<Status Description2>",
        ...
        }
    },
    ...
}
```

Explanation:

- <Attribute Name>: Refers to the attribute's name (e.g., "experience", "reputation").
  - (replace any spaces within attribute names with underscores (\_))
- <Integer representing the current value>: Indicates the current numerical value of the attribute.
- <Minimum Value> and <Maximum Value>: Denote the lower and upper limits of the attribute's potential values.
- <Range StartX>-<Range EndX>: Defines the value ranges corresponding to attribute statuses.
- <Status DescriptionX>: Describes the status associated with the respective value range.

### 2.character_options.json

```
{
    "<Attribute Key>": {
        "options": [
        "<Option 1>",
        "<Option 2>",
        ...
        ],
        "prompt": "<Description of the attribute for user prompt>"
    },
    ...
}
```

Explanation:

- <Attribute Key>: Represents the name of the attribute (e.g., "race", "origin").
- <Option X>: Possible values or choices for that attribute.
- <Description of the attribute for user prompt>: A short description or a keyword to prompt the user about this attribute.

### 3.end_conditions.json

```
[
    {
    "attribute": "<Attribute Name>",
    "condition": "<Comparison Operator>",
    "value": <Threshold Value>,
    "message": "<Outcome Message>"
    },
...
]
```

Explanation:

- <Attribute Name>: The name of the attribute being evaluated (e.g., "health", "experience").
- <Comparison Operator>: The condition for comparison (e.g., "<=", ">=").
- <Threshold Value>: The numeric value used as the threshold for the condition.
- <Outcome Message>: The message displayed when the condition is met.

### 4.story_instructions.txt

```
There are two characters, [partner_name] and [player_name].
Generate an improvised setting for the story. Describe the following elements:

1. The place where the story takes place: <Place Description>.
2. The time period (e.g., past, present, future) in which the story occurs: <Time Period>.
3. The relationship between the characters or a unique situation they find themselves in: <Relationship/Situation Description>.

After describing these elements, proceed with the story by providing the attribute modifications and narrative content.
Generate a detailed scene where you describe the location they are in, their emotions, and the atmosphere around them. Set the stage for an important decision they have to make: <Detailed Scene Description>.

Every choice is a gamble: some promising options might swiftly plunge players into pitfalls, while other seemingly dire choices harbor hidden rewards. Players should constantly anticipate and brace for unexpected twists and turns.
```

Explanation:

- [partner_name] and [player_name]: Placeholders for character names.
- <Place Description>: Placeholder for a description of the setting.
- <Time Period>: Placeholder for the time period in which the story occurs.
- <Relationship/Situation Description>: Placeholder for the relationship or situation between the two characters.
- <Detailed Scene Description>: Placeholder for the in-depth scene setup where the characters find themselves.
