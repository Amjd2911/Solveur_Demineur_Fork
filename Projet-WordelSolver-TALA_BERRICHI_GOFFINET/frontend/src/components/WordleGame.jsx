// frontend/src/components/WordleGame.jsx
import { useState, useCallback, useEffect } from "react";
import { GameBoard } from "./GameBoard";
import { Keyboard } from "./Keyboard";
import { SolverPanel } from "./SolverPanel";
import { GameStats } from "./GameStats";
import { toast } from "sonner";
import { Brain, Gamepad2, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DarkModeToggle } from "./DarkModeToggle";
import axios from "axios";
import {evaluateGuess, buildFeedback, isValidWord, normalizeWord, getFeedbackMessage} from "@/utils/wordle.utils";


const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const MAX_ATTEMPTS = 6;

export function WordleGame() {
  const [language, setLanguage] = useState("fr");
  const [solverMode, setSolverMode] = useState("hybrid");
  const [targetWord, setTargetWord] = useState("");
  const [guesses, setGuesses] = useState([]);
  const [results, setResults] = useState([]);
  const [currentGuess, setCurrentGuess] = useState("");
  const [letterStates, setLetterStates] = useState(new Map());
  const [isRevealing, setIsRevealing] = useState(false);
  const [isGameOver, setIsGameOver] = useState(false);
  const [isWon, setIsWon] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState("");
  const [isLoadingAI, setIsLoadingAI] = useState(false);
  const [candidatesCount, setCandidatesCount] = useState(0);
  const [cspCandidates, setCspCandidates] = useState([]);

  const currentRow = guesses.length;
  

  const updateLetterStates = useCallback((newResults) => {
    setLetterStates((prev) => {
      const updated = new Map(prev);
      for (const result of newResults) {
        const current = updated.get(result.letter);
        if (
          !current ||
          (current === "absent" && result.state !== "absent") ||
          (current === "present" && result.state === "correct")
        ) {
          updated.set(result.letter, result.state);
        }
      }
      return updated;
    });
  }, []);

  const submitGuess = useCallback(async () => {
    if (!isValidWord(currentGuess)) {
      toast.error(language === "fr" ? "Le mot doit contenir 5 lettres" : "Word must be 5 letters");
      return;
    }
  
    setIsRevealing(true);
  
    try {
      let secret = targetWord;
  
      // Si le mot cible n'est pas encore défini, demander au backend
      if (!targetWord) {
        const feedback = buildFeedback(results);
  
        let endpoint;
        if (solverMode === "csp") endpoint = "/wordle/guess/csp";
        else if (solverMode === "hybrid") endpoint = "/wordle/guess/hybrid";
        else endpoint = "/wordle/suggest-ai";
  
        const res = await axios.post(`${API_BASE_URL}${endpoint}`, {
          feedback,
          language
        });
  
        secret = (res.data.next_guess || res.data.suggested_word).toUpperCase();
        setTargetWord(secret);
      }
  
      // Évaluer la tentative
      const resultRow = evaluateGuess(normalizeWord(currentGuess), normalizeWord(secret));
      setGuesses(prev => [...prev, currentGuess.toUpperCase()]);
      setResults(prev => [...prev, resultRow]);
      updateLetterStates(resultRow);
      setCurrentGuess("");
  
      const attemptCount = guesses.length + 1;
      let feedbackMessage = "";
  
      if (currentGuess.toLowerCase() === secret.toLowerCase()) {
        setIsWon(true);
        setIsGameOver(true);
        feedbackMessage = getFeedbackMessage(true, attemptCount, language);
        toast.success(feedbackMessage);
      } else if (attemptCount >= MAX_ATTEMPTS) {
        setIsGameOver(true);
        feedbackMessage = getFeedbackMessage(false, attemptCount, language);
        toast.error(`${feedbackMessage} ${language === "fr" ? "Le mot était :" : "The word was:"} ${secret.toUpperCase()}`);
      }
  
      setIsRevealing(false);
    } catch (error) {
      console.error("❌ Erreur:", error);
      const errorMsg = error.response?.data?.detail || (language === "fr" ? "Erreur serveur" : "Server error");
      toast.error(errorMsg);
      setIsRevealing(false);
    }
  }, [currentGuess, results, guesses, updateLetterStates, language, targetWord, solverMode]);
  

  const handleKeyPress = useCallback(
    (key) => {
      if (isGameOver || isRevealing) return;
      if (key === "ENTER") submitGuess();
      else if (key === "⌫") setCurrentGuess((prev) => prev.slice(0, -1));
      else if (currentGuess.length < 5 && /^[A-Z]$/i.test(key)) 
        setCurrentGuess((prev) => prev + key.toUpperCase());
    },
    [currentGuess, isGameOver, isRevealing, submitGuess]
  );

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === "Enter") handleKeyPress("ENTER");
      else if (e.key === "Backspace") handleKeyPress("⌫");
      else if (/^[a-zA-Z]$/.test(e.key)) handleKeyPress(e.key.toUpperCase());
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyPress]);

  const handleNewGame = useCallback(() => {
    setTargetWord("");
    setGuesses([]);
    setResults([]);
    setCurrentGuess("");
    setLetterStates(new Map());
    setIsGameOver(false);
    setIsWon(false);
    setAiSuggestion("");
    setCandidatesCount(0);
    setCspCandidates([]);
  }, []);

  const handleRequestAI = useCallback(async () => {
    if (results.length === 0) {
      toast.info(language === "fr" ? "Faites au moins une tentative" : "Make at least one attempt");
      return;
    }

    setIsLoadingAI(true);
    try {
      const feedback = buildFeedback(results);
      const convertFeedback = {
        green: Object.fromEntries(Object.entries(feedback.green).map(([k,v]) => [parseInt(k), v])),
        yellow: Object.fromEntries(Object.entries(feedback.yellow).map(([k,v]) => [parseInt(k), v])),
        grey: feedback.grey
      };

      const res = await axios.post(`${API_BASE_URL}/wordle/suggest-ai`, {
        feedback: convertFeedback,
        language,
        previous_guesses: guesses.map(g => g.toLowerCase())
      });

      setAiSuggestion(res.data.suggested_word.toUpperCase());
      setCandidatesCount(res.data.candidates_count || 0);
      toast.success(language === "fr" ? `Suggestion IA: ${res.data.suggested_word}` : `AI Suggestion: ${res.data.suggested_word}`, {
        description: res.data.explanation, duration: 5000
      });
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.detail || "Erreur");
    } finally {
      setIsLoadingAI(false);
    }
  }, [results, language, guesses]);
  

  // Nouvelle fonction pour les suggestions CSP
  const handleRequestCSP = useCallback(async () => {
    if (results.length === 0) {
      toast.info(language === "fr" ? "Faites au moins une tentative" : "Make at least one attempt");
      return;
    }

    setIsLoadingAI(true);
    try {
      const feedback = buildFeedback(results);
      const res = await axios.post(`${API_BASE_URL}/wordle/guess/csp`, { feedback, language });

      setAiSuggestion(res.data.next_guess.toUpperCase());
      setCspCandidates(res.data.candidates || []); 
      setCandidatesCount(res.data.candidates?.length || 0);
      toast.success(language === "fr" ? `Suggestion CSP: ${res.data.next_guess}` : `CSP Suggestion: ${res.data.next_guess}`, {
        description: res.data.explanation, duration: 5000
      });
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.detail || "Erreur");
    } finally {
      setIsLoadingAI(false);
    }
  }, [results, language]);

  // Nouvelle fonction pour les suggestions hybrides
  const handleRequestHybrid = useCallback(async () => {
    if (results.length === 0) {
      toast.info(language === "fr" ? "Faites au moins une tentative" : "Make at least one attempt");
      return;
    }

    setIsLoadingAI(true);
    try {
      const feedback = buildFeedback(results);
      const res = await axios.post(`${API_BASE_URL}/wordle/guess/hybrid`, { feedback, language });

      setAiSuggestion(res.data.next_guess.toUpperCase());
      setCspCandidates(res.data.candidates || []); 
      setCandidatesCount(res.data.candidates?.length || 0);
      toast.success(language === "fr" ? `Suggestion Hybride: ${res.data.next_guess}` : `Hybrid Suggestion: ${res.data.next_guess}`, {
        description: res.data.explanation, duration: 5000
      });
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.detail || "Erreur");
    } finally {
      setIsLoadingAI(false);
    }
  }, [results, language]);

  const handleLanguageSwitch = useCallback(() => {
    setLanguage((prev) => (prev === "fr" ? "en" : "fr"));
    handleNewGame();
  }, [handleNewGame]);

  const handleSolverModeSwitch = useCallback(() => {
    setSolverMode((prev) => {
      if (prev === "csp") return "hybrid";
      if (prev === "hybrid") return "ai";
      return "csp";
    });
    handleNewGame();
  }, [handleNewGame]);

  const solverModeLabel = {
    csp: language === "fr" ? "CSP Seul" : "CSP Only",
    hybrid: language === "fr" ? "CSP + LLM" : "CSP + LLM",
    ai: language === "fr" ? "IA Pure" : "Pure AI"
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/20">
              <img
                src="/Wordle_Lockup.png"
                alt="Wordle logo"
                className="w-12 h-12"
              />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">Wordle CSP</h1>
              <p className="text-xs text-muted-foreground">
                {language === "fr"
                  ? "Solveur par contraintes + LLM"
                  : "CSP Solver + LLM"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleLanguageSwitch}
              className="flex items-center gap-2 hover:bg-primary hover:text-primary-foreground hover:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <Globe className="w-4 h-4" />
              <span className="font-medium">
                {language === "fr" ? "FR" : "EN"}
              </span>
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleSolverModeSwitch}
              className="flex items-center gap-2 hover:bg-primary hover:text-primary-foreground hover:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <Brain className="w-4 h-4" />
              <span className="font-medium text-xs">
                {solverModeLabel[solverMode]}
              </span>
            </Button>
            <DarkModeToggle />
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6 justify-center items-start">
          <div className="flex flex-col items-center">
            <div className="mb-4 text-center">
              <h1 className="text-3xl font-bold text-wordle">
                Wordle <span className="text-foreground">Solver</span>
              </h1>
              <p className="text-sm text-muted-foreground">
                {language === "fr"
                  ? "Devinez moins, gagnez plus !"
                  : "Guess less, win more!"}
              </p>
              <p className="text-xs text-accent mt-1">
                Mode: {solverModeLabel[solverMode]}
              </p>
            </div>
            <GameBoard
              guesses={guesses}
              results={results}
              currentGuess={currentGuess}
              currentRow={currentRow}
              isRevealing={isRevealing}
            />
            <Keyboard
              letterStates={letterStates}
              onKeyPress={handleKeyPress}
              disabled={isGameOver || isRevealing}
            />
          </div>
          <div className="w-full lg:w-80">
            <SolverPanel
              solverData={{
                remainingCount: candidatesCount,
                topSuggestions: [],
                entropy: 0,
                bestGuess: null,
                possibleWords: [],
              }}
              isLoading={isLoadingAI}
              aiSuggestion={aiSuggestion}
              onRequestAI={handleRequestAI}
              onRequestCSP={handleRequestCSP}
              onRequestHybrid={handleRequestHybrid}
              language={language}
              solverMode={solverMode}
            />
          </div>
        </div>
      </main>

      <GameStats
        isGameOver={isGameOver}
        isWon={isWon}
        targetWord={targetWord}
        attempts={guesses.length}
        onNewGame={handleNewGame}
        language={language}
      />
    </div>
  );
}

export default WordleGame;