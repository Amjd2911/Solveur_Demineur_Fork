// frontend/src/components/DarkModeToggle.jsx
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

export function DarkModeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const html = document.documentElement;
    setIsDark(html.classList.contains("dark"));
  }, []);

  const toggleDarkMode = () => {
    const html = document.documentElement;
    html.classList.toggle("dark");
    setIsDark(html.classList.contains("dark"));
  };

  return (
<button
  onClick={toggleDarkMode}
  aria-label="Toggle dark mode"
  className="
    relative w-14 h-7 rounded-full
    bg-secondary/70 dark:bg-secondary/40
    transition-colors duration-300
    hover:bg-secondary
    focus:outline-none focus:ring-2 focus:ring-primary/50
  "
>
  {/* Thumb */}
  <span
    className={cn(
      "absolute top-0.5 left-0.5 w-6 h-6 rounded-full bg-background shadow-lg",
      "flex items-center justify-center text-sm",
      "transition-transform duration-300 ease-in-out",
      isDark ? "translate-x-7" : "translate-x-0"
    )}
  >
    {isDark ? "☾" : "☀︎"}
  </span>

  {/* Background icon (subtil) */}
  <span className="absolute inset-0 flex items-center justify-between px-2 text-xs opacity-60 pointer-events-none">
    <span>☀︎</span>
    <span>☾</span>
  </span>
</button>
  );
}
