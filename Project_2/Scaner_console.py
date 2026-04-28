import sys
import os
from collections import Counter

def analyze_text(text):
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    unique_words = len(set(words))
    sentences = text.count('.') + text.count('!') + text.count('?')
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    
    top_words = Counter(words).most_common(3) if words else []
    
    print("\n" + "="*50)
    print("✨ РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ")
    print("="*50)
    print(f"📝 Слов: {word_count}")
    print(f"🔤 Символов: {char_count}")
    print(f"✨ Уникальных слов: {unique_words}")
    print(f"💬 Предложений: {sentences}")
    print(f"📊 Сред. длина слова: {avg_word_len:.1f}")
    print("\n🏆 Самые частые слова:")
    if top_words:
        for w, c in top_words:
            print(f"  • {w}: {c}")
    else:
        print("  (нет данных)")
    print("="*50 + "\n")

def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"📄 Анализ файла: {filepath}")
            analyze_text(text)
        else:
            print(f"❌ Файл не найден: {filepath}")
    else:
        print("💬 Введите текст (Ctrl+D для завершения):")
        text = sys.stdin.read()
        analyze_text(text)

if __name__ == "__main__":
    main()
