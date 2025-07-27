import { useState, useEffect, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Database, Zap, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import TerminalAutoComplete from "@/components/TerminalAutoComplete";
import { highlightSQLCommand, getSQLSuggestions } from "@/utils/sqlSyntaxHighlighter";
import TutorialMode, { TutorialButton } from "@/components/TutorialMode";
import ThemeSwitcher, { themes, TerminalTheme } from "@/components/ThemeSwitcher";

interface TerminalLine {
  type: 'command' | 'output' | 'error' | 'system' | 'performance';
  content: string;
  timestamp?: Date;
  isTyping?: boolean;
  executionTime?: number;
}

interface Table {
  name: string;
  columns: { name: string; type: string }[];
  data: Record<string, any>[];
}

const Demo = () => {
  const [input, setInput] = useState("");
  const [multiLineInput, setMultiLineInput] = useState<string[]>([""]);
  const [currentLine, setCurrentLine] = useState(0);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [lines, setLines] = useState<TerminalLine[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showAutoComplete, setShowAutoComplete] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isMultiLine, setIsMultiLine] = useState(false);
  const [isTutorialActive, setIsTutorialActive] = useState(false);
  const [currentTheme, setCurrentTheme] = useState<TerminalTheme>(themes[0]);
  const [showThemeSettings, setShowThemeSettings] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);

  // Mock database
  const [tables, setTables] = useState<Table[]>([
    {
      name: 'users',
      columns: [
        { name: 'id', type: 'INTEGER' },
        { name: 'name', type: 'TEXT' },
        { name: 'email', type: 'TEXT' },
        { name: 'age', type: 'INTEGER' }
      ],
      data: [
        { id: 1, name: 'Alice Johnson', email: 'alice@example.com', age: 28 },
        { id: 2, name: 'Bob Smith', email: 'bob@example.com', age: 35 },
        { id: 3, name: 'Carol Davis', email: 'carol@example.com', age: 24 }
      ]
    },
    {
      name: 'products',
      columns: [
        { name: 'id', type: 'INTEGER' },
        { name: 'name', type: 'TEXT' },
        { name: 'price', type: 'REAL' },
        { name: 'category', type: 'TEXT' }
      ],
      data: [
        { id: 1, name: 'Laptop', price: 999.99, category: 'Electronics' },
        { id: 2, name: 'Coffee Mug', price: 12.50, category: 'Kitchen' },
        { id: 3, name: 'Book', price: 24.99, category: 'Education' }
      ]
    }
  ]);

  const addLine = useCallback((content: string, type: TerminalLine['type'] = 'output', options?: { isTyping?: boolean; executionTime?: number }) => {
    setLines(prev => [...prev, { 
      content, 
      type, 
      timestamp: new Date(),
      isTyping: options?.isTyping,
      executionTime: options?.executionTime
    }]);
  }, []);

  const typewriterEffect = useCallback(async (text: string, type: TerminalLine['type'] = 'output') => {
    const words = text.split(' ');
    let currentText = '';
    
    for (let i = 0; i < words.length; i++) {
      currentText += (i > 0 ? ' ' : '') + words[i];
      setLines(prev => {
        const newLines = [...prev];
        if (newLines.length > 0 && newLines[newLines.length - 1].isTyping) {
          newLines[newLines.length - 1] = {
            ...newLines[newLines.length - 1],
            content: currentText
          };
        } else {
          newLines.push({ content: currentText, type, timestamp: new Date(), isTyping: true });
        }
        return newLines;
      });
      await new Promise(resolve => setTimeout(resolve, 50));
    }
    
    // Mark as completed
    setLines(prev => {
      const newLines = [...prev];
      if (newLines.length > 0 && newLines[newLines.length - 1].isTyping) {
        newLines[newLines.length - 1] = {
          ...newLines[newLines.length - 1],
          isTyping: false
        };
      }
      return newLines;
    });
  }, []);

  const welcomeMessage = () => {
    addLine("", 'system');
    addLine("╔══════════════════════════════════════════════════════════════╗", 'system');
    addLine("║            SQLite-Like Database Engine Demo                  ║", 'system');
    addLine("║                      Version 1.0.0                          ║", 'system');
    addLine("║                   Enhanced Terminal Mode                     ║", 'system');
    addLine("╚══════════════════════════════════════════════════════════════╝", 'system');
    addLine("", 'system');
    addLine("🚀 Features: Syntax Highlighting • Auto-completion • Multi-line Support", 'system');
    addLine("", 'system');
    addLine("Quick Start Commands:", 'system');
    addLine("  • help                    - Show all available commands", 'system');
    addLine("  • show tables            - List database tables", 'system');
    addLine("  • select * from users    - Query user data", 'system');
    addLine("  • describe users         - Show table schema", 'system');
    addLine("", 'system');
    addLine("💡 Tips: Use Tab for auto-completion, Ctrl+Enter for multi-line", 'system');
    addLine("", 'system');
  };

  useEffect(() => {
    welcomeMessage();
  }, []);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [lines]);

  const executeCommand = async (command: string) => {
    const trimmedCommand = command.trim().toLowerCase();
    const startTime = performance.now();
    
    // Add command with syntax highlighting
    setLines(prev => [...prev, { 
      content: `sqlite-engine@demo:~$ ${command}`, 
      type: 'command', 
      timestamp: new Date() 
    }]);
    
    setIsProcessing(true);

    // Realistic processing simulation
    const processingTime = Math.random() * 400 + 150;
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    const executionTime = performance.now() - startTime;

    if (trimmedCommand === 'help') {
      addLine("Available Commands:", 'output');
      addLine("  help                     - Show this help message", 'output');
      addLine("  show tables             - List all tables", 'output');
      addLine("  describe <table>        - Show table schema", 'output');
      addLine("  select * from <table>   - Show table data", 'output');
      addLine("  insert into <table>...  - Insert new record", 'output');
      addLine("  update <table>...       - Update records", 'output');
      addLine("  delete from <table>...  - Delete records", 'output');
      addLine("  clear                   - Clear screen", 'output');
      addLine("  exit                    - Return to home page", 'output');
    } else if (trimmedCommand === 'show tables') {
      addLine("Tables in database:", 'output');
      tables.forEach(table => {
        addLine(`  ${table.name}`, 'output');
      });
      addLine("", 'output');
      addLine(`📋 Found ${tables.length} tables • ⚡ ${executionTime.toFixed(2)}ms`, 'performance');
    } else if (trimmedCommand.startsWith('describe ')) {
      const tableName = trimmedCommand.split(' ')[1];
      const table = tables.find(t => t.name === tableName);
      if (table) {
        addLine(`Schema for table '${table.name}':`, 'output');
        addLine("┌─────────────────┬─────────────────┐", 'output');
        addLine("│ Column Name     │ Data Type       │", 'output');
        addLine("├─────────────────┼─────────────────┤", 'output');
        table.columns.forEach(col => {
          addLine(`│ ${col.name.padEnd(15)} │ ${col.type.padEnd(15)} │`, 'output');
        });
        addLine("└─────────────────┴─────────────────┘", 'output');
        addLine("", 'output');
        addLine(`📝 Schema displayed • ⚡ ${executionTime.toFixed(2)}ms`, 'performance');
      } else {
        addLine(`Error: Table '${tableName}' not found`, 'error');
      }
    } else if (trimmedCommand.startsWith('select * from ')) {
      const tableName = trimmedCommand.split(' ')[3];
      const table = tables.find(t => t.name === tableName);
      if (table && table.data.length > 0) {
        const headers = table.columns.map(col => col.name);
        const colWidths = headers.map(header => Math.max(header.length, 12));
        
        // Header
        const headerRow = "│ " + headers.map((h, i) => h.padEnd(colWidths[i])).join(" │ ") + " │";
        const topBorder = "┌─" + colWidths.map(w => "─".repeat(w)).join("─┬─") + "─┐";
        const separator = "├─" + colWidths.map(w => "─".repeat(w)).join("─┼─") + "─┤";
        const bottomBorder = "└─" + colWidths.map(w => "─".repeat(w)).join("─┴─") + "─┘";
        
        addLine(topBorder, 'output');
        addLine(headerRow, 'output');
        addLine(separator, 'output');
        
        // Data
        table.data.forEach(row => {
          const rowData = headers.map((header, i) => 
            String(row[header] || '').padEnd(colWidths[i])
          );
          addLine("│ " + rowData.join(" │ ") + " │", 'output');
        });
        
        addLine(bottomBorder, 'output');
        addLine("", 'output');
        addLine(`✅ Query completed successfully`, 'performance');
        addLine(`📊 ${table.data.length} rows returned • ⚡ ${executionTime.toFixed(2)}ms execution time`, 'performance');
      } else if (table) {
        addLine(`Table '${tableName}' is empty`, 'output');
      } else {
        addLine(`Error: Table '${tableName}' not found`, 'error');
      }
    } else if (trimmedCommand === 'clear') {
      setLines([]);
      welcomeMessage();
    } else if (trimmedCommand === 'exit') {
      addLine("Goodbye! Returning to home page...", 'system');
      setTimeout(() => {
        window.location.href = '/';
      }, 1000);
    } else if (trimmedCommand === '') {
      // Empty command, do nothing
    } else {
      addLine(`Error: Unknown command '${command}'`, 'error');
      addLine("Type 'help' for available commands", 'system');
    }

    setIsProcessing(false);
  };

  // Update suggestions when input changes
  useEffect(() => {
    if (input.trim()) {
      const newSuggestions = getSQLSuggestions(input);
      setSuggestions(newSuggestions);
      setShowAutoComplete(newSuggestions.length > 0);
    } else {
      setShowAutoComplete(false);
    }
  }, [input]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const commandToExecute = isMultiLine 
      ? multiLineInput.join(' ').trim()
      : input.trim();
      
    if (commandToExecute && !isProcessing) {
      setHistory(prev => [...prev, commandToExecute]);
      setHistoryIndex(-1);
      await executeCommand(commandToExecute);
      
      // Reset input
      setInput("");
      setMultiLineInput([""]);
      setCurrentLine(0);
      setIsMultiLine(false);
      setShowAutoComplete(false);
    }
  };

  const handleAutoCompleteSelect = (suggestion: string) => {
    const words = input.split(' ');
    words[words.length - 1] = suggestion;
    setInput(words.join(' ') + ' ');
    setShowAutoComplete(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Handle auto-complete navigation
    if (showAutoComplete && suggestions.length > 0) {
      if (e.key === 'Tab') {
        e.preventDefault();
        handleAutoCompleteSelect(suggestions[0]);
        return;
      }
      if (e.key === 'Escape') {
        setShowAutoComplete(false);
        return;
      }
    }

    // Multi-line support
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      setIsMultiLine(true);
      setMultiLineInput(prev => {
        const newInput = [...prev];
        newInput[currentLine] = input;
        newInput.push("");
        return newInput;
      });
      setCurrentLine(prev => prev + 1);
      setInput("");
      return;
    }

    // Command history navigation
    if (e.key === 'ArrowUp' && !showAutoComplete) {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex === -1 ? history.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setInput(history[newIndex]);
      }
    } else if (e.key === 'ArrowDown' && !showAutoComplete) {
      e.preventDefault();
      if (historyIndex !== -1) {
        const newIndex = historyIndex + 1;
        if (newIndex >= history.length) {
          setHistoryIndex(-1);
          setInput("");
        } else {
          setHistoryIndex(newIndex);
          setInput(history[newIndex]);
        }
      }
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      {/* Background Grid */}
      <div className="absolute inset-0 opacity-[0.02] pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(90deg,hsl(var(--primary))_1px,transparent_1px),linear-gradient(hsl(var(--primary))_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/10 bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="h-6 w-6 text-primary" />
            <span className="text-lg font-semibold">SQLite Engine Demo</span>
          </div>
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setShowThemeSettings(!showThemeSettings)}
            >
              <Settings className="w-4 h-4 mr-2" />
              Theme
            </Button>
            <Link to="/">
              <Button variant="ghost" size="sm" className="gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back to Home
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Theme Settings */}
      {showThemeSettings && (
        <div className="relative z-20 mx-6 mb-6">
          <ThemeSwitcher 
            currentTheme={currentTheme} 
            onThemeChange={(theme) => {
              setCurrentTheme(theme);
              setShowThemeSettings(false);
            }} 
          />
        </div>
      )}

      {/* Terminal */}
      <div className="relative z-10 h-[calc(100vh-80px)] p-6">
        <div className="h-full max-w-6xl mx-auto">
          <div 
            className="terminal-container terminal-crt h-full rounded-lg border border-white/20 backdrop-blur-sm shadow-2xl overflow-hidden"
            style={{ backgroundColor: currentTheme.background }}
          >
            {/* Terminal Header */}
            <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-white/5">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-warning-amber" />
                <div className="w-3 h-3 rounded-full bg-success-green" />
              </div>
              <span className="ml-4 text-sm text-muted-foreground">SQLite Terminal</span>
            </div>

            {/* Terminal Content */}
            <div className="h-[calc(100%-60px)] flex flex-col">
            <div 
                ref={terminalRef}
                className="flex-1 p-4 overflow-y-auto terminal-phosphor text-sm leading-relaxed space-y-1 relative z-10"
                style={{ color: currentTheme.foreground }}
              >
                {lines.map((line, index) => (
                  <div 
                    key={index} 
                    className={`terminal-glow ${
                      line.type === 'command' ? 'text-success-green' :
                      line.type === 'error' ? 'text-red-400' :
                      line.type === 'system' ? 'text-electric-cyan' :
                      line.type === 'performance' ? 'text-warning-amber' :
                      'text-foreground'
                    } ${line.isTyping ? 'animate-pulse' : ''}`}
                  >
                    {line.type === 'command' ? (
                      <div dangerouslySetInnerHTML={{ 
                        __html: line.content.replace(
                          /sqlite-engine@demo:~\$ (.+)/, 
                          'sqlite-engine@demo:~$ ' + highlightSQLCommand('$1')
                        )
                      }} />
                    ) : (
                      line.content
                    )}
                  </div>
                ))}
                {isProcessing && (
                  <div className="text-warning-amber">
                    Processing<span className="animate-pulse">...</span>
                  </div>
                )}
              </div>

              {/* Input Line */}
              <form onSubmit={handleSubmit} className="p-4 border-t border-white/10 relative z-10">
                {isMultiLine && (
                  <div className="mb-2 text-xs text-muted-foreground flex items-center gap-2">
                    <Zap className="h-3 w-3" />
                    Multi-line mode • Press Enter to execute • Escape to cancel
                  </div>
                )}
                
                <div className="flex items-center gap-2 terminal-phosphor text-sm relative">
                  <span 
                    className="terminal-glow"
                    style={{ color: currentTheme.prompt }}
                  >
                    sqlite-engine@demo:~{isMultiLine ? ' ...' : '$'}
                  </span>
                  <div className="flex-1 relative">
                    <input
                      ref={inputRef}
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={handleKeyDown}
                      className="w-full bg-transparent border-none outline-none terminal-glow"
                      style={{ color: currentTheme.foreground, caretColor: currentTheme.cursor }}
                      placeholder={isMultiLine ? "Continue SQL command..." : "Enter SQL command... (Tab for suggestions)"}
                      disabled={isProcessing}
                      autoFocus
                    />
                    <TerminalAutoComplete
                      input={input}
                      suggestions={suggestions}
                      onSelect={handleAutoCompleteSelect}
                      visible={showAutoComplete}
                    />
                  </div>
                  <span 
                    className="w-2 h-4 terminal-glow" 
                    style={{ 
                      backgroundColor: currentTheme.cursor,
                      animation: 'cursor-blink 1s infinite' 
                    }} 
                  />
                </div>
                
                {isMultiLine && (
                  <div className="mt-2 text-xs text-muted-foreground">
                    Current query: {multiLineInput.slice(0, currentLine).join(' ')} {input}
                  </div>
                )}
              </form>
        </div>
      </div>

      {/* Tutorial */}
      <TutorialMode 
        isActive={isTutorialActive} 
        onClose={() => setIsTutorialActive(false)} 
      />
      <TutorialButton onStart={() => setIsTutorialActive(true)} />
    </div>
      </div>
    </div>
  );
};

export default Demo;