# Detalii: Limitare exponent la 100

## Ce s-a schimbat
- Endpoint: /power
- Parsare input:
  - **base** este obținut cu: parseFloat(req.query.base) || 0
  - **exponent** este obținut cu: parseFloat(req.query.exponent) || 0
- Regula nouă de business:
  - Dacă **exponent > 100**, serverul returnează un răspuns cu status **400** și body JSON: { "error": "The maximum allowed exponent is 100." } și oprește execuția (nu se calculează puterea).
  - Dacă **exponent <= 100**, se continuă normal și se răspunde cu { "operation": "power", "result": Math.pow(base, exponent) }.
- Detalii și implicații:
  - **100** este valoarea maximă permisă pentru **exponent** (inclusiv 100 este permis).
  - Mesajul de eroare exact este: "The maximum allowed exponent is 100."
  - Valorile lipsă sau invalide pentru **base** sau **exponent** vor fi convertite implicit la **0** din cauza `|| 0`.
  - Exponenții negativi sau 0 sunt în continuare acceptați (nu sunt restricționați).
  - Măsura oprește calculul pentru exponenți prea mari, reducând posibile costuri sau riscuri legate de operații foarte intensive.

---
*Acest document a fost generat automat de AI la data de 2026-09-14 09:38 (Sursa: PR #4).*