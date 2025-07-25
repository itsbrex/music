# -*- coding: utf-8 -*-
"""Utilities to synthesize singing from text using eCantorix."""

import os
import re
import warnings
import logging
import subprocess
from scipy.io import wavfile
from music.core import normalize_mono

here = os.path.abspath(os.path.dirname(__file__))
ECANTORIXDIR = here + '/ecantorix'
ECANTORIXCACHE = ECANTORIXDIR + '/cache'


# def sing(text="ba-na-nin-ha pra vo-cê",
def sing(text="Mar-ry had a litt-le lamb",
         notes=(4, 2, 0, 2, 4, 4, 4), durs=(1, 1, 1, 1, 1, 1, 2),
         M='4/4', L='1/4', Q=120, K='C', reference=60,
         lang='en', transpose=-36, effect=None):
    #         lang='pt', transpose=-36, effect=None):
    # write abc file
    # write make file
    # convert file to midi
    # sing it out
    # reference -= 24
    write_abc(text, notes, durs, M=M, L=L, Q=Q, K=K, reference=reference)
    conf_text = '$ESPEAK_VOICE = "{}";\n'.format(lang)
    conf_text += '$ESPEAK_TRANSPOSE = {};'.format(transpose)
    if effect == 'flint':
        conf_text += "\ndo 'extravoices/flite.inc';"
    elif effect == 'tremolo':
        conf_text += "\ndo 'extravoices/tremolo.inc';"
    elif effect == 'melt':
        conf_text += "\ndo 'extravoices/melt.inc';"
    elif effect:
        raise ValueError('effect not understood')
    with open(ECANTORIXCACHE + '/achant.conf', 'w') as f:
        f.write(conf_text)
    # write conf file
    try:
        subprocess.run(
            [
                'cp',
                f'{ECANTORIXDIR}/Makefile',
                f'{ECANTORIXCACHE}/Makefile'
            ],
            check=True,
        )
        subprocess.run(['make', '-C', ECANTORIXCACHE], check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f'Failed to build singing cache: {exc}') from exc
    wread = wavfile.read(ECANTORIXCACHE + '/achant.wav')
    assert wread[0] == 44100
    return normalize_mono(wread[1])
    # return wread[1]


def write_abc(text, notes, durs, M='4/4', L='1/4', Q=120, K='C', reference=60):
    text_ = 'X:1\n'
    text_ += 'T:Some chanting for music python package\n'
    text_ += 'M:{}\n'.format(M)
    text_ += 'L:{}\n'.format(L)
    text_ += 'Q:{}\n'.format(Q)
    text_ += 'V:1\n'
    text_ += 'K:{}\n'.format(K)
    notes = translate_to_abc(notes, durs, reference)
    text_ += notes + "\nw: " + text
    fname = ECANTORIXCACHE + "/achant.abc"
    with open(fname, 'w') as f:
        f.write(text_)


def translate_to_abc(notes, durs, reference):
    durs = [str(i).replace('-', '/') for i in durs]
    durs = [i if i != '1' else '' for i in durs]
    notes = converter.convert(notes, reference)
    return ''.join([i + j for i, j in zip(notes, durs)])


class Notes:
    def __init__(self):
        self.notes_dict = None
        self.make_dict()

    def make_dict(self):
        notes = re.findall(r'[\^=]?[a-g]', '=c^c=d^de=f^f=g^g=a^ab')
        # notes=re.findall(r'[\^]{0,1}[a-g]{1}','a^abc^cd^def^fg^g')
        notes_ = [note.upper() for note in notes]
        notes__ = [note + "," for note in notes_]
        notes___ = [note + "," for note in notes__]
        notes____ = [note + "," for note in notes___]
        notes_u = [note + "'" for note in notes]
        notes__u = [note + "'" for note in notes_u]
        notes___u = [note + "'" for note in notes__u]
        notes_all = notes____ + notes___ + notes__ + notes_ + notes + \
            notes_u + notes__u + notes___u
        self.notes_dict = dict([(i, j) for i, j in zip(range(12, 97),
                                                       notes_all)])

    def convert(self, notes, reference):
        if 'notes_dict' not in dir(self):
            self.make_dict()
        notes_ = [reference + note for note in notes]
        notes__ = [self.notes_dict[note] for note in notes_]
        return notes__


converter = Notes()

if __name__ == '__main__':
    narray = sing()
    logging.info("finished")
