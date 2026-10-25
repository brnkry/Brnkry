// Episode 06 (third clip of video4, 23.95..30.65 s of the source): "What's the movie name?" -> "ready or not" -> "Ready".
// S = Samara (left), A = hi i'm ash (right). Times from pocketsphinx.
window.USERS={S:{name:'Samara',color:'#FF8FC8',side:'L',age:'9h'},A:{name:"hi i'm ash",color:'#6B5A50',side:'R',age:'9h'}};
window.LINES=[
 {id:'s1',who:'S',likes:'42',em:[2,3],w:[["What's",0.05],['the',.35],['movie',.42],['name?',.81]],end:1.1},
 {id:'a1',who:'A',likes:'51',em:[0,1,2],w:[['ready',2.3],['or',2.6],['not',2.67]],end:2.85},
 {id:'s2',who:'S',likes:'',em:[0],w:[['Ready',4.59]],end:4.9}
];
window.MEMES={};
window.EPISODE='EPISODE 06';
window.DUR=6.6;
