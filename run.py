from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
import os
import sys

# Determine the correct base path for templates, whether running as a script or a PyInstaller executable.
if getattr(sys, 'frozen', False):
    # If running as a frozen executable (e.g., created by PyInstaller)
    base_path = os.path.join(sys._MEIPASS, "templates")
else:
    # If running as a normal Python script
    base_path = os.path.abspath("./templates")

# Load .txt files from the 'templates' folder.
# The original script limited this to the first 9 files; maintaining that behavior.
txt_files = [f for f in os.listdir(base_path) if f.endswith(".txt")]
if len(txt_files) > 9:
    txt_files = txt_files[:9]

# Initialize variables for label dimensions and layout. These will be set based on the chosen mode.
cell_width = 0
cell_height = 0
num_cols = 0
num_rows = 0
x_offset = 0
y_offset = 0

# Define A4 page dimensions.
page_width, page_height = A4

# Define the output PDF file name.
output_file = "griglia_etichette.pdf"

# --- Step 1: Choose the printing mode ---
print("Scegli la modalità di stampa:")
print("1. Fogli 110 etichette (Etichette 38.1mm x 13mm)")
print("2. Legacy (Etichette 35mm x 5mm)")

while True:
    try:
        mode_choice = int(input("Inserisci il numero della modalità: "))
        if mode_choice == 1:
            print_mode = "110_labels"
            break
        elif mode_choice == 2:
            print_mode = "legacy"
            break
        else:
            print("Scelta non valida. Riprova.")
    except ValueError:
        print("Inserisci un numero valido.")

# --- Step 2: Set parameters based on the chosen mode ---
if print_mode == "legacy":
    cell_width = 35 * mm
    cell_height = 5 * mm
    # Calculate columns and rows dynamically for the legacy mode to fit the page.
    # The original script used 30mm total horizontal margin and 35mm total vertical margin.
    num_cols = int((page_width - 30 * mm) // cell_width)
    num_rows = int((page_height - 35 * mm) // cell_height)
    # Calculate offsets to center the grid on the page.
    x_offset = (page_width - num_cols * cell_width) / 2
    y_offset = (page_height - num_rows * cell_height) / 2
elif print_mode == "110_labels":
    cell_width = 39 * mm
    cell_height = 13 * mm
    num_cols = 5  # Fixed 5 columns for 110-label sheets
    num_rows = 22 # Fixed 22 rows for 110-label sheets
    # Calculate offsets to center the block of labels.
    # This results in approximately 10mm horizontal margins and 5.5mm vertical margins.
    # The user requested "circa 9/10mm" border; this calculation prioritizes centering the fixed grid.
    x_offset = (page_width - (num_cols * cell_width)) / 2
    y_offset = (page_height - (num_rows * cell_height)) / 2

# --- Step 3: Display available files and get user's file choice ---
print("\nScegli un file:")
for i, filename in enumerate(txt_files, 1):
    print(f"{i}. {filename}")

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

# --- Step 4: Get the number of copies to produce ---
while True:
    try:
        num_copies = int(input("Inserisci il numero di macchine/subassemblati da produrre: "))
        if num_copies > 0:
            break
        else:
            print("Il numero deve essere maggiore di 0.")
    except ValueError:
        print("Inserisci un numero intero valido.")

# --- Step 5: Read labels from the selected file ---
labels = []
file_path = os.path.join(base_path, selected_file)
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        clean_line = line.strip()
        # Each unique label from the file is duplicated 'num_copies * 2' times.
        # This accounts for 'num_copies' sets, where each label appears twice (left and right) per set.
        labels.extend([clean_line] * num_copies * 2)

# --- Step 6: Create the PDF canvas ---
c = canvas.Canvas(output_file, pagesize=A4)

# Set grid line color to white (invisible) as requested.
grid_color = Color(255, 255, 255)

# --- Step 7: Draw labels onto the PDF ---
# Loop as long as there are labels to draw.
while labels:
    c.setStrokeColor(grid_color)
    c.setFont("Helvetica", 8)

    # Iterate through rows and columns to place labels.
    for row in range(num_rows):
        for col in range(num_cols):
            # Stop drawing if all labels have been used.
            if not labels:
                break

            # Calculate X position (from left).
            x = x_offset + col * cell_width
            # Calculate Y position (from top, as ReportLab's Y-axis starts from bottom).
            # This makes sure labels are drawn top-down.
            y = page_height - (y_offset + (row + 1) * cell_height)

            # Get the current label text.
            currentLabel = labels.pop(0)

            # Draw a transparent rectangle for the label cell (border only).
            c.rect(x, y, cell_width, cell_height, fill=0, stroke=0)

            # Set text color to black.
            c.setFillColorRGB(0, 0, 0)

            # Define text margin from the cell edge.
            text_margin = 4 * mm
            # Calculate Y position for text to be vertically centered within the cell.
            text_y = y + cell_height / 2 - 3 # -3 is a small adjustment for font baseline.

            # Draw the label text aligned to the left.
            c.drawString(x + text_margin, text_y, currentLabel)
            # Draw the label text aligned to the right.
            c.drawRightString(x + cell_width - text_margin, text_y, currentLabel)

    # --- Step 8: Draw crop marks (arrows) at the page margins ---
    if print_mode == "legacy":
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(0, 0, 0)

        # Draw top and bottom arrows.
        for col in range(num_cols + 1):
            x_center = x_offset + col * cell_width
            # Top arrows (above the label grid)
            c.drawCentredString(x_center, page_height - y_offset + 4, "↓")
            # Bottom arrows (below the label grid)
            c.drawCentredString(x_center, page_height - (y_offset + num_rows * cell_height) - 8, "↑")

        # Draw left and right arrows.
        for row in range(num_rows + 1):
            # Y position for side arrows (aligned with the top of each row).
            y_pos_for_side_arrow = page_height - (y_offset + row * cell_height)
            # Left arrows
            c.drawString(x_offset - 10, y_pos_for_side_arrow - 2, "→")
            # Right arrows
            c.drawString(x_offset + num_cols * cell_width + 4, y_pos_for_side_arrow - 2, "←")

    # If there are still labels remaining, add a new page for them.
    if labels:
        c.showPage()

# --- Step 9: Save the PDF and open it ---
c.save()
print(f"PDF creato: {output_file}")

# Open the generated PDF automatically based on the operating system.
if sys.platform == "win32":
    os.startfile(output_file, "open")
else:
    os.system(f"open {output_file}")

