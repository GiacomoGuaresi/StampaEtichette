from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
import os
import sys

# Trova la cartella corretta (normale o da eseguibile)
if getattr(sys, 'frozen', False):
    base_path = os.path.join(sys._MEIPASS, "templates")
else:
    base_path = os.path.abspath("./templates")

# Carica i file .txt dalla cartella templates
txt_files = [f for f in os.listdir(base_path) if f.endswith(".txt")][:9]

cell_width = 35 * mm
cell_height = 5 * mm
page_width, page_height = A4

output_file = "griglia_etichette.pdf"

# Mostra i file disponibili
print("Scegli un file:")
for i, filename in enumerate(txt_files, 1):
    print(f"{i}. {filename}")

# Input scelta file
while True:
    try:
        choice = int(input("Inserisci il numero del file da usare: "))
        if 1 <= choice <= len(txt_files):
            selected_file = txt_files[choice - 1]
            break
        else:
            print("Scelta non valida. Riprova.")
    except ValueError:
        print("Inserisci un numero valido.")

# Input numero di copie
while True:
    try:
        num_copies = int(input("Inserisci il numero di macchine/subassemblati da produrre: "))
        if num_copies > 0:
            break
        else:
            print("Il numero deve essere maggiore di 0.")
    except ValueError:
        print("Inserisci un numero intero valido.")

# Leggi il contenuto del file
labels = []
file_path = os.path.join(base_path, selected_file) 
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        clean_line = line.strip()
        labels.extend([clean_line] * num_copies * 2)

# Crea il canvas
c = canvas.Canvas(output_file, pagesize=A4)

# Colore linea semitrasparente
# grid_color = Color(0, 0, 0, alpha=0.1)
grid_color = Color(255,255,255)

# Calcola quante celle per pagina
num_cols = int((page_width - 30 * mm) // cell_width)
num_rows = int((page_height - 35 * mm) // cell_height)

# Margini
x_offset = (page_width - num_cols * cell_width) / 2
y_offset = (page_height - num_rows * cell_height) / 2

# Disegna finché ci sono label
while labels:
    c.setStrokeColor(grid_color)
    c.setFont("Helvetica", 8)

    for row in range(num_rows):
        for col in range(num_cols):
            if not labels:
                break

            x = x_offset + col * cell_width
            y = y_offset + row * cell_height

            currentLabel = labels.pop(0)

            # Rettangolo trasparente
            c.rect(x, y, cell_width, cell_height, fill=0)

            # Testo allineato a sinistra e duplicato a destra
            text_margin = 2 * mm
            text_y = y + cell_height / 2 - 3

            c.setFillColorRGB(0, 0, 0)
            c.drawString(x + text_margin, text_y, currentLabel)
            c.drawRightString(x + cell_width - text_margin, text_y, currentLabel)

    # Simboli ⊕ ai margini
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0, 0, 0)

    for col in range(num_cols + 1):
        x = x_offset + col * cell_width
        c.drawCentredString(x, y_offset - 8, "↑")
        c.drawCentredString(x, y_offset + num_rows * cell_height + 4, "↓")

    for row in range(num_rows + 1):
        y = y_offset + row * cell_height
        c.drawString(x_offset - 10, y - 2, "→")
        c.drawString(x_offset + num_cols * cell_width + 4, y - 2, "←")

    # Se ci sono ancora label, aggiungi una nuova pagina
    if labels:
        c.showPage()

# Salva il PDF
c.save()
print(f"PDF creato: {output_file}")

# Apri il PDF automaticamente
os.startfile(output_file, "open") if sys.platform == "win32" else os.system(f"open {output_file}")