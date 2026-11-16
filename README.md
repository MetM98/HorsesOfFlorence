# 🐴 Horses of Florence

**A cavallo in viaggio verso l'armonia.**

Sito web bilingue (italiano / inglese) di *Horses of Florence*: un progetto nel cuore del Chianti fiorentino, alle porte di Firenze, in cui il cavallo non è solo compagno ma guida, un ponte tra la terra e l'interiorità.

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
- essere pienamente fruibile in **italiano e inglese**.

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
- **Inglese**: traduzione **in corso** (da completare prima della pubblicazione).

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

> `[DA COMPLETARE]` Lo stack non è ancora stato definito. Compilare questa sezione quando verrà scelto.

| Ambito | Scelta |
|---|---|
| Framework / generatore | `[DA COMPLETARE]` |
| Gestione i18n (IT/EN) | `[DA COMPLETARE]` |
| Stili | `[DA COMPLETARE]` |
| Hosting / deploy | `[DA COMPLETARE]` |
| Modulo contatti | `[DA COMPLETARE]` |

## Struttura del repository

Struttura **proposta** (da adattare allo stack scelto):

```text
.
├── content/
│   ├── it/          # testi in italiano
│   └── en/          # traduzioni in inglese
├── public/
│   ├── images/      # fotografie ottimizzate
│   └── logo/        # logo (SVG/PNG)
├── src/             # pagine, componenti, stili
└── README.md
```

## Avvio in locale

> `[DA COMPLETARE]` Aggiungere i comandi di installazione, sviluppo e build una volta scelto lo stack.

```bash
git clone https://github.com/MetM98/HorsesOfFlorence.git
cd HorsesOfFlorence
```

## Roadmap

- [ ] Completare la traduzione inglese dei testi
- [ ] Scegliere e documentare lo stack tecnologico
- [ ] Ricavare logo vettoriale e palette definitiva (blu, avorio, argento)
- [ ] Raccogliere e ottimizzare le fotografie (alta definizione, diritti verificati)
- [ ] Inserire contatti e modulo di richiesta informazioni
- [ ] Collegare la pagina abbigliamento ("Vesti la nostra filosofia")
- [ ] Ottimizzazione SEO bilingue (`hreflang`, meta tag)
- [ ] Verifica accessibilità e prestazioni (mobile first)
- [ ] Informativa privacy e cookie, se necessari
- [ ] Pubblicazione

## Licenza

© Horses of Florence. Tutti i diritti riservati. Testi, logo, marchio e immagini sono di proprietà dei rispettivi titolari e non possono essere riutilizzati senza autorizzazione.

> `[DA CONFERMARE]` Se il codice dovrà essere open source, scegliere una licenza (es. MIT) e applicarla al solo codice, lasciando riservati contenuti e marchio.
