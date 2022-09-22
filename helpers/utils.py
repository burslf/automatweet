import random

def remove_empty_lines(lyrics):
    return list(filter((lambda x: len(x) > 0), lyrics))

def get_random_lyrics_index(lyrics):
    return random.randrange(len(lyrics)-2)
