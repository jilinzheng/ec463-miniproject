#!/usr/bin/env python3
"""
PWM Tone Generator based on https://www.coderdojotc.org/micropython/sound/04-play-scale/

Set to play 'Feather' by Nujabes on repeat https://youtube.com/watch?v=hQ5x8pHoIPA
Score obtained from https://musescore.com/user/187873/scores/5064390
"""

import machine
import utime


# GP16 is the speaker pin
SPEAKER_PIN = 16

# FREQUENCIES/NOTES NEEDED
# Frequencies obtained from https://muted.io/note-frequencies/
G4_SHARP = 415.3
A4_SHARP = 466.16
C5 = 523.25
C5_SHARP = 554.37
D5_SHARP = 622.25
F5 = 698.46
G5_SHARP = 830.61

# BPM + NOTE LENGTHS (seconds)
# Calculations obtained from https://bradthemad.org/guitar/tempo_explanation.php
BPM = 180.
SIXTEENTH_NOTE = 15./BPM
TRIPLET_EIGHTH_NOTE = 20./BPM
EIGHTH_NOTE = 30./BPM
QUARTER_NOTE = 60./BPM
DOTTED_QUARTER_NOTE = 90./BPM
HALF_NOTE = 120./BPM

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


# helper functions
def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(10000)
    speaker.freq(int(frequency))
    utime.sleep(duration)


def quiet(duration: float):
    speaker.duty_u16(0)
    utime.sleep(duration)


# MUSIC!
while True:
    print("Playing 'Feather', by Nujabes. Enjoy!")
    # FIRST MEASURE
    playtone(F5,HALF_NOTE)
    playtone(C5_SHARP,DOTTED_QUARTER_NOTE)
    playtone(G5_SHARP,EIGHTH_NOTE)
    # SECOND MEASURE
    playtone(F5,QUARTER_NOTE)
    playtone(D5_SHARP,TRIPLET_EIGHTH_NOTE)
    playtone(F5,TRIPLET_EIGHTH_NOTE)
    playtone(D5_SHARP,TRIPLET_EIGHTH_NOTE)
    playtone(C5_SHARP,QUARTER_NOTE)
    playtone(C5,QUARTER_NOTE)
    # THIRD MEASURE
    playtone(C5,EIGHTH_NOTE)
    playtone(G4_SHARP,EIGHTH_NOTE)
    playtone(A4_SHARP,EIGHTH_NOTE)
    playtone(C5,EIGHTH_NOTE)
    playtone(C5_SHARP,DOTTED_QUARTER_NOTE)
    playtone(D5_SHARP,EIGHTH_NOTE)
    # FOURTH MEASURE
    playtone(F5,DOTTED_QUARTER_NOTE)
    playtone(G4_SHARP,SIXTEENTH_NOTE)
    playtone(A4_SHARP,SIXTEENTH_NOTE)
    playtone(C5,EIGHTH_NOTE)
    playtone(C5_SHARP,EIGHTH_NOTE)
    playtone(D5_SHARP,EIGHTH_NOTE)
    playtone(G5_SHARP,EIGHTH_NOTE)
