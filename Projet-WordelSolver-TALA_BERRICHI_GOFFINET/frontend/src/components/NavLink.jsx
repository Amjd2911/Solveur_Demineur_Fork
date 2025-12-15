// frontend/src/components/NavLink.jsx
import { NavLink as RouterNavLink } from "react-router-dom";
import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";

export function NavLink({ className, activeClassName, pendingClassName, to, children, ...props }) {
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
    <div className="flex items-center gap-3">
      <RouterNavLink
        to={to}
        className={({ isActive, isPending }) =>
          cn(className, isActive && activeClassName, isPending && pendingClassName)
        }
        {...props}
      >
        {children}
      </RouterNavLink>

      {/* Toggle Dark Mode */}
      <button
        onClick={toggleDarkMode}
        className="relative w-14 h-7 rounded-full bg-secondary/70 dark:bg-secondary/50 transition-colors"
      >
        <span
          className={cn(
            "absolute top-0.5 left-0.5 w-6 h-6 bg-foreground rounded-full shadow-md transition-transform",
            isDark ? "translate-x-7" : "translate-x-0"
          )}
        />
        <span className="absolute left-2 top-0.5 text-xs pointer-events-none">
          {isDark ? "🌙" : "☀️"}
        </span>
      </button>
    </div>
  );
}
