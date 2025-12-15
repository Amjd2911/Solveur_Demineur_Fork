# backend/app/data/load_en_words.py

import os
import re

def clean_word(word: str) -> str | None:
    """
    Nettoie un mot en supprimant les chiffres et caractères spéciaux.
    
    Args:
        word: Mot à nettoyer
    
    Returns:
        Mot nettoyé en majuscules, ou None si le mot est invalide
    
    Examples:
        >>> clean_word("hello123")
        'HELLO'
        >>> clean_word("world-1")
        'WORLD'
        >>> clean_word("12345")
        None
    """
    if not word:
        return None
    
    # Convertir en majuscules
    word = word.upper()
    
    # Supprimer tous les caractères qui ne sont pas des lettres (A-Z)
    word = re.sub(r'[^A-Z]', '', word)
    
    # Retourner None si le mot est vide après nettoyage
    return word if word else None


def is_valid_word(word: str, min_length: int = 2, max_length: int = 15) -> bool:
    """
    Vérifie si un mot est valide (longueur, caractères alphabétiques uniquement).
    
    Args:
        word: Mot à vérifier
        min_length: Longueur minimale acceptée (défaut: 2)
        max_length: Longueur maximale acceptée (défaut: 15)
    
    Returns:
        True si le mot est valide, False sinon
    """
    if not word:
        return False
    
    # Vérifier que le mot contient uniquement des lettres
    if not word.isalpha():
        return False
    
    # Vérifier la longueur
    return min_length <= len(word) <= max_length


def load_en_words(file_path: str | None = None,
                  clean: bool = True,
                  min_length: int = 2,
                  max_length: int = 15,
                  unique_only: bool = True,
                  verbose: bool = False) -> list[str]:
    """
    Charge tous les mots anglais depuis un fichier txt avec options de nettoyage.
    Chaque mot doit être sur une ligne séparée dans le fichier.
    
    Args:
        file_path: Chemin vers le fichier txt. Par défaut, cherche 'en_words.txt'.
        clean: Si True, nettoie les mots (supprime chiffres, caractères spéciaux)
        min_length: Longueur minimale des mots à conserver (défaut: 2)
        max_length: Longueur maximale des mots à conserver (défaut: 15)
        unique_only: Si True, supprime les doublons (défaut: True)
        verbose: Si True, affiche les statistiques de nettoyage (défaut: False)

    Returns:
        Liste de mots anglais en majuscules, nettoyés et filtrés.
    
    Examples:
        >>> words = load_en_words(clean=True, min_length=5, max_length=5)
        >>> all(len(word) == 5 for word in words)
        True
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "en_words.txt")
    
    words = []
    stats = {
        'total_lines': 0,
        'empty_lines': 0,
        'with_numbers': 0,
        'with_special_chars': 0,
        'too_short': 0,
        'too_long': 0,
        'duplicates_removed': 0,
        'final_count': 0
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stats['total_lines'] += 1
                word = line.strip()
                
                # Ignorer les lignes vides
                if not word:
                    stats['empty_lines'] += 1
                    continue
                
                # Nettoyer le mot si demandé
                if clean:
                    # Détecter les caractères à nettoyer (pour stats)
                    if any(c.isdigit() for c in word):
                        stats['with_numbers'] += 1
                    if re.search(r'[^a-zA-Z]', word):
                        stats['with_special_chars'] += 1
                    
                    # Nettoyer
                    word = clean_word(word)
                    if not word:
                        continue
                else:
                    word = word.upper()
                
                # Vérifier la validité du mot
                if not is_valid_word(word, min_length, max_length):
                    if len(word) < min_length:
                        stats['too_short'] += 1
                    elif len(word) > max_length:
                        stats['too_long'] += 1
                    continue
                
                words.append(word)
        
        # Supprimer les doublons si demandé
        if unique_only:
            original_count = len(words)
            words = list(dict.fromkeys(words))  # Préserve l'ordre
            stats['duplicates_removed'] = original_count - len(words)
        
        stats['final_count'] = len(words)
        
        # Afficher les statistiques si verbose
        if verbose:
            print("\n" + "=" * 70)
            print(f"📊 STATISTICS - {os.path.basename(file_path)}")
            print("=" * 70)
            print(f"  Total lines read           : {stats['total_lines']}")
            print(f"  Empty lines ignored        : {stats['empty_lines']}")
            if clean:
                print(f"\n  🧹 CLEANING :")
                print(f"     Words with numbers      : {stats['with_numbers']}")
                print(f"     Words with special char : {stats['with_special_chars']}")
            print(f"\n  📏 LENGTH FILTERING :")
            print(f"     Too short (< {min_length})       : {stats['too_short']}")
            print(f"     Too long (> {max_length})        : {stats['too_long']}")
            if unique_only:
                print(f"\n  🔄 Duplicates removed      : {stats['duplicates_removed']}")
            print(f"\n  ✅ FINAL WORDS LOADED      : {stats['final_count']}")
            print("=" * 70 + "\n")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error loading words: {e}")
    
    return words


def get_words_by_length(words: list[str], length: int) -> list[str]:
    """
    Filters words by specific length.
    
    Args:
        words: List of words
        length: Desired length
    
    Returns:
        List of words with specified length
    
    Examples:
        >>> words = ["CAT", "MOUSE", "TABLE"]
        >>> get_words_by_length(words, 5)
        ['MOUSE', 'TABLE']
    """
    return [word for word in words if len(word) == length]


# Quick test
if __name__ == "__main__":
    print("🧪 TEST OF load_en_words.py MODULE\n")
    
    # Test 1: Normal loading with cleaning
    print("=" * 70)
    print("TEST 1: Loading with complete cleaning")
    print("=" * 70)
    words = load_en_words(clean=True, verbose=True)
    print(f"First words: {words[:10]}\n")
    
    # Test 2: 5-letter words only (for Wordle)
    print("=" * 70)
    print("TEST 2: Loading 5-letter words (Wordle)")
    print("=" * 70)
    words_5 = load_en_words(clean=True, min_length=5, max_length=5, verbose=True)
    print(f"Examples of 5-letter words: {words_5[:20]}\n")
    
    # Test 3: Cleaning functions
    print("=" * 70)
    print("TEST 3: Cleaning functions")
    print("=" * 70)
    test_words = ["hello123", "world-456", "test_word", "GOOD", "bad!"]
    for word in test_words:
        cleaned = clean_word(word)
        print(f"  '{word}' → '{cleaned}'")
    
    print("\n✅ Tests completed!\n")