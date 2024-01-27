Kuva-annotaattori

Ohjelman idea: lataa kuvia ohjelmaan, tee annotaatioita, luo dataset.
Voit ladata graafisen käyttöliittymän avulla ohjelmaan kuvia, ja tehdä niihin annotaatioita.
Kuvat ja annotaatiot voi tallentaa torchvisionin avulla tehtyyn datasettiin, ja voit selata tallennettuja
kuvia ja annotaatioita edestakaisin.


Picture.py -tiedostosta löytyy luokka Picture (QWidgetin alaluokka). Picture yhdistää kuvan ja sen tämän annotaatiot. Picturella on esimerkiksi self.annotations (lista Annotation-olioita) ja self.picture (QPixmap-olio).

Annotation.py -tiedostosta löytyy luokka Annotation (QWidgetin alaluokka). Annotation yhdistää QRect-olion ja annotaation nimen. Annotaatiolla on self.name (annotaation nimi) ja self.rectangle (annotaation rajaava QRect-olio).

Tiedostossa dataset.py määritellään luokka ImageDataset. ImageDatasetin self.image on lista Picture-olioita ja self.annotations on lista kaikkien Picture-olioiden annotaatioista. Metodi __len_ palauttaa listan self.annotations pituuden. Metodi __getitem__  palauttaa tietyn annotaation rajaaman alueen annotaation kuvasta ja annotaation nimen.

Ohjelman käynnistää main.py. 

Ohjelman ehkä tärkein tiedosto on mainwindow.py, jossa on QMainWindowin ala luokka Mainwindow. __init__ metodissa muun muassa luodaan flagit self.is_drawing (varmistaa, että mouseMoveEvent tekee jotain vain kun hiiri on pohjassa), self.first_image (varmistaa, että annotaatioita ei pysty luoda ennen kuin kuva on ladattu) ja self.toinenflagi (mahdollistaa musiikin pysäyttämisen). 

Metodi init_ui muun muassa asettaa ikkunan geometrian ja luo QLabelin, johon avatut kuvat liitetään. Tässä metodissa määritetään myös taustan väri. Metodissa avataan kelvoton kuva. Tämän avulla sain avattua tyhjän kuvan, jolloin ikkunan avautuessa ohjelma näyttää “tyhjältä”.

Metodi init_buttons luo ikkunan napit. Jokainen napeista kutsuu tiettyä metodia, joka saa aikaan halutun asian.

Metodi removeannotation (yhdistetty Hups-nappiin) poistaa nykyisen kuvan viimeisimmän annotaation yksinkertaisesti poistamalla sen Picture-olion self.annotations -listasta kutsumalla Picture-olion removeannotation metodia.

Metodin paintEvent tarkoitus on piirtää annotaatiot. Piirtäminen tapahtuu QPainter-oliolla, joka piirtää avatun kuvan kopioon. Tämä järjestely on tehty sen takia, että alun perin annotaatiot piirrettiin suoraan avattuun kuvaan, mutta tällöin 
vanhat annotaatiot eivät jostakin syystä poistuneet (esim. aina kun hiirtä veti, piirtyi uusi suorakaide, mutta vanha suorakaide ei poistunut). Metodissa piirretään erikseen self.annotation_rect (suorakaide, jota vasta luodaan, hiiri pohjassa ja hiirtä vedetään) ja kuvan tallennetut annotaatiot. PaintEventiä ilmeisesti kutsutaan aina kun self.picture_labelissa (QLabel) tapahtuu jokin muutos, jolloin QPainter piirtää annotaatiot uudestaan.

Metodi mousePress aktivoituu kun hiirtä klikataan. Metodi tarkistaa flagin self.first_image (ei tee mitään ellei ensimmäistä kuvaa olla ladattu).
Metodi asettaa flagin self.is_drawing arvoksi True, mikä vaikuttaa mouseMoveEventin toimintaan. Metodi myös tallentaa muuttujaan self.start_pos kursorin nykyiset koordinaatit.

Metodin mouseMoveEvent idea on luoda QRect suorakaide jo silloin kun hiirtä raahataan ja annotaatiota ollaan vasta luomassa. Metodi tarkistaa flagin self.first_image (ei tee mitään ellei ensimmäistä kuvaa olla ladattu). Tämän jälkeen metodi tarkistaa flagin self.is_drawing. Jos sen arvo on True, hiiri on pohjassa ja asetetaan QRect-olio muuttujaan self.annotation_rect. 

