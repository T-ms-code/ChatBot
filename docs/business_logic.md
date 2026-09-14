# Logica de Business - API Backend

Aceasta documentatie este generata si actualizata automat de agentul LLM pe baza Pull Request-urilor din aplicatie. Aici regasesti istoricul deciziilor si regulilor de business, ordonate cronologic.

---

## Istoric Modificari (Paths)
* **[2026-09-14] S-a adăugat un endpoint GET /power care calculează exponentierea valorii **base** la **exponent** din query string și returnează rezultatul în JSON.** 
  * -> [Explorează detaliile logicii](./pr_3_adăugare_endpoint_putere.md)
* **[2026-09-14] Endpoint-ul /power verifică acum dacă **exponent** depășește 100 și, în acest caz, returnează o eroare 400 fără a efectua calculul.** 
  * -> [Explorează detaliile logicii](./pr_4_limitare_exponent_la_100.md)
* **[2026-09-14] Endpoint-ul "/power" a fost eliminat, inclusiv validarea pragului pentru **exponent** (maxim 100).** 
  * -> [Explorează detaliile logicii](./pr_5_eliminare_endpoint_putere.md)
