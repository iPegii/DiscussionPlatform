# Keskustelualusta

Sovellus on löydettävissä [Herokusta](https://tsoha-discussionplatform.herokuapp.com/)  
  
Tällä hetkellä sovelluksessa toimii vain kirjautuminen ja uloskirjautuminen. Sekä toimimaton näkymä viestien lähettämisestä.


## Osiot

Käyttäjä:
* Rekisteröi ja kirjautuu
* Liittyy huoneisiin
* Lähettää viestejä

Ylläpitäjä:
* Poistaa viestejä

Huone:
* Viestejä
* Sisältää liittyineitä käyttäjiä ja ylläpitäjiä

## Ominaisuuksia

Sovelluksen ominaisuudet:
* Huoneissa on tavallisia käyttäjiä ja ylläpitäjiä
* Käyttäjät voivat liittyä huoneisiin, lähettää viestejä ja tykätä viesteistä
* Viesteissä näkyy lähettäjän nimi, aika ja tykkäykset
* Huoneiden ylläpitäjät voivat poistaa viestejä

Mahdolliset parannukset:
* Ylläpitäjät voivat antaa käyttäjille väliaikaisia tai pysyviä estoja
* Viestejä voidaan myös miinustaa
* Käyttäjä voi poistaa ja muokata viestejä

## Mahdolliset taulut

Taulut
* Käyttäjät(id,nimi, käyttäjätunnus, salasana)
* Viesti(id,teksti,aika,käyttäjä,tykkäykset)
* Huoneet(id, huoneen nimi, huoneen id, salasana)
* Huoneen_viestit(id, huoneen id, viesti)
* Huoneen_käyttäjät(id,huone id, käyttäjä id, oikeudet)
