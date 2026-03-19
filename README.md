# Tady Coin - Blockchain

Jednoduchá ukázka toho, jak funguje blockchainová síť. Projekt v sobě obsahuje **REST API** (postavené na Flasku), trvalé ukládání dat do souboru (`blockchain.json`), algoritmus **Proof of Work** a automatickou kontrolu **integrity sítě**.

## Jak to spustit

1. Ujistěte se, že máte nainstalovaný Python a knihovnu Flask:
   `pip install Flask`
2. Zapněte hlavní server příkazem:
   `python server.py`
3. Server nyní běží na adrese `http://127.0.0.1:5000`

## Jak používat API

Když server běží, můžete otevírat tyto adresy přímo ve webovém prohlížeči:

* **Zobrazit historii:** `GET /blocks` (Ukáže všechny zapsané bloky)
* **Vytěžit blok:** `GET /mine` (Zpracuje čekající transakce a trvale je zapíše do databáze)
* **Zkontrolovat stav:** `GET /validate` (Ověří, zda se do sítě nikdo nenaboural)

Nebo můžete ve druhém terminálu spustit skript `python client.py`, který celou ukázku projede automaticky.


## Spuštění klientského dema

- Nyní nasimulujeme uživatele, který posílá peníze a těží bloky.

1. Otevřete si úplně nové, druhé okno terminálu (ve VS Code pomocí tlačítka + v panelu terminálu).
2. Spusťte testovací skript příkazem: `python client.py`
3. Ve výpisu uvidíte, jak klient automaticky odeslal transakce, vytěžil nový blok a zkontroloval stav sítě. Ve vaší složce se právě objevil soubor blockchain.json!

---

## Návod na simulaci hackerského útoku

Tento projekt je navržen tak, aby ukázal, že blockchain nelze tajně zfalšovat. Zkuste si to sami:

1. Zapněte `server.py` a nechte proběhnout test pomocí `client.py`.
2. Všimněte si, že se ve vaší složce vytvořil soubor `blockchain.json`.
3. Vypněte server (`Ctrl + C` v terminálu).
4. Otevřete soubor `blockchain.json` v textovém editoru. Najděte tam libovolnou transakci (např. odeslání 100 mincí od Alice) a částku přepište na `99999`. Soubor uložte.
5. Znovu zapněte server `python server.py`.
6. Otevřete v prohlížeči adresu `http://127.0.0.1:5000/validate`.
7. **Výsledek:** Systém okamžitě odhalí podvod, protože vaše fyzická změna v textu narušila předpočítané matematické hashe. Vypíše chybu: `"NARUŠENO! Data byla změněna."`
