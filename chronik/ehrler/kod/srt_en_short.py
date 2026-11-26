# English SRT for the Ehrler Shorts / Reel (radio message, then the short narration)
import sys
sys.path.insert(0, '/home/user/Brnkry/chronik/ehrler/kod'); sys.path.insert(0, '/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/ehrler/kod')
import srt_en, ks
EN = ["Those are said to have been Heinrich Ehrler's last words, radioed in April 1945.",
"Ehrler was one of the Luftwaffe's most successful fighter pilots.",
"With Jagdgeschwader 5 he flew in the far north, over Lapland, the Barents Sea and the Murmansk front, in snowstorms and polar night.",
"He was credited with almost 200 aerial victories, wore the Knight's Cross with Oak Leaves and became commander of his wing.",
"But on 12 November 1944 everything changed.",
"British Lancaster bombers attacked the battleship Tirpitz off Tromsø.",
"Their Tallboy bombs, each over five tons, hit; the Tirpitz capsized and about a thousand sailors died.",
"The fighters from nearby Bardufoss came too late.",
"Warnings arrived late or not at all, communications failed.",
"The leadership needed someone to blame, and they found him in Ehrler.",
"A court-martial sentenced him to three years in prison and took away his command.",
"The sentence was suspended so that he could fly again.",
"In February 1945 he joined Jagdgeschwader 7, the world's first jet fighter unit, flying the Messerschmitt Me 262.",
"In April 1945 he took off against a large American bomber formation.",
"According to the reports he shot down two bombers.",
"Then his ammunition was gone.",
"Whether he really rammed the third bomber is still disputed today.",
"Only this is certain:",
"His aircraft crashed near Stendal.",
"Heinrich Ehrler was 27 years old.",
"A little over a month later the war in Europe was over."]
srt_en.build(ks.WD, EN, [ks.R1], '/home/user/Brnkry/chronik/ehrler/untertitel/short.en_US.srt')
