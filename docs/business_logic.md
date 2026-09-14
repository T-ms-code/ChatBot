# Logica de Business - API Backend

## Ce avem initial?

1. **Endpoint pentru Adunare (`GET /sum`):** Expune o rută care preia parametrii `a` și `b` din cererea URL (query string) și returnează un obiect JSON conținând tipul operației ("sum") și rezultatul adunării matematice a celor două valori.
2. **Endpoint pentru Scădere (`GET /diff`):** Expune o rută similară care preia parametrii `a` și `b` și returnează un obiect JSON cu tipul operației ("difference") și rezultatul scăderii acestora (`a - b`).
3. **Mecanism de Fallback:** Pentru ambele rute, valorile primite sunt convertite în numere fracționare (`parseFloat`). În cazul în care parametrii lipsesc din cerere sau nu pot fi convertiți într-un număr valid, sistemul atribuie automat valoarea `0` pentru a garanta finalizarea cu succes a operației.

Aceasta documentatie este generata automat de agentul LLM pe baza Pull Request-urilor din aplicatie.

---
