# Balck 9:16 cover (CDM) in the cover9 layout: b09, the gaunt Oberst in the field, no heroic framing
from cover9 import *
if __name__ == '__main__':
    os.makedirs(B + 'thumbs', exist_ok=True)
    cover('b09', 145, 0, 0.8, ('C', 'DM'), 'HERMANN', 'BALCK', 'LEHRER ODER TÄTER?', B + 'thumbs/DE_Balck_Lehrer_oder_Taeter.jpg'); print('ok')
