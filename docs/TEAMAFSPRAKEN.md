# Teamafspraken Nexus IT

Dit document bevat de afspraken die wij als team Nexus IT hanteren voor samenwerken via GitLab, merge requests en code reviews. Deze afspraken staan in GitLab zodat iedereen ze kan teruglezen en we ze in de les kunnen presenteren.

## 1. Branches

- Werken gebeurt altijd op een eigen branch, nooit direct op `main`
- 1 issue = 1 branch
- Branch naamgeving:
  - `feature/<korte-omschrijving>` voor nieuwe functies
  - `bugfix/<korte-omschrijving>` voor bug fixes
  - `hotfix/<korte-omschrijving>` voor spoedreparaties
- Branches blijven kortlevend (maximaal een paar dagen)
- Voor een MR halen we eerst de laatste `main` of `develop` binnen

## 2. Commit messages

We volgen Conventional Commits:

- `feat(scope): beschrijving` voor nieuwe functies
- `fix(scope): beschrijving` voor bug fixes
- `docs(scope): beschrijving` voor documentatie
- `refactor(scope): beschrijving` voor herstructurering
- `test(scope): beschrijving` voor tests

Voorbeeld: `feat(login): voeg wachtwoord reset toe`

Regels:
- Klein en vaak committen, maar wel werkende code
- Geen Type errors meecommitten
- Berichten in het Nederlands of Engels, kies er een en blijf consistent

## 3. Merge Requests

### Grootte en frequentie
- Kleine, gerichte MR's (richtlijn maximaal ongeveer 400 regels)
- Grote features opsplitsen in meerdere MR's
- Geen Work In Progress mergen naar `main` of `develop`

### Aanmaken
- Maak de MR aan vanuit de issue (Create merge request knop)
- Gebruik altijd de MR template
- Wijs een reviewer aan voor je de MR opent voor review

### Reviewen
- Elke MR heeft minimaal 1 reviewer (teamgenoot)
- Niemand merged zijn eigen MR zonder approval
- Reviewer reageert binnen 24 uur (op werkdagen)
- Developer reageert binnen 24 uur op feedback

### Approval en merge
- Minimaal 1 approval nodig
- Alle threads moeten resolved zijn
- Pas mergen als CI groen is
- Donderdag voor 17:00 alles afgerond zodat we vrijdag schoon beginnen

### GitLab instellingen
In Settings > Merge Requests staat afgedwongen:
- "All threads must be resolved"
- "Minimum required approvals: 1"

## 4. Code review afspraken

### Waar letten we op
- Functionele correctheid (acceptatiecriteria afgevinkt, randgevallen afgedekt)
- Leesbaarheid (duidelijke namen, functies doen 1 ding)
- Stijl en conventies (HvA code conventies, geen Type errors)
- Tests en CI groen
- Security (geen wachtwoorden, tokens of persoonsgegevens in code)

### Feedback geven
- Gebruik inline comments op specifieke regels
- Concreet zijn: leg uit wat je verwacht, niet alleen dat iets fout is
- Stel vragen als iets onduidelijk is
- Geef ook positieve feedback
- Focus op de code, niet op de persoon

### Merge conflicts
- Eerst zelf proberen op te lossen door `main` of `develop` binnen te halen
- Lukt het niet? Overleg met de andere ontwikkelaar
- Conflicten zijn een signaal: vaker pullen en kleinere MR's maken

## 5. Templates

We hebben templates in de repo onder `.gitlab/`:

- `.gitlab/merge_request_templates/Default.md` voor elke nieuwe MR
- `.gitlab/issue_templates/Default.md` voor elke nieuwe issue

Deze worden automatisch geladen in GitLab.

## 6. Werkritme

- Dagelijks pullen voor je begint te werken
- Klein en vaak committen
- Reviews doen we verspreid over de week, niet alleen vrijdag
- Vragen of blokkades meteen delen in de teamchat, niet wachten tot de standup

---

*Laatst bijgewerkt: 20 mei 2026*
