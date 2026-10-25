// Episode 05 (second clip of video4, 9.0..23.4 s of the source): guessing game with an AI chatbot.
// H = the human (left), A = Gemini (right, the AI chatbot). Times from pocketsphinx + energy.
window.USERS={H:{name:'You',color:'#2C8CD6',side:'L',age:''},A:{name:'Gemini',color:'#7B8CF0',side:'R',age:''}};
window.LINES=[
 {id:'h1',who:'H',em:[3],w:[['Tell',0],['me',.22],['a',.34],['color',.37],['and',.67],["I'll",.76],['try',.88],['to',1.01],['guess',1.08],['it',1.25],['😄',1.36]],end:1.5},
 {id:'a1',who:'A',em:[5],w:[['Perfect!',2.71],['I',3.49],['chose',3.59],['the',3.93],['color',4.04],['red.',4.42],['Try',4.84],['to',5.13],['guess',5.25],['it',5.56],['✦',5.62]],end:5.75},
 {id:'h2',who:'H',em:[0],w:[['Red',6.6],['😄',6.75]],end:6.9},
 {id:'a2',who:'A',em:[0,6,7,8],w:[['Yes,',8.2],['that',8.6],['was',8.78],['it!',9.03],['How',9.5],['did',9.63],['you',9.82],['guess',9.96],['it?',10.1],['😮',10.2]],end:10.4}
];
window.MEMES={stare:[11.0,14.4]};
window.EPISODE='EPISODE 05';
window.DUR=14.4;
