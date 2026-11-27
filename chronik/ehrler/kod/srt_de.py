# German SRT (long and short), same timing as the English SRT; the radio message as its own cues
import sys
sys.path.insert(0, '/home/user/Brnkry/chronik/ehrler/kod'); sys.path.insert(0, '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/ehrler/kod')
import srt_en, ee, ks
srt_en.RADIO = [(0.25, 3.45, 'Funkspruch: „Theo, Heinrich hier. Habe zwei Bomber abgeschossen.“'), (3.5, 5.7, '„Munition ist alle. Ich ramme jetzt.“'),
                (5.85, 8.7, '„Auf Wiedersehen, wir sehen uns in Walhalla.“')]
def de(WD): return [' '.join(w[0] for w in s).replace('Me zweihundertzweiundsechzig', 'Me 262') for s in srt_en.sents(WD)]
U = '/home/user/Brnkry/chronik/ehrler/untertitel/'
srt_en.build(ee.WD, de(ee.WD), [ee.R1, ee.R2], U + 'captions.de.srt')
srt_en.build(ks.WD, de(ks.WD), [ks.R1], U + 'short.de.srt')
