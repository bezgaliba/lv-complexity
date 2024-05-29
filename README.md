# lv-complexity
Bakalaura darba ietvaros apskatīts NLP uzdevums - teksta sarežģītības noteikšana klāt ar šī rīka izveidi, kas ir publiski pieejams saitē [sarezgitiba.lv](https://sarezgitiba.lv/)

Teksta sarežģītības noteikšana ir dabiskās valodas apstrādes nozares uzdevums, kas nosaka  rakstiska teksta leksisko, sintaktisko struktūru, lasāmības un uztveras grūtības pakāpi, ņemot vērā atdalot to trijās galvenās raksturojošās komponentes – tekstu raksturojošos kvantitatīvos rādītājus, teksta kvalitāti un lasītāja pieredzi un zināšanas.

Risinājums ir ieviests bezmaksas Google mākoņa pakalpojumā, izstrādāts Python valodā ar to NLP/ML bibliotēkām un grafiskajai saskarnei izmantots React.js

Autors: Māris K., LU Datorikas Fakultātes 4. kursa students, 2023./2024. m.g.

# Darbināšana lokāli

Nepiciešams Python, pieejams: https://www.python.org/downloads/
CL interpretorā palaist komandu `pip install requests/nltk/spacy/pyfiglet`
Norādiet direktoriju, kur stāv lv-complexity direktorija un darbiniet programmu `python lv-complexity -t TEXT_FILE.txt`, kur TEXT_FILE.txt ir jūsu pakļavīgs teksta fails ar tekstu saturu, kuru vēlaties izanalizēt. 

# Paldies šiem autoriem par izmantotajiem rīkiem:

- NLP-Pipe rīks latviešu valodai:  A. Znotiņš, P. Paikens, D. Goško; G. Bārzdiņš, N. Grūzītis, 2018, NLP-PIPE: Latvian NLP Tool Pipeline, CLARIN-LV digital library at IMCS, University of Latvia, Riga http://hdl.handle.net/20.500.12574/4 
- Izmantotais teksta korpuss vārdu biežumam: K. Levāne-Petrova, R. Darģis, K. Pokratniece, V. J. Lasmanis. 2022. The Balanced Corpus of Modern Latvian (LVK2022). CLARIN-LV digital library. Riga. Pieejams: https://nosketch.korpuss.lv/#wordlist?corpname=LVK2022&tab=basic&wlattr=lc&showresults=1
- Ushuia rīks, hunspell bāzēts: https://www.ushuaia.pl/hyphen/?ln=lv
