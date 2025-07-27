import { useState, useEffect } from "react";
import { Copy, Play, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

const InteractiveCodeEditor = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState("");

  const codeLines = [
    "import sqlite_engine",
    "",
    "# Initialize database connection",
    'db = SQLiteEngine("example.db")',
    "",
    "# Create table with indexes",
    'db.execute("""',
    "    CREATE TABLE users (",
    "        id INTEGER PRIMARY KEY,",
    "        name TEXT NOT NULL,",
    "        email TEXT UNIQUE,",
    "        created_at TIMESTAMP",
    "    );",
    '""")',
    "",
    "# Insert data with transaction",
    "with db.transaction():",
    '    db.execute("""',
    "        INSERT INTO users (name, email, created_at)",
    "        VALUES (?, ?, ?)",
    '    """, ("John Doe", "john@example.com", datetime.now()))'
  ];

  const simulateExecution = async () => {
    setIsRunning(true);
    setOutput("");
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setOutput(`Database initialized successfully!
Table 'users' created with schema:
  - id: INTEGER PRIMARY KEY
  - name: TEXT NOT NULL  
  - email: TEXT UNIQUE
  - created_at: TIMESTAMP

Transaction completed: 1 row inserted
Execution time: 0.045ms`);
    
    setIsRunning(false);
  };

  const copyCode = () => {
    navigator.clipboard.writeText(codeLines.join('\n'));
  };

  return (
    <div className="code-editor">
      <div className="code-editor-header">
        <div className="flex items-center space-x-3">
          <h3 className="text-lg font-semibold text-foreground">Python Usage Example</h3>
          <div className="flex space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-success-green"></div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={copyCode}
            className="h-8 w-8 p-0"
          >
            <Copy className="w-4 h-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={simulateExecution}
            disabled={isRunning}
            className="h-8 w-8 p-0"
          >
            {isRunning ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Play className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
      
      <div className="code-editor-content">
        {codeLines.map((line, index) => (
          <div key={index} className="code-line">
            <span className="line-number">{index + 1}</span>
            <span className="code-content">
              {line}
            </span>
          </div>
        ))}
        
        {output && (
          <div className="mt-6 p-4 bg-success-green/10 border border-success-green/20 rounded">
            <div className="text-sm text-success-green font-mono whitespace-pre-line">
              {output}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractiveCodeEditor;