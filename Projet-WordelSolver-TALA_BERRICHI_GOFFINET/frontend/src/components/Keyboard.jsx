import { cn } from "@/lib/utils";
import { Delete } from "lucide-react";

const KEYBOARD_ROWS = [
  ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
  ["ENTER", "W", "X", "C", "V", "B", "N", "⌫"],
];

export function Keyboard({ letterStates, onKeyPress, disabled = false }) {
  const getKeyClasses = (key) => {
    const state = letterStates.get(key);

    switch (state) {
      case "correct":
        return "bg-[hsl(var(--wordle-correct))] text-foreground glow-correct";
      case "present":
        return "bg-[hsl(var(--wordle-present))] text-foreground glow-present";
      case "absent":
        return "bg-muted text-muted-foreground";
      default:
        return "bg-secondary text-foreground hover:bg-secondary/80";
    }
  };

  return (
    <div className="flex flex-col gap-1.5 sm:gap-2 p-2 sm:p-4">
      {KEYBOARD_ROWS.map((row, rowIndex) => (
        <div key={rowIndex} className="flex justify-center gap-1 sm:gap-1.5">
          {row.map((key) => {
            const isSpecial = key === "ENTER" || key === "⌫";
            return (
              <button
                key={key}
                onClick={() => onKeyPress(key)}
                disabled={disabled}
                className={cn(
                  "flex items-center justify-center rounded-md font-mono-game font-semibold",
                  "transition-all duration-150 active:scale-95",
                  "h-12 sm:h-14",
                  isSpecial ? "px-2 sm:px-4 text-xs sm:text-sm" : "w-8 sm:w-10 text-sm sm:text-base",
                  getKeyClasses(key),
                  disabled && "opacity-50 cursor-not-allowed"
                )}
              >
                {key === "⌫" ? <Delete className="w-5 h-5" /> : key}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}
