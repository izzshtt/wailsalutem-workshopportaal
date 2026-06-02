# Code Review checklist - Nexus IT

Deze checklist gebruikt elke reviewer bij een MR. Alle punten doorlopen voor je approval geeft.

## Functioneel

- [ ] De code doet wat de gekoppelde issue beschrijft
- [ ] Alle acceptatiecriteria uit de issue zijn afgevinkt
- [ ] Randgevallen zijn afgedekt (lege input, null, foutieve invoer)
- [ ] Foutafhandeling is aanwezig waar nodig
- [ ] Applicatie lokaal gedraaid en feature getest

## Kwaliteit en leesbaarheid

- [ ] Functies en variabelen hebben duidelijke namen
- [ ] Functies doen 1 ding (Single Responsibility)
- [ ] Geen dode code, console.log of debug statements
- [ ] Comments alleen waar de code het waarom niet duidelijk maakt
- [ ] Geen duplicate code zonder reden

## Stijl en conventies

- [ ] Code volgt de HvA code conventies
- [ ] Indentatie en formatting consistent
- [ ] Geen Type errors of linter warnings
- [ ] Bestandsnamen en structuur volgen de afspraak

## Tests en CI

- [ ] CI pipeline is groen
- [ ] Bestaande tests draaien nog steeds
- [ ] Voor nieuwe functionaliteit zijn tests toegevoegd

## Security

- [ ] Geen wachtwoorden, API keys of tokens in code of commits
- [ ] Geen persoonsgegevens gelogd
- [ ] Input wordt gevalideerd

## Commit en MR

- [ ] Commit messages volgen Conventional Commits
- [ ] MR template is ingevuld (wat, hoe te testen, screenshots, checklist)
- [ ] MR is klein en gericht (richtlijn maximaal 400 regels)
- [ ] Branch naam volgt de conventie (`feature/`, `bugfix/`, `hotfix/`)

---

Zie ook [TEAMAFSPRAKEN.md](TEAMAFSPRAKEN.md) voor de bredere afspraken.
