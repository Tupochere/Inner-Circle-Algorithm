import pandas as pd

def is_swing_high(df, i):
    return df['high'][i] > df['high'][i - 1] and df['high'][i] > df['high'][i + 1]

def is_swing_low(df, i):
    return df['low'][i] < df['low'][i - 1] and df['low'][i] < df['low'][i + 1]

def detect_market_structure(df):
    structure = []
    last_swing_high = None
    last_swing_low = None
    last_direction = None

    for i in range(1, len(df) - 1):
        swing_high = is_swing_high(df, i)
        swing_low = is_swing_low(df, i)

        if swing_high:
            curr_high = df['high'][i]
            if last_swing_high is not None and curr_high > last_swing_high:
                structure.append((df['timestamp'][i], 'HH'))
                if last_direction == 'down':
                    structure.append((df['timestamp'][i], 'CHoCH'))
                else:
                    structure.append((df['timestamp'][i], 'BOS'))
                last_direction = 'up'
            last_swing_high = curr_high

        if swing_low:
            curr_low = df['low'][i]
            if last_swing_low is not None and curr_low < last_swing_low:
                structure.append((df['timestamp'][i], 'LL'))
                if last_direction == 'up':
                    structure.append((df['timestamp'][i], 'CHoCH'))
                else:
                    structure.append((df['timestamp'][i], 'BOS'))
                last_direction = 'down'
            last_swing_low = curr_low

    return structure
