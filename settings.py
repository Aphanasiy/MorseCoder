import yaml

class Settings:
    FREQ = 440

    SAMPLE_RATE = 44100

    T_DOT = 0.1
    T_DASH = 0.3
    T_DASHDOTGAP = 0.15
    T_LGAP = 0.5
    T_WGAP = 2

    L_APP = "en"
    L_MORSE = "en"

    def __init__(self, lang="en"):
        with open("settings.yaml", 'r') as stream:
            s = yaml.safe_load(stream)
        self.SPEED = s["SPEED"]
        self.FREQ = s["FREQ"]
        self.SAMPLE_RATE = s["SAMPLE_RATE"]
        self.T_DOT = s["T_DOT"] / self.SPEED
        self.T_DASH = s["T_DASH"] / self.SPEED
        self.T_DASHDOTGAP = s["T_DASHDOTGAP"] / self.SPEED
        self.T_LGAP = s["T_LETTERGAP"] / self.SPEED
        self.T_WGAP = s["T_WORDGAP"] / self.SPEED
        self.L_APP = s["APP_LOCALE"]
        self.L_MORSE = s["MORSE_LOCALE"]



class Morse:
    def __init__(self, lang):
        with open("morse.yaml", 'r') as stream:
            morse = yaml.safe_load(stream)
            self.MORSE = morse[lang]
    def items(self):
        return self.MORSE.items()

DEFAULT_LOCALE = "en"

class L10N:
    DEFAULT = "en"
    
    def __init__(self, locale=DEFAULT_LOCALE):
        self._localization = dict()
        with open("l10n.yaml", 'r') as stream:
            s = yaml.safe_load(stream)
            for k, v in s.items():
                self._localization[k] = v
        self.set_app_locale(locale)

    def set_app_locale(self, locale):
        self.__dict__.update(self._localization[locale])
    
                
        
        