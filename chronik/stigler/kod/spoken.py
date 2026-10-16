# display word -> spoken form (for syllable count)
TEXT = open(__file__.replace('spoken.py','script.txt')).read().split()
SPOKEN = {
 '20.':'zwanzigsten','1943':'neunzehnhundertdreiundvierzig','21-jährige':'einundzwanzigjährige',
 'B-17':'B siebzehn','27':'siebenundzwanzig','109.':'hundertneun','1953':'neunzehnhundertdreiundfünfzig',
 '1986':'neunzehnhundertsechsundachtzig','1990':'neunzehnhundertneunzig','2008':'zweitausendacht',
 '92':'zweiundneunzig','86.':'sechsundachtzig','Bf':'B F','„Ye':'Je','Olde':'Olde','Pub“.':'Pab',
 'Hugh':'Hju','Seething':'Siething','Charlie':'Tschali','Charles':'Tscharls',
}
