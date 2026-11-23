import math, struct, wave
from pathlib import Path

SAMPLE_RATE = 44100
EVENTS = [
    (0.00, 0.50, 60, 90),
    (0.50, 0.50, 64, 105),
    (1.00, 0.75, 67, 80),
]

def midi_to_freq(note):
    return 440.0 * 2 ** ((note - 69) / 12)

def make_audio(events, filename):
    length = max(start + duration for start, duration, _, _ in events)
    samples = [0.0] * int(length * SAMPLE_RATE)

    for start, duration, note, velocity in events:
        f = midi_to_freq(note)
        begin = int(start * SAMPLE_RATE)
        count = int(duration * SAMPLE_RATE)
        for j in range(count):
            # Short fade-in and fade-out to reduce clicks.
            attack = min(1.0, j / max(1, int(0.01 * SAMPLE_RATE)))
            release = min(1.0, (count - j - 1) / max(1, int(0.02 * SAMPLE_RATE)))
            envelope = max(0.0, min(attack, release))
            value = 0.65 * (velocity / 127) * envelope * math.sin(2 * math.pi * f * j / SAMPLE_RATE)
            if begin + j < len(samples):
                samples[begin + j] += value
                
    pcm = [max(-32768, min(32767, int(v * 32767))) for v in samples]
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2) # 16-bit PCM
        w.setframerate(SAMPLE_RATE)
        w.writeframes(struct.pack('<' + 'h' * len(pcm), *pcm))
    return len(pcm)

n = make_audio(EVENTS, 'midi_demo.wav')
print('Samples:', n)
print('Duration:', n / SAMPLE_RATE, 'seconds')
print('WAV bytes:', Path('midi_demo.wav').stat().st_size)
for _, _, note, velocity in EVENTS:
    print(note, velocity, round(midi_to_freq(note), 2), 'Hz')
