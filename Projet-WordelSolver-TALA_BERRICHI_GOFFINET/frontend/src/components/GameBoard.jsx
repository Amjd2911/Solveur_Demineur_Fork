// frontend/src/components/GameBoard.jsx
import React from "react";
import { GameTile } from "./GameTile";

export function GameBoard({ guesses, results, currentGuess, currentRow, isRevealing }) {
  const rows = [];

  for (let i = 0; i < 6; i++) {
    const tiles = [];

    for (let j = 0; j < 5; j++) {
      let letter = "";
      let state = "empty"; // 'empty', 'correct', 'present', 'absent'

      if (results[i]) {
        // Lignes déjà validées
        letter = guesses[i]?.[j] || "";
        state = results[i][j]?.state || "empty";
      } else if (i === currentRow) {
        // Ligne en cours de saisie
        letter = currentGuess[j] || "";
        state = "empty";
      }

      tiles.push(
        <GameTile
          key={`${i}-${j}`}
          letter={letter}
          state={state}
          isRevealing={isRevealing && results[i]} // Reveal seulement si ligne validée
          delay={j}
          isCurrentRow={i === currentRow}
        />
      );
    }

    rows.push(
      <div key={i} className="flex gap-1.5 sm:gap-2">
        {tiles}
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1.5 sm:gap-2 p-4">
      {rows}
    </div>
  );
}
