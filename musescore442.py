# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:06:01 2020
@author: Daniel Manwiller
"""
from music21 import* # Importing everything from the music21 pakcage
from config import PATH_TO_MUSESCORE

# Setting the proper environment variables to find the installation of MuseScore3
us = environment.UserSettings()
#NOTE: Edit the config.py file to change path to Musescore app
us['musicxmlPath'] = PATH_TO_MUSESCORE

# Dictionaries for G Clef and C Clef
g_dict = {'L0': "c", 'L1': "e", 'L-1': "A'", 'L2': "g", 'L-2': "F'", 
          'L3': "b", 'L-3': "D'", 'L4': "d'", 'L5': "f'", 'L6': "a'", 
          'L7': "c''", 'L8': "e''", 'S0': "d", 'S1': "f", 'S-1': "B'",
          'S2': "a", 'S-2': "G'", 'S3': "c'", 'S-3': "E'", 'S4': "e'",
          'S5': "g'", 'S6': "b'", 'S7': "d''", 'S8': "f''"}
c_dict = {'L0': "EE", 'L1': "GG", 'L-1': "DD", 'L2': "BB", 'L-2': "BBB", 
          'L3': "D", 'L-3': "GGG", 'L4': "F'", 'L5': "A'", 'L6': "c", 
          'L7': "e", 'L8': "g", 'S0': "FF", 'S1': "AA", 'S-1': "DD",
          'S2': "C", 'S-2': "BBB", 'S3': "E", 'S-3': "GGG", 'S4': "G",
          'S5': "B'", 'S6': "d", 'S7': "f", 'S8': "a"}

# Converts Agnostic encoding translation to TinyNotation string
def agnostic2tiny(datastring):
    data = datastring.split()
    tinystring = "tinyNotation: "
    clef = ""
    time_signature = ""       
    accidental = "" # For setting accidentals properly
    key_signature = 0
    
    # Making sure we have a clef
    if data[0][0] != '*':
        raise Exception('No Clef Symbol Detected')
    else:
        clef = data[0][1]
    
    # Getting the key and time signatures:
    flag = 0 # Know when to stop when we get 2 time signature numbers
    iterator = 1 # Where to start...
    while flag < 2:
        if data[iterator][0] == "-" or data[iterator][0] == "#":
            accidental += data[iterator][0]
        elif data[iterator][0] == '@':
            if flag == 0:
                time_signature += data[iterator][1:] + "/"
                flag += 1
            else:
                time_signature += data[iterator][1:]
                flag += 1
        elif data[iterator][0] == '&':
            if data[iterator][1:] == "C": # Common Meter
                time_signature = "4/4"
                flag = 2
            else: # Must = 'CC' ~ Cut Time
                time_signature = "2/2"
                flag = 2
        else:
            pass #raise Exception('Not a valid symbol before finished time signature')
        iterator += 1
    # end while()
    tinystring += time_signature # Setting the time signature
    if accidental != "":  # Defining the key_signature
        if accidental[0] == "#":
            key_signature = len(accidental)
        else:
            key_signature = len(accidental)*(-1)
    accidental = "" # Resetting accidental    
    
    # Looping over the rest of the data
    for d in data[iterator:]:
        if d[0] == "-" or d[0] == "n" or d[0] == "#": # Setting proper accidentals
            accidental = d
        elif d[0] == "r": # Adding rests
            tinystring += " " + d
        elif d[0] == 'L' or d[0] == 'S': # Adding notes
            tinystring += " " # Adding proper spacing
            note_data = d.split('\\')
            if clef == "G":
                tinystring += g_dict[note_data[0]] + note_data[1]
            else: # Clef is C
                tinystring += c_dict[note_data[0]] + note_data[1]
            #####################################################
            if accidental != "": # Adding accidentals properly
                tinystring += accidental
                accidental = ""
        elif d[0] == '.' or d[0] == '~': # Adding dotted notes and ties
            tinystring += d[0]
        
    return key_signature, tinystring
# end agnostic2tiny()

def ShowMuseScore(datastring):
    print(datastring)
    key_signature, tinystring = agnostic2tiny(datastring)
    # Parsing the tinyNotation data from the deep-learning model
    t = converter.parse(tinystring)
    t.keySignature = key.KeySignature(key_signature) 

    # Fixing a weird thing with music21 notation where the notes aren't properly
    # synced with the key signature. This took forever to make work...
    for n in t.recurse().notes: # Looping over all the notes
        nStep = n.pitch.step
        rightAccidental = t.keySignature.accidentalByStep(nStep) # Finding proper accidental
        if n.pitch.accidental == None: # Making sure not to override proper accidentals
            n.pitch.accidental = rightAccidental # Setting the correct accidental
            if n.pitch.accidental != None: # If we have now changed the accidental
                n.pitch.accidental.displayStatus = False # Then don't display it
    # Showing the output in MuseScore. From there, any mistakes from the deep-learning
    # model can be edited and the final output can be exported as a .pdf or as an
    # audio .mp3 file.
    t.show('musicxml')
#end ShowMuseScore()
