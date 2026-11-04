# Wainwright 9:16 cover (Chronicle of Power) in the cover9 layout: w05, gaunt after three years as a prisoner, no heroic framing
from cover9 import *
if __name__ == '__main__':
    os.makedirs(B + 'thumbs', exist_ok=True)
    cover('w05', 524, 128, 1.29, ('C', 'P'), 'JONATHAN', 'WAINWRIGHT', 'FORCED TO SURRENDER IN 1942', B + 'thumbs/EN_Wainwright_Surrendered.jpg'); print('ok')
