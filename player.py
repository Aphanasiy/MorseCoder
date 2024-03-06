import simpleaudio as sa
import settings
import dashdot

import random
import time
import itertools
from dataclasses import dataclass


class LetterGame:
    SETTINGS: dict

    class LetterGameRound:
        
        def __init__(self, settings, morse):
            self.Settings = settings
            self.Letter, self.Code = random.choice(morse)
            self.Audio = dashdot.generate(self.Code, self.Settings)
            self.Started = False
        
        def start(self, wait=False):
            self._play_sound()
            self.Started = True
        
        def check(self, letter, wait=False, replay=True):
            letter = letter.strip().lower()
            if (not self.Started):
                raise Exception("The game is not started")
            if (letter != self.Letter):
                if (replay):
                    self._play_sound()
                return False
            return True

        def _play_sound(self, wait=False):
            play_obj = sa.play_buffer(self.Audio, 1, 2, self.Settings.SAMPLE_RATE)
            if wait:
                play_obj.wait_done()
        
        def __repr__(self):
            return f"Round<Letter:{self.Letter}, Code:{self.Code}>"
    
    def __init__(self):
        self.SETTINGS = settings.Settings("en")
        self.MORSE = list(settings.Morse(self.SETTINGS.L_MORSE).items())
    
    def round_generator(self):
        while True:
            yield self.LetterGameRound(self.SETTINGS, self.MORSE)


class TKinterLetterGame(LetterGame):

    @dataclass
    class Stage:
        Round: LetterGame.LetterGameRound = None
        Num: int = 0
        Attempt: int = 0
        Generator = None

    def _l10n(self):
        return self.frame._l10n()

    def __init__(self, frame, rounds=5):
        super().__init__()
        self.frame = frame
        self.stage = self.Stage()
        self.stage.Generator = self.round_generator()
        self.maxRounds = rounds

    def start_round(self, force=False):
        if force:
            self.__init__(self.frame, rounds=self.maxRounds)
        if self.stage.Num == self.maxRounds:
            self.frame.unbind_keyboard()
            self.frame.bind("<Return>", self.frame.start)
            self.frame.display(self._l10n().LetterGameEndMessage)
            return
        self.frame.display(self._l10n().LetterGameStartRoundMessage.format(
            stageNum = self.stage.Num + 1
        ))
        self.stage.Round = next(self.stage.Generator)
        self.stage.Attempt = 0
        self.stage.Num += 1
        self.stage.Round.start(wait=True)
    
    def press(self, x):
        if not self.stage.Round.check(x, replay=self.stage.Attempt != 2, wait=True):
            self.stage.Attempt += 1
            self.frame.background("#522323")
            if (self.stage.Attempt == 3):
                self.frame.display(self._l10n().LetterGameFailedMessage.format(
                    currLetter = self.stage.Round.Letter, currCode = self.stage.Round.Code
                ))
                self.stage.Round.check(x, wait=True)
                return
                time.sleep(1)
                self.start_round()
            elif self.stage.Attempt < 3:
                self.frame.display(self._l10n().LetterGameWrongMessage.format(attemptNum = self.stage.Attempt + 1))
        else:
            if (self.stage.Attempt >= 3):
                self.frame.background("gray")
            else:
                self.frame.background("#407200")
            self.start_round()



class ConsoleLetterGame(LetterGame):
    
    def start(self, rounds = 5):
        for i, rnd in enumerate(itertools.islice(self.round_generator(), rounds), 1):
            print(f" === === ROUND {i} === === ")

            print("What letter is it?")
            rnd.start()
            x = input("answer: ")
            attempt = 1
            while not rnd.check(x, wait=True) and attempt <= 3:
                if (attempt == 3):
                    break
                print(f"[{attempt}/3] That's wrong. Try again")
                x = input("answer: ")
                attempt += 1
            if (attempt == 3):
                print(f"Failed. The correct answer is \"{rnd.Letter}\". It's code is \"{rnd.Code}\"")
                time.sleep(1)
            else:
                print("Correct!")
            time.sleep(0.3)
    



