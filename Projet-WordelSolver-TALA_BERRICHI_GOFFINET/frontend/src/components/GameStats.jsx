// frontend/src/components/GameStats.jsx
import React from "react";
import { Trophy, RotateCcw, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";

export function GameStats({ 
  isGameOver, 
  isWon, 
  targetWord, 
  attempts, 
  onNewGame,
  language = "fr"
}) {
  if (!isGameOver) return null;

  const translations = {
    fr: {
      congratulations: "Félicitations !",
      won: attempts === 1 
        ? "Vous avez trouvé le mot en 1 tentative !" 
        : `Vous avez trouvé le mot en ${attempts} tentatives !`,
      gameOver: "Partie terminée",
      theWordWas: "Le mot était :",
      newGame: "Nouvelle partie"
    },
    en: {
      congratulations: "Congratulations!",
      won: attempts === 1 
        ? "You found the word in 1 attempt!" 
        : `You found the word in ${attempts} attempts!`,
      gameOver: "Game Over",
      theWordWas: "The word was:",
      newGame: "New Game"
    }
  };

  const t = translations[language] || translations.fr;

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div className="bg-card rounded-2xl border border-border p-6 sm:p-8 max-w-sm w-full text-center shadow-2xl animate-in zoom-in duration-300">
        {isWon ? (
          <>
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/20 flex items-center justify-center animate-bounce">
              <Trophy className="w-8 h-8 text-primary" />
            </div>
            <h2 className="text-2xl font-bold text-foreground mb-2">
              {t.congratulations}
            </h2>
            <p className="text-muted-foreground mb-4">
              {t.won}
            </p>
            <div className="p-4 rounded-lg bg-primary/10 border border-primary/20 mb-4">
              <p className="text-3xl font-bold font-mono text-primary tracking-widest">
                {targetWord}
              </p>
            </div>
          </>
        ) : (
          <>
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-destructive/20 flex items-center justify-center">
              <Clock className="w-8 h-8 text-destructive" />
            </div>
            <h2 className="text-2xl font-bold text-foreground mb-2">
              {t.gameOver}
            </h2>
            <p className="text-muted-foreground mb-2">{t.theWordWas}</p>
            <div className="p-4 rounded-lg bg-muted border border-border mb-4">
              <p className="text-3xl font-bold font-mono text-primary tracking-widest">
                {targetWord}
              </p>
            </div>
          </>
        )}

        <Button 
          onClick={onNewGame} 
          className="w-full gap-2 hover:scale-105 transition-transform"
        >
          <RotateCcw className="w-4 h-4" />
          {t.newGame}
        </Button>
      </div>
    </div>
  );
}