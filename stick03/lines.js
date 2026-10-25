// Episode 03: "bogos binted" (a text thread, 8 s). A = the guy asking about photos (left, turns alien at 3.4 s),
// B = the alien in a bad human disguise (right, turns human). English words from pocketsphinx, alien words by hand.
window.USERS={A:{name:'Me',color:'#7AC943',age:'',side:'L'},B:{name:'Unknown number',color:'#9B7BD9',age:'',side:'R'}};
window.LINES=[
 {id:'a1',who:'A',em:[7,8],w:[['Hey,',.0],['just',.23],['wondering',.42],['if',.67],['you',.76],['got',.82],['your',.95],['photos',1.04],['printed?',1.37]],end:1.7},
 {id:'b1',who:'B',em:[0,1],w:[['bogos',1.9],['binted?',2.18]],end:2.4},
 {id:'a2',who:'A',em:[0],w:[['What',2.82]],end:3.05},
 {id:'a3',who:'A',em:[6,7,8],w:[['Zinky',3.48],['zoogle,',3.62],['zeekybooble',3.92],['beeble',4.5],['meep.',4.75],['Forp',4.98],['Bogos',5.16],['Binted?',5.42]],end:5.75},
 {id:'b2',who:'B',em:[0,1],w:[['Photos',5.97],['printed',6.3]],end:6.6},
 {id:'a4',who:'A',em:[0],w:[['Vorp?',6.9]],end:7.1,hideAt:7.55}
];
window.MEMES={};
window.SWAP=3.38;  // the moment the languages flip
window.EPISODE='EPISODE 03';
window.DUR=8.3;
