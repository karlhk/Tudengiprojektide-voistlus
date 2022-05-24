# Personal
GRAAFIKU KOOSTAMISE JUHEND

ESMANE VÄIKE TABEL	

•	Kuu: numbri kujul (“10”, mitte “oktoober”)
•	Aasta: numbri kujul (“2020”)
•	Pikki shifte päevas: mitu inimest peab osakonnas 24h vahetuses olema (“2”)
•	Lühikesi shifte päevas: mitu inimest peab osakonnas 12h vahetuses olema (“1”)

SUUR TABEL
•	Eesnimi, perenimi, telefon, email, aadress: võib jääda tühjaks
•	Soovipäevad: numbrid eralda komadega, võimalik sisestada vahemikke (“1, 3-5, 9, 19, 23-28”)
•	Puhkus: võib jääda tühjaks (“1-7, 23-26”)
•	Vahetuse pikkused: valikus 8, 10, 12, 24. Eraldada komadega (“12,24”)
•	Üle/alatunnid: info eelneva kuu lõpul olevatest üle- ja alatundidest. Kui positiivne number siis alatunnid, kui negatiivne siis ületunnid. 	

TULP “MUU”
SISESTA JUTUMÄRKIDES KÄSKLUS, KÄSKLUSED ERALDA SEMIKOOLONIGA ;
•	“võiks koos: [NIMI]” - programm määrab töötaja võimalusel tööle koos [NIMI]-ga
•	“peab koos: [NIMI]” - programm määrab töötaja alati tööle koos [NIMI]-ga
•	“ei tohi koos: [NIMI]” - programm ei määra töötajat tööle koos [NIMI]-ga
•	“võiks paus: [NR]” - programm jätab võimalusel vähemalt [NR] päeva kahe 24h shifti vahele. Kui ei sisesta, siis jätab võimalusel kaks vaba päeva. 
•	“peab paus: [NR]” - programm jätab alati vähemalt [NR] päeva kahe 24h shifti vahele (default 1)
•	“argipäeviti: [NR]” - programm määrab talle ainult tööpäevadel [NR]-tunnise shifti, ei arvesta teda graafiku muude vahetuste katmisel
•	“nädala kaupa: [NR]” - programm määrab talle vahetusi 3-4 ülepäevaste plokkide kaupa, jättes [NR] päeva kahe ploki vahele
•	“koolitus: [KUUPÄEVAD]/[NR]” - programm määrab töötajale [KUUPÄEVAD] koolituspäevadeks ning arvestab normtundidest [NR] tundi maha iga koolituspäeva kohta
•	“eelistab: [NR]” - programm määrab talle eelisjärjekorras [NR]-tunniseid shifte (kasutada, kui töötaja teeb vajadusel erineva pikkusega shifte, kuid eelistab kindlat pikkust)

