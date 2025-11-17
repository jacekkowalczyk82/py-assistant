import whisper
import os

def transkrybuj_audio(sciezka_do_pliku, jezyk="pl", model_name="base"):
    """
    Wykonuje transkrypcję pliku audio przy użyciu modelu Whisper.

    :param sciezka_do_pliku: Pełna ścieżka do pliku audio (np. MP3, WAV, M4A).
    :param jezyk: Kod języka do transkrypcji (domyślnie 'pl' dla polskiego).
    :param model_name: Nazwa modelu Whisper (np. 'base', 'small', 'medium').
    :return: Transkrybowany tekst lub komunikat o błędzie.
    """
    if not os.path.exists(sciezka_do_pliku):
        return f"BŁĄD: Plik nie został znaleziony pod ścieżką: {sciezka_do_pliku}"

    print(f"Ładowanie modelu '{model_name}' (to może potrwać kilka chwil za pierwszym razem)...")
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        return f"BŁĄD: Nie udało się załadować modelu. Upewnij się, że masz stabilne połączenie i wystarczającą ilość pamięci. Szczegóły: {e}"

    print(f"Rozpoczynanie transkrypcji pliku '{os.path.basename(sciezka_do_pliku)}'...")
    try:
        # Ustawienie opcji 'language' znacznie przyspiesza proces
        # i zwiększa dokładność transkrypcji dla konkretnego języka.
        result = model.transcribe(sciezka_do_pliku, language=jezyk)

        return result["text"]
    except Exception as e:
        return f"BŁĄD Transkrypcji: Nie udało się przetworzyć pliku. Szczegóły: {e}"

# --- UŻYCIE PROGRAMU ---

# 1. Zmień tę ścieżkę na ścieżkę do Twojego pliku nagrania (np. "C:/Users/User/Desktop/nagranie.mp3")
NAZWA_PLIKU_AUDIO = "moje_nagranie.mp3"

# 2. Wybierz model: 'base' jest szybki i wystarczający, 'small' jest dokładniejszy.
MODEL_WYBRANY = "small"

print(f"Program do Transkrypcji Whisper v1.0")
print("-" * 30)

transkrypcja = transkrybuj_audio(NAZWA_PLIKU_AUDIO, model_name=MODEL_WYBRANY)

# Wynik
print("\n=== WYNIK TRANSKRYPCJI ===")
print(transkrypcja)
print("==========================")
