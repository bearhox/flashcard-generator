import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

def fetch_definition(word):
    """Retrieve the definition of a word using a dictionary API."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()
        
        if isinstance(data, list) and "meanings" in data[0]:
            meanings = data[0]["meanings"]
            if meanings and "definitions" in meanings[0]:
                return meanings[0]["definitions"][0]["definition"]
    
    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError):
        return "Definition not found"
    
    return "Definition not found"

def generate_pdf(flashcards, output_file="flashcards.pdf"):
    print(f"Generating PDF... Saving to {output_file}")  # Debugging line
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    card_width = width / 2 - 40
    card_height = height / 4 - 20
    x_start_left = 30
    x_start_right = width / 2 + 10
    y_start = height - 50

    c.setFont("Helvetica-Bold", 14)

    for index, (word, definition) in enumerate(flashcards):
        print(f"Processing: {word}")  # Debugging line
        if y_start < 50:  # Check if a new page is needed
            c.showPage()
            y_start = height - 50
            c.setFont("Helvetica-Bold", 14)

        # Draw word flashcard border
        c.setStrokeColor(colors.black)
        c.rect(x_start_left, y_start - card_height, card_width, card_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x_start_left + 10, y_start - 30, word)
        
        # Draw definition flashcard border
        c.setStrokeColor(colors.black)
        c.rect(x_start_right, y_start - card_height, card_width, card_height)
        c.setFont("Helvetica", 12)
        wrapped_text = simpleSplit(definition, "Helvetica", 12, card_width - 20)
        y_text = y_start - 30
        for line in wrapped_text:
            if y_text < y_start - card_height + 20:
                break
            c.drawString(x_start_right + 10, y_text, line)
            y_text -= 15

        # Adjust y_start for next row of flashcards
        y_start -= card_height + 20

    c.save()
    print(f"PDF saved successfully as {output_file}")  # Debugging line

### Enter file name here in .txt
def main():
    with open("words.txt", "r") as f:
        words = [line.strip() for line in f.readlines()]
    
    flashcards = [(word, fetch_definition(word)) for word in words]
    
    if not flashcards:
        print("No flashcards to generate. Check words.txt file.")
        return
    
    print(f"Generating PDF with {len(flashcards)} flashcards.")  # Debugging line
    generate_pdf(flashcards)

if __name__ == "__main__":
    main()

print("Flashcards PDF has been generated successfully.")

