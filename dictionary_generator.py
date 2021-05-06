from lxml import html
import requests
import time
import random as rand

# Depracated, do not use
def scrape_definition_MW(word):
    """Scrapes a definition from Merriam-webster"""
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    page = requests.get(url)
    
    xml_tree = html.fromstring(page.content)
    
    
    definition_arr = xml_tree.xpath(
        '//*[@id="dictionary-entry-1"]/div[2]/div[1]/span/div/span[2]/span/text()'
    )
    definition = "".join(definition_arr)
    entry = f"{word.upper()}: " + definition
    words = ''.join(list(filter(lambda x: x.isalpha() or x==' ', definition))).split(' ')
    return entry, words

# This is the function to use
def scrape_definition_wordnik(word):
    """Scrapes a definition from wordnik/duckduckgo"""
    word = word.lower() # To make sure it fits the URL scheme
    url = f"https://www.wordnik.com/words/{word}"
    page = requests.get(url)
    
    xml_tree = html.fromstring(page.content)
    
    # Create definition to add to dictionary
    for i in range(1, 100):
        definition_arr = xml_tree.xpath(
            f'//*[@id="define"]/div/ul[1]/li[{i}]/text()'
        )
        definition = "".join(definition_arr).strip()
        if len(definition) > 0:
            break
        
    entry = f"{word.upper()}: " + definition
    
    # Create next list of words to use
    allowed_non_alpha_chars = '-'
    filter_for_allowed_chars = lambda word_: all([c.isalpha() or c in allowed_non_alpha_chars for c in word_])
    words = ''.join(list(filter(lambda x: filter_for_allowed_chars(x) or x==' ', definition))).split(' ')
    words = list(filter(lambda w: len(w) > 0 and all([filter_for_allowed_chars(c) for c in w]), words))
    words = [w.lower() for w in words]
    
    
    # Checks for errors and missing words, returns -1,-1 if error
    if len(words) < 1:
        return -1, -1
    return entry, words



# Initialize global variables
# Initializing them right above main instead of the top of the document
# because this is closer to the context they are used in
super_dict = dict()
start_time = -1

def main(seed="owns", delay=0.05, runtime=100):
    """The main loop to generate the dictionary definitions.
    
    Args:
        seed (str): The seed word to start out the dictionary generation with.
        delay (float): The time in seconds between dictionary queries. Increase this if you are getting ratelimited.
        runtime (float): The amount of time to run the program for.
    """
    global super_dict
    global start_time
    
    # Initialize timer, if not already initialized.
    # Timer must be global because main() is recursive and I dont want to pass the arg down through the calls
    if start_time < 0:
        start_time = time.time()
    # Begins with the seed word
    word = seed
    entry, words = scrape_definition_wordnik(word)
    super_dict_entry = {word.upper() : entry}
    super_dict.update(super_dict_entry)
    
    # Main loop to continuously add words to dictionary
    while (time.time() - start_time) < runtime:
        time.sleep(0.05)
        for i in range(len(words)):
            word = words[i].lower()
            # Check if given word is in dictionary already
            if word.upper() in super_dict.keys():
                print(f'"{word.upper()}" already added, skipping...')
                # In the event that all available words are already in the dictionary, try again with a random one
                
                # Check for issues
                if all([w.upper() in super_dict.keys() for w in words]):
                    main(seed=rand.choice(list(super_dict.keys()))) # Must convert to list first, rand.choice cant use dict_keys obj
                continue
            # print(f'Querying "{word.upper()}"')
            entry_, words_ = scrape_definition_wordnik(word)
            
            # Check for errors
            if entry_ == -1 or words_ == -1:
                continue
            
            entry, words = entry_, words_
                
            # No errors, so updates super_dict with the word : definition pair
            super_dict_entry = {word.upper() : entry}
            super_dict.update(super_dict_entry)
            print(f"Added: {entry}")
            break
            
    # Adding an if statement, because the program could stop for other reasons (errors)
    if (time.time() - start_time) >= runtime:
        print("RUNTIME over, exiting program...")
        
    return super_dict
