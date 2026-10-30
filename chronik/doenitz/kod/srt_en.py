# English subtitle track for the German Dönitz short, timed to the German words (words.json): one cue per German clause
import json, sys
B = sys.argv[1] + '/'; W_ = json.load(open(B + 'words.json'))
CUES = [   # (German clause, English)
 ("Er war Hitlers Nachfolger,", "He was Hitler's successor,"),
 ("und achtzehn Jahre nach dem Krieg stand er vor einer Schulklasse.", "and eighteen years after the war he stood in front of a school class."),
 ("Sein Name war Karl Dönitz.", "His name was Karl Dönitz."),
 ("Als Befehlshaber der U-Boote", "As commander of the U-boats"),
 ("schickte er Zehntausende junge Männer in den Atlantik,", "he sent tens of thousands of young men into the Atlantic,"),
 ("die meisten kehrten nie zurück.", "and most of them never came back."),
 ("In seinem Testament ernannte Hitler ihn zum Reichspräsidenten.", "In his testament, Hitler named him Reich President."),
 ("Von Flensburg-Mürwik aus regierte Dönitz noch drei Wochen lang", "From Flensburg-Mürwik, Dönitz governed for three more weeks"),
 ("ein Reich, das es kaum noch gab.", "a Reich that barely existed anymore."),
 ("Am 23. Mai 1945 rückten britische Soldaten an.", "On 23 May 1945, British soldiers moved in."),
 ("Dönitz und seine gesamte Regierung wurden verhaftet.", "Dönitz and his entire government were arrested."),
 ("In Nürnberg verurteilte man ihn zu zehn Jahren Haft,", "At Nuremberg he was sentenced to ten years in prison,"),
 ("die er in Spandau bis zum letzten Tag absaß.", "which he served in Spandau to the very last day."),
 ("Im Januar 1963 kam er an ein Gymnasium in Geesthacht.", "In January 1963 he came to a grammar school in Geesthacht."),
 ("Organisiert hatte den Vortrag der Schülersprecher Uwe Barschel,", "The talk had been organised by the head boy, Uwe Barschel,"),
 ("später Ministerpräsident von Schleswig-Holstein.", "later Minister-President of Schleswig-Holstein."),
 ("Dönitz sprach vor Schülern der Oberstufe über den Krieg,", "Dönitz spoke to senior students about the war"),
 ("ohne ein Wort der Kritik oder der Reue.", "without a word of criticism or remorse."),
 ("Lehrer und Schüler applaudierten,", "Teachers and students applauded,"),
 ("die Lokalzeitung lobte den Abend.", "and the local paper praised the evening."),
 ("Dann berichteten Spiegel, Zeit und sogar Le Monde,", "Then Der Spiegel, Die Zeit and even Le Monde reported on it,"),
 ("und ganz Deutschland war empört.", "and all of Germany was outraged."),
 ("Der Schulleiter geriet unter Druck", "The headmaster came under pressure"),
 ("und nahm sich kurz darauf das Leben.", "and took his own life shortly afterwards."),
 ("Dönitz selbst starb 1980", "Dönitz himself died in 1980"),
 ("und verteidigte seine Rolle bis zuletzt.", "and defended his role to the very end."),
]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return '%02d:%02d:%06.3f' % (h, m, s)
i = 0; out = []
for k, (de, en) in enumerate(CUES):
    n = len(de.split()); ws = W_[i:i + n]; assert [w[0] for w in ws] == de.split(), (de, [w[0] for w in ws]); i += n
    a = ws[0][1]; b = ws[-1][2] + 0.2
    if i < len(W_): b = min(b, W_[i][1] - 0.02)
    out.append('%d\n%s --> %s\n%s\n' % (k + 1, ts(a).replace('.', ','), ts(b).replace('.', ','), en))
assert i == len(W_)
open(B + 'untertitel/captions.en_US.srt', 'w').write('\n'.join(out)); print(len(out), 'cues')
