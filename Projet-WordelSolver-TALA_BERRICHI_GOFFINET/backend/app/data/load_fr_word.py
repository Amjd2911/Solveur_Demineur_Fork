# backend/app/data/load_fr_words.py

import os
import unicodedata
import re

def remove_accents(text: str) -> str:
    """
    Supprime tous les accents d'une chaîne de caractères.
    
    Args:
        text: Texte contenant potentiellement des accents
    
    Returns:
        Texte sans accents
    
    Examples:
        >>> remove_accents("CAFÉ")
        'CAFE'
        >>> remove_accents("ÉLÈVE")
        'ELEVE'
    """
    # Normalisation NFD : décompose les caractères accentués
    nfd = unicodedata.normalize('NFD', text)
    # Supprime les caractères de combinaison (accents)
    without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
    return without_accents


def clean_word(word: str) -> str | None:
    """
    Nettoie un mot en supprimant les accents, chiffres et caractères spéciaux.
    
    Args:
        word: Mot à nettoyer
    
    Returns:
        Mot nettoyé en majuscules, ou None si le mot est invalide
    
    Examples:
        >>> clean_word("café123")
        'CAFE'
        >>> clean_word("élève-1")
        'ELEVE'
        >>> clean_word("12345")
        None
    """
    if not word:
        return None
    
    # Convertir en majuscules
    word = word.upper()
    
    # Supprimer les accents
    word = remove_accents(word)
    
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


def load_fr_words(file_path: str | None = None, 
                  clean: bool = True,
                  min_length: int = 2,
                  max_length: int = 15,
                  unique_only: bool = True,
                  verbose: bool = False) -> list[str]:
    """
    Charge tous les mots français depuis un fichier txt avec options de nettoyage.
    Chaque mot doit être sur une ligne séparée dans le fichier.
    
    Args:
        file_path: Chemin vers le fichier txt. Par défaut, cherche 'fr_words.txt'.
        clean: Si True, nettoie les mots (supprime accents, chiffres, etc.)
        min_length: Longueur minimale des mots à conserver (défaut: 2)
        max_length: Longueur maximale des mots à conserver (défaut: 15)
        unique_only: Si True, supprime les doublons (défaut: True)
        verbose: Si True, affiche les statistiques de nettoyage (défaut: False)

    Returns:
        Liste de mots français en majuscules, nettoyés et filtrés.
    
    Examples:
        >>> mots = load_fr_words(clean=True, min_length=5, max_length=5)
        >>> all(len(mot) == 5 for mot in mots)
        True
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "fr_words.txt")
    
    words = []
    stats = {
        'total_lines': 0,
        'empty_lines': 0,
        'with_accents': 0,
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
                mot = line.strip()
                
                # Ignorer les lignes vides
                if not mot:
                    stats['empty_lines'] += 1
                    continue
                
                original_mot = mot
                
                # Nettoyer le mot si demandé
                if clean:
                    # Détecter les caractères à nettoyer (pour stats)
                    if any(c in mot for c in 'àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ'):
                        stats['with_accents'] += 1
                    if any(c.isdigit() for c in mot):
                        stats['with_numbers'] += 1
                    if re.search(r'[^a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ]', mot):
                        stats['with_special_chars'] += 1
                    
                    # Nettoyer
                    mot = clean_word(mot)
                    if not mot:
                        continue
                else:
                    mot = mot.upper()
                
                # Vérifier la validité du mot
                if not is_valid_word(mot, min_length, max_length):
                    if len(mot) < min_length:
                        stats['too_short'] += 1
                    elif len(mot) > max_length:
                        stats['too_long'] += 1
                    continue
                
                words.append(mot)
        
        # Supprimer les doublons si demandé
        if unique_only:
            original_count = len(words)
            words = list(dict.fromkeys(words))  # Préserve l'ordre
            stats['duplicates_removed'] = original_count - len(words)
        
        stats['final_count'] = len(words)
        
        # Afficher les statistiques si verbose
        if verbose:
            print("\n" + "=" * 70)
            print(f"📊 STATISTIQUES DE CHARGEMENT - {os.path.basename(file_path)}")
            print("=" * 70)
            print(f"  Lignes totales lues        : {stats['total_lines']}")
            print(f"  Lignes vides ignorées      : {stats['empty_lines']}")
            if clean:
                print(f"\n  🧹 NETTOYAGE :")
                print(f"     Mots avec accents       : {stats['with_accents']}")
                print(f"     Mots avec chiffres      : {stats['with_numbers']}")
                print(f"     Mots avec caract. spéc. : {stats['with_special_chars']}")
            print(f"\n  📏 FILTRAGE PAR LONGUEUR :")
            print(f"     Trop courts (< {min_length})      : {stats['too_short']}")
            print(f"     Trop longs (> {max_length})       : {stats['too_long']}")
            if unique_only:
                print(f"\n  🔄 Doublons supprimés      : {stats['duplicates_removed']}")
            print(f"\n  ✅ MOTS FINAUX CHARGÉS     : {stats['final_count']}")
            print("=" * 70 + "\n")
        
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {file_path}")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des mots : {e}")
    
    return words


def get_words_by_length(words: list[str], length: int) -> list[str]:
    """
    Filtre les mots par longueur spécifique.
    
    Args:
        words: Liste de mots
        length: Longueur désirée
    
    Returns:
        Liste de mots de la longueur spécifiée
    
    Examples:
        >>> mots = ["CHAT", "CHIEN", "TABLE"]
        >>> get_words_by_length(mots, 5)
        ['CHIEN', 'TABLE']
    """
    return [word for word in words if len(word) == length]


# Test rapide
if __name__ == "__main__":
    print("🧪 TEST DU MODULE load_fr_words.py\n")
    
    # Test 1 : Chargement normal avec nettoyage
    print("=" * 70)
    print("TEST 1 : Chargement avec nettoyage complet")
    print("=" * 70)
    mots = load_fr_words(clean=True, verbose=True)
    print(f"Premiers mots : {mots[:10]}\n")
    
    # Test 2 : Mots de 5 lettres seulement (pour Wordle)
    print("=" * 70)
    print("TEST 2 : Chargement des mots de 5 lettres (Wordle)")
    print("=" * 70)
    mots_5 = load_fr_words(clean=True, min_length=5, max_length=5, verbose=True)
    print(f"Exemples de mots à 5 lettres : {mots_5[:20]}\n")
    
    # Test 3 : Fonctions de nettoyage
    print("=" * 70)
    print("TEST 3 : Fonctions de nettoyage")
    print("=" * 70)
    test_words = ["café", "élève123", "châ_teau", "NAÏVE", "où", "être-là"]
    for word in test_words:
        cleaned = clean_word(word)
        print(f"  '{word}' → '{cleaned}'")
    
    print("\n✅ Tests terminés !\n")