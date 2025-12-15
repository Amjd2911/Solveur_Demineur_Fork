// frontend/src/constants/game.constants.js

// Configuration du jeu
export const GAME_CONFIG = {
    WORD_LENGTH: 5,
    MAX_ATTEMPTS: 6,
    REVEAL_DELAY_MS: 250,
  };
  
  // États possibles d'une lettre
  export const LETTER_STATES = {
    EMPTY: 'empty',
    CORRECT: 'correct',
    PRESENT: 'present',
    ABSENT: 'absent',
  };
  
  // Modes de résolution
  export const SOLVER_MODES = {
    CSP: 'csp',
    HYBRID: 'hybrid',
    AI: 'ai',
  };
  
  // Langues supportées
  export const LANGUAGES = {
    FR: 'fr',
    EN: 'en',
  };
  
  // Messages de toast
  export const TOAST_MESSAGES = {
    fr: {
      wordTooShort: 'Le mot doit contenir 5 lettres',
      wordInvalid: 'Mot invalide',
      serverError: 'Erreur serveur',
      aiSuggestionError: 'Erreur lors de la suggestion IA',
      needAttempt: 'Faites au moins une tentative avant de demander une suggestion',
      gameWon: 'Bravo ! Vous avez gagné !',
      gameLost: 'Perdu ! Le mot était :',
    },
    en: {
      wordTooShort: 'Word must be 5 letters',
      wordInvalid: 'Invalid word',
      serverError: 'Server error',
      aiSuggestionError: 'Error getting AI suggestion',
      needAttempt: 'Make at least one attempt before requesting a suggestion',
      gameWon: 'Congratulations! You won!',
      gameLost: 'Game Over! The word was:',
    },
  };
  
  // Configuration du clavier
  export const KEYBOARD_ROWS = [
    ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M'],
    ['ENTER', 'W', 'X', 'C', 'V', 'B', 'N', '⌫'],
  ];
  
  // Classes CSS pour les états des lettres
  export const LETTER_STATE_CLASSES = {
    [LETTER_STATES.EMPTY]: 'bg-background border-border',
    [LETTER_STATES.CORRECT]: 'bg-[hsl(var(--wordle-correct))] text-card-foreground border-[hsl(var(--wordle-correct))] glow-correct',
    [LETTER_STATES.PRESENT]: 'bg-[hsl(var(--wordle-present))] text-card-foreground border-[hsl(var(--wordle-present))] glow-present',
    [LETTER_STATES.ABSENT]: 'bg-muted text-card-foreground border-muted',
  };
  
  // Labels des modes de résolution
  export const SOLVER_MODE_LABELS = {
    [SOLVER_MODES.CSP]: {
      [LANGUAGES.FR]: 'CSP Seul',
      [LANGUAGES.EN]: 'CSP Only',
    },
    [SOLVER_MODES.HYBRID]: {
      [LANGUAGES.FR]: 'CSP + LLM',
      [LANGUAGES.EN]: 'CSP + LLM',
    },
    [SOLVER_MODES.AI]: {
      [LANGUAGES.FR]: 'IA Pure',
      [LANGUAGES.EN]: 'Pure AI',
    },
  };
  
  // Regex de validation
  export const VALIDATION_REGEX = {
    WORD: /^[a-zA-Z]{5}$/,
    LETTER: /^[a-zA-Z]$/,
  };
  
  // Durées d'animation (ms)
  export const ANIMATION_DURATION = {
    TILE_FLIP: 300,
    TILE_POP: 100,
    ROW_REVEAL: 250,
    KEYBOARD_PRESS: 150,
  };
  
  // LocalStorage keys
  export const STORAGE_KEYS = {
    STATS: 'wordle_stats',
    SETTINGS: 'wordle_settings',
    THEME: 'wordle_theme',
  };