Metodin mouseReleaseEvent idea on luoda suorakaiteesta self.annotation_rect annotaatio. Metodi tarkistaa flagin self.first_image (ei tee mitään ellei ensimmäistä kuvaa olla ladattu). Tämän jälkeen flagin self.is_drawing arvoksi asetetaan False merkiksi siitä, että self.annotation_rectiä ei tarvitse enää päivittää mouseMoveEventissä. Tämän jälkeen avataan QInputDialog, jossa annotaatio nimetään. Jos annotaation nimi pystytään lukemaan, 
self.annotation_rectistä ja annotaation nimestä luodaan Annotation-olio, joka lisätään avatun kuvan (Picture()) self.annotations -listaan. Self.annotation_rectin arvoksi asetetaan None syystä, jotta paintEvent ei maalaa samaa suorakaidetta kahdesti (en tiedä onko tällä mitään väliä).

Metodissa load_image (yhdistettu Tuo-nappiin) ohjelmaan tuodaan uusi kuva. Metodi avaa QInputDialogin, johon syötetään seuraavan kuvan tiedostosijainti. Jos dialogiin syötetty teksti voidaan lukea, asetetaan self.imagenamen arvoksi syötetty teksti ja kutsutaan funktiota update_image. Flagi self.first_image asetetaan Trueksi, merkiksi siitä, että ainakin ensimmäinen kuva on ladattu ohjelmaan.

Metodi update_image asettaa muuttujan self.wholeimage arvoksi uuden Picture-olion, jonka parametrinä toimii self.imagename (uuden kuvan tiedostosijainti). self.picture_labeliin asetetaan uuden Picture-olion QPixmap-olio. 

Metodi save_image (yhdistetty Tallenna-nappiin) tallentaa nykyisen kuvan ja sen annotaatiot self.kuvat-listaan. Metodi tarkistaa flagin self.first_image (ei tee mitään ellei ensimmäistä kuvaa olla ladattu). Metodi tutkii onko nykyinen kuva jo tallennettu ja jos on, niin kuvan annotaatiot päivitetään vastaamaan haluttuja annotaatioita. Jos taas nykyistä kuvaa ei olla vielä tallennettu, kuva tallennetaan self.kuvat-listaan. Sitä päivitetäänkö listan jäsentä, vai lisätäänkö uusi jäsen hallitaan flagin “flag” avulla.

Metodeilla next_picture ja previous_picture selataan tallennettuja kuvia. Keskiössä on self.indeksi, jonka avulla seurataan, missä self.kuvat jäsenessä mennään (mikä jäsenistä on tällä hetkellä auki).Metodit tutkivat onko yhtäkään kuvaa tallennettu, ja jos on, next_picture tutkii onko nyt näkyvillä oleva kuva viimeinen tallennettu kuva. Jos ei ole, self.indeksin avulla metodi päivittää self.wholeimagen ja self.picture_labelin vastaamaan listan seuraavaa kuvaa (avaa seuraavan kuvan). Previous_picture taas tutkii onko nykyinen kuva ensimmäinen tallennettu kuva (mitään ei tapahdu jos on).

Metodin set_image avulla voidaan ladata ohjelmaan kuva ilman että tiedostosijainti syötetään QInputDialogiin. Voisi olla kätevä metodi testauksessa.

Metodi playsound soittaa musiikkia tai lopettaa musiikin soiton riippuen siitä soiko musiikki jo valmiiski. 

Metodi create_dataset (yhdistetty “Dataset”-nappiin) luo Mainwindowin listasta self.kuvat ImageDataset-olion ja tallentaa sen muuttujaan self.dataset.

Metodi lopeta() sulkee ohjelman komennolla self.close()



Ohjeita:
Asenna torchvision ja PyQt6.     HUOM! PROJEKTIN TORCHVISION-OSUUS EI TOIMI
Pycharm -> file -> settings -> project:[projecti] -> pluskuvake(install) -> etsi torchvision/PyQt6 -> install package

Käyttöohje:
Aja main.py. 
Tämän jälkeen avautuvassa ikkunassa on painettava nappia “Tuo”. Tämä nappi avaa kohdan, johon voit syöttää kuvan tiedostosijainnin. Haluttu kuva avautuu, ja hiirtä klikkaamalla ja vetämällä voit tehdä annotaatioita kuvaan. 
Nappi “Hups” poistaa viimeisimmän annotaation kuvasta. Kun haluttu annotaatio on rajattu, ohjelma kysyy annotaation nimeä. 
Kun kuva on annotoitu, sen voi tallentaa ohjelmaan “Tallenna”-napista. 
Tämän jälkeen voit ladata uuden kuvan “Tuo”-napin avulla. 
Tallennettuja kuvia ja niiden annotaatioita voi selata napeilla “Seuraava” ja “Edellinen”. 
Kun kaikki halutut kuvat on annotoitu ja tallennettu “Dataset”-napista voi luoda PyTorch datasetin kuvista ja niiden annotaatioista.
Jos ohjelma ei tunnu stimuloivan käyttäjää tarpeeksi “Musiikkia”-nappia painamalla voi laittaa musiikkia soimaan (nappia painamalla Never gonna give you up alkaa soida). 
Nappi “Poistu” sulkee ohjelman.
