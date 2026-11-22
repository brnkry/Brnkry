# narration paragraphs = script rows (senaryo.md); first words of each row
STARTS = [(1,"Yasuo, ağbisini"),(3,"Yone, onura"),(4,"Kardeşi Yasuo ise"),(5,"Yaşlı Souma, Yasuo'yu"),(6,"Bir tohum sadece"),
 (7,"Ama Yone'nin içinde"),(8,"Yone çift kılıçla"),(9,"İyonya'ya savaş"),(10,"Bir gece Yaşlı"),(11,"Bu Yone'yi"),(12,"Yasuo peşine"),
 (13,"Yarın ilk ışıkla"),(14,"Onu buldu."),(15,"Ama ölüm bir son"),(16,"Sonra gürleyen"),(17,"Yone tek kelime"),(18,"Öfke onu"),
 (19,"Yeni bir karanlık"),(20,"Yone kendine"),(21,"Yüzünde, azakananın"),(22,"Bu yaratıklar"),(23,"Bir gece, on üç"),(24,"Çocuk koşarken"),
 (25,"Korkman gereken"),(26,"Sisin içinde"),(27,"Yone o adı"),(28,"Çocuk sordu:"),(29,"Sadece senin"),(30,"Çocuk bunun"),
 (31,"Sevdiklerimiz, bizi"),(32,"Sonra karanlığa"),(33,"Azakanaların peşinde"),(35,"Yone, Yasuo'yu öldürmedi."),(36,"Yone hâlâ"),
 (37,"Peki o kahkaha"),(38,"Ama bu hikayede")]
def rows(text):
    out=[]; pos=[text.index(s) for _,s in STARTS]+[len(text)]
    for k,(r,_) in enumerate(STARTS): out.append((r,text[pos[k]:pos[k+1]].strip()))
    return out
