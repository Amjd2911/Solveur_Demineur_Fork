import { useState } from 'react';
import { useStore } from '../store/useStore';
import { apiService } from '../services/api';
import { Play, Settings } from 'lucide-react';

export default function SolverControls() {
  const { selectedInstance, setSolution, setError, setSolving } = useStore();
  const [timeLimit, setTimeLimit] = useState<number>(8);
  const [numWorkers, setNumWorkers] = useState<number>(8);

  const handleSolve = async () => {
    if (!selectedInstance) {
      setError('Please select an instance first');
      return;
    }

    setSolving(true);
    setError(null);

    try {
      const solution = await apiService.solveInstance({
        instance_name: selectedInstance,
        time_limit: timeLimit > 0 ? timeLimit : undefined,
        num_workers: numWorkers,
      });

      setSolution(solution);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to solve instance');
    } finally {
      setSolving(false);
    }
  };

  return (
    <div className="card-hover p-0">
      <div className="space-y-4 p-6">
        {/* Time Limit */}
        <div>
          <label className="block text-sm font-semibold text-white/90 mb-2">
            Time Limit (seconds)
          </label>
          <input
            type="number"
            min="0"
            max="60"
            step="0.5"
            value={timeLimit}
            onChange={(e) => setTimeLimit(parseFloat(e.target.value))}
            className="input-field"
          />
          <p className="text-xs text-white/60 mt-1">
            Set to 0 for unlimited time
          </p>
        </div>

        {/* Number of Workers */}
        <div>
          <label className="block text-sm font-semibold text-white/90 mb-2">
            Parallel Workers
          </label>
          <input
            type="number"
            min="1"
            max="16"
            value={numWorkers}
            onChange={(e) => setNumWorkers(parseInt(e.target.value))}
            className="input-field"
          />
          <p className="text-xs text-white/60 mt-1">
            Number of parallel search workers (1-16)
          </p>
        </div>
      </div>
      
      {/* Solve Button */}
      <div className="border-t border-white/10 p-4">
        <button
          onClick={handleSolve}
          disabled={!selectedInstance}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="w-4 h-4" />
          Solve Instance
        </button>
      </div>
    </div>
  );
}
