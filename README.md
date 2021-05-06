# dictionary_generator
Generates a dictionary by scraping from Wordnik. Made in a short amount of time for fun. Not for use in production.

## How it works
Starts with the seed word. Gets the definition of the seed word. Stores the definition. Selects the first word in the definition. Repeats the process with this new word.

## Usage:
\>>> import dictionary_generator

\>>> entries = dictionary_generator.main(seed="apple", delay=0.01, runtime=10)

![image](https://user-images.githubusercontent.com/22204498/117265840-812bc480-ae09-11eb-9c89-55df47ae9cb9.png)

