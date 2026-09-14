# Detalii: Adăugare endpoint putere

## Descriere logică nouă
- Endpoint: GET **/power**
- Parametri query:
  - **base** — valoare de bază, convertită cu `parseFloat(req.query.base)`; dacă lipsește sau nu e numerică se folosește implicit **0** (din `parseFloat(...) || 0`).
  - **exponent** — exponentul, convertit cu `parseFloat(req.query.exponent)`; dacă lipsește sau nu e numeric se folosește implicit **0**.
- Operație: se calculează **Math.pow(base, exponent)**.
- Răspuns JSON: `{ operation: "power", result: <număr> }`.
- Comportamente notabile:
  - Se acceptă exponenți negativi și fracționari (comportament nativ `Math.pow`).
  - Cazul **0^0** va returna **1** conform comportamentului JavaScript (`Math.pow(0, 0) === 1`).
  - Valorile invalide sau absentate sunt transformate silentios în **0** (fără eroare).
- Decizii importante:
  - Folosirea `parseFloat(... ) || 0` pentru a asigura un număr implicit **0** în loc de a valida/respinge inputurile ne numerice.

---
*Acest document a fost generat automat de AI la data de 2026-09-14 09:32 (Sursa: PR #3).*