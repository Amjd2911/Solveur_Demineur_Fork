// frontend/src/utils/wordle.utils.js

/**
 * Évalue un mot deviné contre le mot cible
 * Retourne un tableau d'objets {letter, state}
 * 
 * @param {string} guess - Le mot deviné (ex: "ARBRE")
 * @param {string} target - Le mot cible (ex: "FLEUR")
 * @returns {Array<{letter: string, state: string}>}
 */
export function evaluateGuess(guess, target) {
    if (!target) return guess.split("").map(letter => ({ letter, state: "empty" }));
    
    const result = [];
    const targetLetters = target.toUpperCase().split("");
    const guessLetters = guess.toUpperCase().split("");
    const targetCounts = {};
    
    targetLetters.forEach(letter => {
      targetCounts[letter] = (targetCounts[letter] || 0) + 1;
    });
    
    guessLetters.forEach((letter, idx) => {
      if (targetLetters[idx] === letter) {
        result[idx] = { letter, state: "correct" };
        targetCounts[letter]--;
      } else {
        result[idx] = { letter, state: null };
      }
    });
    
    guessLetters.forEach((letter, idx) => {
      if (result[idx].state === null) {
        if (targetCounts[letter] > 0) {
          result[idx] = { letter, state: "present" };
          targetCounts[letter]--;
        } else {
          result[idx] = { letter, state: "absent" };
        }
      }
    });
    
    return result;
  }
  
  /**
   * Construit un objet feedback au format backend depuis les résultats
   * 
   * @param {Array<Array<{letter: string, state: string}>>} results - Tous les résultats des tentatives
   * @returns {{green: Object, yellow: Object, grey: Array}}
   */
export function buildFeedback(results) {
  const feedback = {
    green: {},
    yellow: {},
    grey: []
  };
  
  const greenLetters = new Set();
  const yellowLetters = new Set();
  
  results.forEach((row) => {
    row.forEach((cell, idx) => {
      const letter = cell.letter.toLowerCase();
      
      if (cell.state === "correct") {
        feedback.green[idx] = letter;
        greenLetters.add(letter);
      } else if (cell.state === "present") {
        if (!feedback.yellow[idx]) {
          feedback.yellow[idx] = [];
        }
        if (!feedback.yellow[idx].includes(letter)) {
          feedback.yellow[idx].push(letter);
        }
        yellowLetters.add(letter);
      } else if (cell.state === "absent") {
        const isGreenOrYellow = greenLetters.has(letter) || yellowLetters.has(letter);
        if (!isGreenOrYellow && !feedback.grey.includes(letter)) {
          feedback.grey.push(letter);
        }
      }
    });
  });
  
  return feedback;
}
  
  /**
   * Vérifie si un mot est valide (5 lettres, alphabétique)
   * 
   * @param {string} word - Le mot à vérifier
   * @returns {boolean}
   */
  export function isValidWord(word) {
    if (!word || typeof word !== 'string') return false;
    return word.length === 5 && /^[a-zA-Z]+$/.test(word);
  }
  
  /**
   * Normalise un mot (uppercase, trim)
   * 
   * @param {string} word - Le mot à normaliser
   * @returns {string}
   */
  export function normalizeWord(word) {
    if (!word) return "";
    return word.trim().toUpperCase();
  }
  
  /**
   * Calcule les statistiques du jeu
   * 
   * @param {Array} guesses - Liste des tentatives
   * @param {boolean} isWon - Le joueur a-t-il gagné ?
   * @returns {{attempts: number, success: boolean, successRate: number}}
   */
  export function calculateStats(guesses, isWon) {
    return {
      attempts: guesses.length,
      success: isWon,
      successRate: isWon ? 100 : 0
    };
  }
  
  /**
   * Génère un message de feedback selon le résultat
   * 
   * @param {boolean} isWon - Le joueur a-t-il gagné ?
   * @param {number} attempts - Nombre de tentatives
   * @param {string} language - Langue ("fr" ou "en")
   * @returns {string}
   */
  export function getFeedbackMessage(isWon, attempts, language = "fr") {
    const messages = {
      fr: {
        win: [
          "Génial ! 🎉",
          "Excellent ! 👏",
          "Bravo ! 🎊",
          "Magnifique ! ⭐",
          "Parfait ! 💯",
          "Impressionnant ! 🔥"
        ],
        lose: [
          "Presque ! Réessayez 💪",
          "Ce n'est pas grave, continuez ! 🎯",
          "Vous y êtes presque ! 🚀"
        ]
      },
      en: {
        win: [
          "Awesome! 🎉",
          "Excellent! 👏",
          "Well done! 🎊",
          "Amazing! ⭐",
          "Perfect! 💯",
          "Impressive! 🔥"
        ],
        lose: [
          "Almost! Try again 💪",
          "Don't give up! 🎯",
          "You're getting closer! 🚀"
        ]
      }
    };
    
    const lang = messages[language] || messages.fr;
    const pool = isWon ? lang.win : lang.lose;
    
    // Sélectionner un message en fonction du nombre de tentatives
    if (isWon) {
      if (attempts === 1) return pool[4]; // Parfait !
      if (attempts <= 3) return pool[0]; // Génial !
      if (attempts <= 4) return pool[1]; // Excellent !
      return pool[2]; // Bravo !
    } else {
      return pool[Math.floor(Math.random() * pool.length)];
    }
  }
  
  /**
   * Sauvegarde les stats dans le localStorage
   * 
   * @param {Object} stats - Statistiques à sauvegarder
   */
  export function saveStats(stats) {
    try {
      const existing = localStorage.getItem('wordle_stats');
      const allStats = existing ? JSON.parse(existing) : [];
      allStats.push({
        ...stats,
        timestamp: new Date().toISOString()
      });
      localStorage.setItem('wordle_stats', JSON.stringify(allStats));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde des stats:', error);
    }
  }
  
  /**
   * Récupère les stats depuis le localStorage
   * 
   * @returns {Array<Object>}
   */
  export function loadStats() {
    try {
      const stats = localStorage.getItem('wordle_stats');
      return stats ? JSON.parse(stats) : [];
    } catch (error) {
      console.error('Erreur lors du chargement des stats:', error);
      return [];
    }
  }