# Persoonlijke review checklist - Serhat

Deze checklist gebruik ik bij elke code review die ik doe. Kort genoeg om in een paar minuten af te lopen, scherp genoeg om de belangrijkste dingen niet te missen.

## Voor ik begin

- [ ] Issue erbij gepakt en acceptatiecriteria gelezen
- [ ] Applicatie lokaal gestart en de feature uitgeprobeerd (niet alleen diff lezen)

## Tijdens het reviewen

- [ ] **Naamgeving** snap ik binnen 5 seconden wat een functie of variabele doet?
- [ ] **Randgevallen** wat gebeurt er bij lege input, null of een hele lange string?
- [ ] **Losse eindjes** geen `console.log`, TODO comments of uitgecommentarieerde code
- [ ] **Veiligheid** geen wachtwoorden, tokens of persoonsgegevens in de code
- [ ] **Tests** is er een test voor de nieuwe code en draait CI groen?

## Bij het geven van feedback

- [ ] Inline comments op specifieke regels, niet algemeen
- [ ] Vraag stellen in plaats van oordelen ("Zou X duidelijker zijn?" in plaats van "Dit is fout")
- [ ] Ook positieve feedback gegeven waar het verdiend is
- [ ] Concreet: uitgelegd wat ik verwacht, niet alleen dat iets anders moet

## Voor ik approve

- [ ] Alle threads zijn resolved
- [ ] Ik sta er echt achter, geen approval uit beleefdheid
- [ ] CI is groen
- [ ] Acceptatiecriteria daadwerkelijk afgevinkt
