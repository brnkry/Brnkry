// Dialogue timeline. who: S = shaun_73 (the dumb one, left), B = ben_soir4 (the smart one, right).
// Each word: [display text, start time]. Ben's lines and most of Shaun's come from pocketsphinx (align_chunks.py);
// Shaun's chipmunk voice failed on a few phrases, those were timed by hand from voiced runs + the source video's reveals.
window.LINES=[
 {id:'s0',em:[5, 6, 7],who:'S',likes:'12.2K',w:[['Why',.08],['did',.25],['they',.4],['name',.55],['it',.8],["'world",1.22],["war",1.5],["1'?",1.7],['Did',1.97],['they',2.36],['already',2.69],['know',2.98],['there',3.18],['were',3.29],['going',3.36],['to',3.51],['be',3.58],['more?',3.73]],end:4.3},
 {id:'b1a',who:'B',likes:'',em:[9],w:[['Actually,',5.16],['the',5.56],['name',5.64],["'first",5.87],['world',6.19],["war'",6.4],['only',7.08],['appeared',7.33],['in',7.63],['1939,',7.71],['when',8.56],['the',8.67],['second',8.73],['world',9.02],['war',9.2],['started.',9.36]],end:9.95},
 {id:'b1b',who:'B',likes:'2,726',em:[8,9,10],w:[['Before',10.11],['then,',10.39],['people',10.9],['simply',11.13],['referred',11.39],['to',11.7],['it',11.8],['as',11.88],["'the",12.49],['great',12.6],["war'.",12.94]],end:13.7},
 {id:'s2',em:[8],who:'S',likes:'9,013',w:[['Wow.',14.5],['Personally',14.96],['I',15.69],["don't",15.76],['think',15.98],['there',16.13],['was',16.22],['anything',16.35],['great',16.68],['about',16.96],['it',17.28],['at',17.36],['all.',17.5]],end:18.0},
 {id:'b3',em:[0, 4, 12],who:'B',likes:'1,493',w:[['Great',19.9],["doesn't",20.27],['necessarily',20.51],['mean',21.01],['good.',21.24],['Great',21.92],['in',22.1],['this',22.19],['case',22.32],['refers',22.59],['to',22.93],['the',23.01],['scale',23.08],['of',23.42],['the',23.49],['war.',23.56]],end:24.4},
 {id:'s4',em:[5, 6],who:'S',likes:'7,289',w:[['idk',25.35],['i',26.0],['think',26.31],["it's",26.52],['kinda',26.66],['messed',26.94],['up',27.23],['that',27.39],['they',27.67],['called',27.79],['it',28.07],['that',28.24]],end:28.8},
 {id:'b5',em:[5],who:'B',likes:'1,222',w:[['Well',30.72],['what',30.87],['would',31.04],['you',31.14],['have',31.28],['called',31.4],['it',31.74],['then?',32.2]],end:32.9},
 {id:'s6',em:[5, 6, 7],who:'S',likes:'14.8K',w:[['something',33.46],['negative',33.87],['like',34.6],['maybe',34.77],['the',35.05],['big',35.14],['bad',35.36],['war',35.65]],end:36.1},
 {id:'b7',em:[12, 13],who:'B',likes:'966',w:[['Are',37.95],['you',38.02],['serious?',38.12],["'The",38.77],['big',39.21],['bad',39.4],["war'",39.71],['makes',40.39],['it',40.55],['sound',40.61],['like',40.8],['a',40.9],['fairy',40.94],['tale',41.2],['for',41.37],['children.',41.45]],end:42.6},
 {id:'s8',em:[0, 1, 9, 11],who:'S',likes:'11.6K',w:[['4',43.2],['billion',43.6],['people',44.07],['died',44.41],['bro.',44.75],['It',45.11],["doesn't",45.23],['get',45.46],['much',45.64],['bigger',45.83],['and',46.16],['badder',46.4],['than',46.85],['that.',47.25]],end:48.0},
 {id:'b9',em:[0, 1],who:'B',likes:'488',w:[['40',48.48],['million',48.75],['people',49.02],['died',49.26],['in',49.49],['world',49.56],['war',49.78],['one.',49.92],['Where',50.16],['on',50.69],['earth',50.77],['did',51.05],['you',51.15],['get',51.23],['those',51.34],['numbers',51.51],['from?',51.79]],end:53.9},
 {id:'s10',em:[5, 6],who:'S',likes:'15.1K',w:[['I',54.31],['made',54.46],['them',54.65],['up',54.81],['for',54.96],['dramatic',55.04],['effect',55.49]],end:56.3}
];
// Meme cut-ins of the source video (their sounds stay in the original audio track)
window.MEMES={he:[18.3,19.8],roar:[28.85,30.35],sour:[36.35,37.65]};
window.DUR=57.5;
window.EPISODE='EPISODE 01'; // text the neon sign switches to
