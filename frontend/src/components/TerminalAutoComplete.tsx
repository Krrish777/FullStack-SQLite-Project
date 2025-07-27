import { useState, useEffect } from "react";

interface AutoCompleteProps {
  input: string;
  suggestions: string[];
  onSelect: (suggestion: string) => void;
  visible: boolean;
}

const TerminalAutoComplete = ({ input, suggestions, onSelect, visible }: AutoCompleteProps) => {
  const [selectedIndex, setSelectedIndex] = useState(0);

  useEffect(() => {
    setSelectedIndex(0);
  }, [suggestions]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!visible || suggestions.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % suggestions.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + suggestions.length) % suggestions.length);
      } else if (e.key === 'Tab' || e.key === 'Enter') {
        e.preventDefault();
        onSelect(suggestions[selectedIndex]);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [visible, suggestions, selectedIndex, onSelect]);

  if (!visible || suggestions.length === 0) return null;

  return (
    <div className="absolute bottom-full left-0 mb-2 bg-card border border-border rounded-md shadow-lg max-h-48 overflow-y-auto z-50">
      {suggestions.map((suggestion, index) => (
        <div
          key={suggestion}
          className={`px-3 py-2 text-sm cursor-pointer transition-colors ${
            index === selectedIndex 
              ? 'bg-primary text-primary-foreground' 
              : 'hover:bg-muted'
          }`}
          onClick={() => onSelect(suggestion)}
        >
          <span className="font-mono">{suggestion}</span>
        </div>
      ))}
    </div>
  );
};

export default TerminalAutoComplete;