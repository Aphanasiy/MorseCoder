import numpy as np

def _dot(st):
    t = np.linspace(0, st.T_DOT, int(st.T_DOT * st.SAMPLE_RATE), False)
    return np.sin(st.FREQ * t * 2 * np.pi)

def _dash(st):
    t = np.linspace(0, st.T_DASH, int(st.T_DASH * st.SAMPLE_RATE), False)
    return np.sin(st.FREQ * t * 2 * np.pi)

def _ddgap(st):
    return np.zeros(int(st.T_DASHDOTGAP * st.SAMPLE_RATE))

def _lgap(st):
    return np.zeros(int(st.T_LGAP * st.SAMPLE_RATE))

def _wgap(st):
    return np.zeros(int(st.T_WGAP * st.SAMPLE_RATE))

def _generate(schema, st):
    stack = [_ddgap(st)]
    for s in schema:
        if s == '.':
            stack.append(_dot(st))
        elif s == '-':
            stack.append(_dash(st))
        elif s == " ":
            stack.append(_lgap(st))
        stack.append(_ddgap(st))
    return np.hstack(stack)

def generate(schema, settings):
    audio = _generate(schema, settings)
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    return audio

