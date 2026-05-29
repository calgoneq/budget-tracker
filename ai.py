from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_summary(transactions: list[dict]) -> str:
    if not transactions:
        return "Brak transakcji do podsumowania."

    lines = []
    for t in transactions:
        line = f"\n- Sklep: {t['sklep']}, Kwota: {t['kwota']} PLN, Kategoria: {t['kategoria']}, Data: {t['data']}"
        lines.append(line) 
        
    prompt = f"""Oto lista moich wydatków:
{lines}
Napisz krótkie podsumowanie (3-4 zdania) po polsku: na co i ile wydałem, 
która kategoria dominuje, czy coś rzuca się w oczy."""

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Błąd podczas generowania podsumowania: {str(e)}"
