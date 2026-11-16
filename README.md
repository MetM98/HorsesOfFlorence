# 🐴 Horses of Florence

**A cavallo in viaggio verso l'armonia.**

Sito web in italiano, inglese e tedesco di *Horses of Florence*: un progetto nel cuore del Chianti fiorentino, alle porte di Firenze, in cui il cavallo non è solo compagno ma guida, un ponte tra la terra e l'interiorità.

---

## Indice

- [Il progetto](#il-progetto)
- [Cosa offre Horses of Florence](#cosa-offre-horses-of-florence)
- [Struttura del sito](#struttura-del-sito)
- [Lingue e contenuti](#lingue-e-contenuti)
- [Linee guida di brand](#linee-guida-di-brand)
- [Requisiti per i partecipanti](#requisiti-per-i-partecipanti)
- [Stack tecnologico](#stack-tecnologico)
- [Struttura del repository](#struttura-del-repository)
- [Avvio in locale](#avvio-in-locale)
- [Roadmap](#roadmap)
- [Licenza](#licenza)

---

## Il progetto

Questo repository contiene il codice e i contenuti del sito ufficiale di **Horses of Florence**.

Il sito presenta una proposta fondata sulla relazione con il cavallo e sul ritorno a sé: un invito a rallentare, a sentire, a ritrovare il proprio centro, unendo la bellezza della campagna fiorentina alla profondità del rapporto con l'animale.

Obiettivi del sito:

- raccontare la filosofia e l'approccio di Horses of Florence;
- presentare l'offerta (sessioni con i cavalli, soggiorno, esperienze sul territorio);
- permettere a chi visita di mettersi in contatto per ricevere informazioni;
- essere pienamente fruibile in **italiano, inglese e tedesco**.

## Cosa offre Horses of Florence

- **Accoglienza individuale o in piccoli gruppi**: da uno a tre cavalieri al massimo, così che l'istruttore possa curare anche i minimi dettagli.
- **Cavalli propri o altrui**: si lavora con i cavalli della struttura oppure con il proprio cavallo, che può essere ospitato presso la struttura di riferimento.
- **Struttura di riferimento**: centro ippico affiliato alla Federazione Italiana Sport Equestri (FISE), con personale qualificato.
- **Lavoro con i cavalli da terra e in sella**, con due finalità principali:
  - migliorare il rapporto con il proprio cavallo, compagno di vita o di lavoro;
  - superare blocchi emotivi, ritrovare se stessi, rigenerarsi e recuperare energie.
- **Soggiorno** presso il B&B, per vivere la vacanza o il tempo libero come un viaggio verso se stessi.

### Esperienze sul territorio

Oltre al tempo trascorso con i cavalli, il sito presenta le attività possibili nei dintorni:

- visita a borghi fortificati, piccoli paesi e castelli;
- Siena e Firenze, e altre mete turistiche raggiungibili anche in mezz'ora;
- piscina, padel e pesca sportiva nei pressi del B&B;
- esplorazione in bicicletta (con noleggio) o a piedi lungo il torrente Pesa, dal B&B fino a Cerbaia in Val di Pesa, tramite pista ciclabile dedicata;
- degustazione di olio e vini locali presso realtà produttive del territorio.

## Struttura del sito

| Sezione | Contenuto |
|---|---|
| **Home** | Presentazione del progetto, della filosofia e del luogo (Chianti fiorentino, alle porte di Firenze). |
| **Noi per voi** | Modalità di accoglienza (individuale o piccoli gruppi), struttura FISE, attività con i cavalli da terra e in sella, soggiorno. |
| **Scegli le tue esperienze** | Attività e visite sul territorio: borghi, castelli, Siena e Firenze, piscina, padel, pesca sportiva, bici e passeggiate lungo il Pesa, degustazioni. |
| **Contatti** | Modulo e/o recapiti per richiedere informazioni. Invito finale: *"Non aspettare domani per prenderti cura di Te, di Voi."* |
| **Abbigliamento** | Link a "Vesti la nostra filosofia", la linea di abbigliamento del progetto. |

Nota di footer / informazioni pratiche: *richiesta la conoscenza delle tre andature; indossare abbigliamento idoneo.*

## Lingue e contenuti

- **Italiano**: testo completo disponibile e approvato come base del sito.
- **Inglese** e **tedesco**: traduzioni fedeli dei testi italiani (il tedesco usa il «Du» maiuscolo, come il «Tu» dell'italiano).

Indicazioni per la gestione dei testi:

- i contenuti vanno tenuti separati dal codice (file o collezioni per lingua), così da poter aggiornare testi e traduzioni senza toccare i template;
- ogni pagina deve esistere in entrambe le lingue, con selettore di lingua visibile;
- per la SEO prevedere `<html lang>`, meta title/description per lingua e tag `hreflang`;
- il tono del testo è intimo e rivolto direttamente a chi legge (uso del "Tu" maiuscolo): la traduzione inglese dovrebbe mantenere lo stesso registro caldo e personale.

## Linee guida di brand

Indicazioni ricevute dalla titolare del progetto:

- **Colori**: blu e avorio molto chiaro come base; l'abbigliamento del progetto usa blu, bianco e argento (l'argento può essere usato per dettagli e accenti).
- **Tipografia**:
  - titoli: il font maiuscolo usato nel logo;
  - testo corrente: uno stile affine a quello del sito del B&B.
- **Logo**: fornito in PDF (`Horses of Florence logo pdf.pdf`). Per il sito è consigliabile ricavarne una versione vettoriale (SVG) e una raster ottimizzata.
- **Fotografie**: si useranno le foto disponibili e/o immagini da Internet, preferibilmente ad alta definizione. In caso di immagini di terzi, verificare sempre licenza e diritti d'uso prima della pubblicazione.

## Requisiti per i partecipanti

- Conoscenza delle **tre andature** (passo, trotto, galoppo).
- **Abbigliamento idoneo** all'equitazione.

## Stack tecnologico

Lo stesso approccio del sito del B&B *A spasso con Daisy*: sito vetrina statico, veloce e senza dipendenze nel browser.

| Ambito | Scelta |
|---|---|
| Framework / generatore | HTML statico generato con Python + Jinja2 (`build.py`) |
| Lingue (IT/EN/DE) | Un file di testi per lingua: `src/content/it.json`, `en.json`, `de.json` |
| Stili | CSS scritto a mano (`assets/css/style.css`), nessun framework |
| Font | Montserrat (titoli, simile alla scritta del logo), Jost (testo, come il B&B), Cormorant Garamond corsivo (citazioni). Ospitati nel sito, licenza OFL |
| Hosting / deploy | GitHub Pages tramite GitHub Actions (`.github/workflows/pages.yml`) |
| Contatti | Collegamenti diretti a WhatsApp, email, telefono e Instagram (da `src/site.json`): nessun modulo, nessun dato salvato |
| Animazioni | `assets/js/main.js`: ogni movimento dipende solo dalla posizione di scorrimento, va avanti scendendo e si riavvolge risalendo. Con «riduci movimento» attivo, o senza JavaScript, tutto resta fermo e visibile |
| Cookie | Nessuno: niente statistiche né contenuti di terze parti, quindi niente banner |

## Struttura del repository

```text
.
├── index.html, privacy/, en/, de/     pagine generate (non modificarle a mano)
├── src/
│   ├── content/it.json, en.json, de.json   testi delle pagine (solo i testi forniti, e la loro traduzione)
│   ├── content/legal/*.json           informativa privacy e cookie (IT/EN/DE)
│   ├── site.json                      contatti, link, titolare, opzioni
│   └── base.html, home.html, legal.html, macros.html   template
├── assets/
│   ├── css/style.css                  stile (blu, avorio, argento)
│   ├── js/main.js                     menu, intestazione, movimenti legati allo scorrimento
│   ├── fonts/                         font ospitati in locale
│   └── img/
│       ├── brand/                     logo originale (PDF), versioni vettoriali SVG, favicon, immagine social
│       ├── photos/                    foto ottimizzate (WebP) + credits.json
│       └── icons.svg                  icone
├── tools/
│   ├── logo.py                        ricava gli SVG del logo dal PDF/JPEG originale
│   ├── photos.py                      scarica e ottimizza le foto elencate in credits.json
│   └── render_brand.js                crea favicon, icone e immagine per i social
├── build.py                           generatore
└── README.md
```

### Le scene della home

La home racconta i testi come una sequenza di scene. Ogni movimento segue lo scorrimento:

1. **Soglia**: il nome e il logo, poi un arco si apre sulle colline del Chianti all'alba (disegno vettoriale, inciso a linee sottili). Il sole sale mentre le parole del primo testo compaiono una alla volta.
2. **Un ponte**: tre archi si disegnano tra le coppie di parole.
3. **Alle porte di Firenze**: la foto si avvicina lentamente.
4. **Ogni passo, ogni sguardo, ogni respiro**: tre finestre ad arco si aprono come uno sguardo.
5. **Immersi nella natura**: un ramo d'olivo disegnato a inchiostro.
6. **Il proprio centro**: gli anelli di un tronco si chiudono verso il centro.
7. **Ricordare**: la parola in lamina d'argento cattura la luce.
8. **Noi per voi**: capolettera, filari disegnati, le due finalità.
9. **Scegli le tue esperienze**: su computer la campagna scorre in orizzontale lungo il torrente Pesa; su telefono è una colonna.
10. **Contatti** sotto le stelle, poi **Vesti la nostra filosofia**.

### Logo

Il PDF ricevuto contiene un'immagine JPEG piccola (491×624 px). `tools/logo.py` la ricalca in curve vettoriali:

- `assets/img/brand/logo.svg`: logo completo con scritta verticale, colori originali (nero e rosso);
- `mark.svg`: solo cavallo e giglio, colori originali;
- `mark-navy.svg` e `mark-ivory.svg`: cavallo blu notte o avorio, giglio rosso, usati nel sito su fondi chiari e scuri.

Se esiste un file vettoriale originale del logo (AI, EPS, SVG o PDF vettoriale), conviene usare quello.

### Foto

Le foto vengono da Unsplash (licenza gratuita, anche per uso commerciale). Quelle dei paesaggi sono le stesse del sito del B&B. Per sostituirle con foto vostre, ad esempio dei vostri cavalli e delle sessioni:

1. salvate il JPG in `tools/originals/<slug>.jpg`, usando lo slug della foto da sostituire (es. `mane`, `gaze`, `herd`);
2. lanciate `python3 tools/photos.py --force` e poi `python3 build.py`.

## Avvio in locale

```bash
git clone https://github.com/MetM98/HorsesOfFlorence.git
cd HorsesOfFlorence
```

```bash
pip install jinja2
```

```bash
python3 build.py
```

```bash
python3 -m http.server 8000
```

Poi apri http://localhost:8000.

### Come modificare i testi

1. Testi delle pagine: `src/content/it.json`, `en.json` e `de.json` (stessa struttura).
2. Privacy e cookie: `src/content/legal/it.json`, `en.json` e `de.json` (testo tecnico obbligatorio, da far rivedere).
3. Email, WhatsApp, telefono, Instagram, link all'abbigliamento e dati del titolare: `src/site.json`.
4. Rigenera le pagine con `python3 build.py`.

| Campo di `src/site.json` | Note |
|---|---|
| `email` | Indirizzo per i contatti e per la privacy. Finché manca, il sito mostra un segnaposto giallo «[da completare]». |
| `whatsapp` | Solo cifre, con prefisso (es. `393331234567`). Finché manca, compare il segnaposto. |
| `phone`, `instagram` | Facoltativi: compaiono nei contatti solo se compilati. |
| `apparel_url` | Link a «Vesti la nostra filosofia». Finché è vuoto, il collegamento porta ai contatti. |
| `owner` | Titolare del trattamento per l'informativa privacy. |
| `noindex` | `true` tiene l'anteprima fuori da Google. Mettere `false` alla pubblicazione definitiva. |

## Pubblicazione su GitHub Pages

1. Nel repository apri **Settings → Pages**.
2. In **Build and deployment → Source** scegli **GitHub Actions**.
3. A ogni modifica su `main` il sito viene rigenerato e pubblicato su `https://metm98.github.io/HorsesOfFlorence/` (oppure **Actions → Build and deploy site → Run workflow**).

Tutti i percorsi sono relativi, quindi il sito funziona anche con un dominio proprio (**Settings → Pages → Custom domain**). In quel caso aggiorna `base_url` in `src/site.json`.

## Roadmap

- [x] Scegliere e documentare lo stack tecnologico
- [x] Ricavare logo vettoriale e palette (blu, avorio, argento)
- [x] Testi definitivi in italiano e traduzione inglese
- [x] Contatti diretti (WhatsApp, email, telefono, Instagram)
- [x] SEO bilingue (`hreflang`, meta tag, dati strutturati, immagine per i social)
- [x] Accessibilità e prestazioni di base (mobile first, foto WebP, font locali)
- [x] Informativa privacy e cookie
- [ ] Rileggere le traduzioni inglese e tedesca
- [ ] Email, WhatsApp/telefono e dati del titolare in `src/site.json`
- [ ] Foto vere dei cavalli, delle sessioni e della struttura al posto di quelle di Unsplash
- [ ] Link alla linea di abbigliamento ("Vesti la nostra filosofia") in `apparel_url`
- [ ] Logo vettoriale originale, se disponibile
- [ ] Pubblicazione: `noindex` → `false`, GitHub Pages attivo

## Licenza

© Horses of Florence. Tutti i diritti riservati. Testi, logo, marchio e immagini sono di proprietà dei rispettivi titolari e non possono essere riutilizzati senza autorizzazione.

> `[DA CONFERMARE]` Se il codice dovrà essere open source, scegliere una licenza (es. MIT) e applicarla al solo codice, lasciando riservati contenuti e marchio.
