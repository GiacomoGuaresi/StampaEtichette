# StampaEtichette

**StampaEtichette** è uno strumento da riga di comando scritto in Python, pensato per generare etichette personalizzate a partire da template testuali. Utilizzato internamente per velocizzare e standardizzare la stampa di etichette con testi predefiniti.

---

## 🚀 Come iniziare

### 1. Clona il repository

```bash
git clone https://github.com/GiacomoGuaresi/StampaEtichette
cd StampaEtichette
```

### 2. Installa le dipendenze

Assicurati di avere Python 3 installato, quindi esegui:

```bash
pip install -r requirements.txt
```

### 3. Avvia lo strumento

```bash
python run.py
```

Segui le istruzioni mostrate nella console.

---

## 🧩 Aggiungere nuovi template

Per creare un nuovo template, aggiungi un file `.txt` all'interno della cartella `templates/`.

Ogni riga del file rappresenta un'etichetta.

Esempio di file `template_nuovo.txt`:

```
Etichetta 1
Etichetta 2
Etichetta 3
```

---

## 🔧 Build del programma

Puoi creare un eseguibile standalone con PyInstaller.

### Per Windows

```bash
python -m PyInstaller --onefile --add-data "templates;templates" run.py
```

L'eseguibile sarà disponibile in:

```
/dist/run.exe
```

### Per Linux/macOS

```bash
python -m PyInstaller --onefile --add-data "templates:templates" run.py
```

L'eseguibile sarà disponibile in:

```
/build/run
```

---

## 💻 Utilizzo

Il programma funziona interamente da console. Dopo l'avvio, verranno richieste alcune informazioni tramite prompt testuali.

Basta rispondere alle domande per generare correttamente le etichette.

---

## 📁 Struttura del progetto

```
StampaEtichette/
├── templates/         # Template di etichette (file .txt)
├── run.py             # Script principale per l'esecuzione
├── requirements.txt   # Dipendenze Python
├── README.md          # Questo file
```