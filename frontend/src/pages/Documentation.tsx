import { ArrowLeft, Copy, Check, Github, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import BackgroundAnimation from "@/components/BackgroundAnimation";
import ScrollProgress from "@/components/ScrollProgress";

const Documentation = () => {
  const navigate = useNavigate();
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const copyToClipboard = async (text: string, id: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const CodeBlock = ({ children, language = "", id }: { children: string; language?: string; id: string }) => (
    <div className="relative group">
      <pre className="bg-muted/30 border rounded-lg p-4 overflow-x-auto">
        <code className={`language-${language} text-sm`}>{children}</code>
      </pre>
      <Button
        size="sm"
        variant="ghost"
        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
        onClick={() => copyToClipboard(children, id)}
      >
        {copiedCode === id ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
      </Button>
    </div>
  );

  return (
    <div className="min-h-screen bg-background text-foreground relative">
      <ScrollProgress />
      <BackgroundAnimation />
      
      <div className="relative z-10 max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" onClick={() => navigate("/")} className="group">
            <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Home
          </Button>
          <div>
            <h1 className="text-4xl font-bold gradient-text">Documentation</h1>
            <p className="text-muted-foreground mt-2">Complete guide to the SQLite-like Database Engine</p>
          </div>
        </div>

        {/* Content */}
        <Card className="backdrop-blur-sm bg-background/80 border-border/50">
          <CardContent className="p-8 prose prose-invert max-w-none">
            
            <div className="text-center mb-12">
              <h1 className="text-5xl font-bold gradient-text mb-4">🔧 SQLite-Like Database Engine in Python</h1>
              <p className="text-xl text-muted-foreground mb-4">
                This is a <strong>complete, modular, compiler-based educational database engine</strong> built from scratch in Python, inspired by SQLite. 
                The project follows a layered architecture with distinct components for tokenization, parsing, code generation, virtual machine execution, and persistent storage.
              </p>
              <div className="bg-tech-accent/20 border border-tech-accent/30 rounded-lg p-4 mb-6">
                <p className="text-lg">
                  🎯 <strong>Goal</strong>: To understand and recreate the core internals of a relational database engine using compiler and systems programming principles.
                </p>
              </div>
              <div className="text-2xl text-primary">
                🚀 <strong>Project Status</strong>: <span className="text-green-400">COMPLETE ✅</span> - Full working database engine with persistent storage!
              </div>
            </div>

            <hr className="border-border/30 my-12" />

            <h2 className="text-3xl font-bold gradient-text mb-8">✅ Features Implemented</h2>

            <div className="grid md:grid-cols-2 gap-6 mb-12">
              <Card className="bg-muted/20 border-border/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-tech-blue mb-4">🧠 Compiler Frontend</h3>
                  <ul className="space-y-2 text-sm">
                    <li><strong>Tokenizer</strong>: Converts raw SQL into structured tokens</li>
                    <li><strong>Parser</strong>: Builds abstract syntax trees (ASTs)</li>
                    <li><strong>Code Generator</strong>: Transforms ASTs into opcodes</li>
                    <li><strong>Opcode Design</strong>: Custom instruction set</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-muted/20 border-border/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-tech-purple mb-4">⚙️ Execution Engine</h3>
                  <ul className="space-y-2 text-sm">
                    <li><strong>Virtual Machine</strong>: Complete execution engine ✅</li>
                    <li><strong>Database Session</strong>: Query processing ✅</li>
                    <li><strong>SQL Processor</strong>: High-level coordination ✅</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-muted/20 border-border/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-tech-green mb-4">💾 Storage Backend</h3>
                  <ul className="space-y-2 text-sm">
                    <li><strong>B-Tree</strong>: Row storage and indexing ✅</li>
                    <li><strong>Pager</strong>: Database file paging system ✅</li>
                    <li><strong>OS Interface</strong>: File system operations ✅</li>
                    <li><strong>Row Codec</strong>: Row encoding/decoding ✅</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-muted/20 border-border/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-primary mb-4">🛠️ Infrastructure</h3>
                  <ul className="space-y-2 text-sm">
                    <li><strong>Logging System</strong>: Structured logging ✅</li>
                    <li><strong>Error Handling</strong>: Comprehensive errors ✅</li>
                    <li><strong>Validation</strong>: Input validation ✅</li>
                    <li><strong>CLI Interface</strong>: Full command-line ✅</li>
                  </ul>
                </CardContent>
              </Card>
            </div>

            <h2 className="text-3xl font-bold gradient-text mb-8">🧱 Architecture Overview</h2>
            
            <Card className="bg-muted/10 border-border/30 mb-12">
              <CardContent className="p-8">
                <pre className="text-center text-sm font-mono leading-relaxed text-muted-foreground">
{`SQL Query
   ↓
🔤 Tokenizer (Lexical Analysis)
   ↓
🌳 Parser (Syntax Analysis)
   ↓
📋 AST (Abstract Syntax Tree)
   ↓
⚡ Code Generator (Bytecode Generation)
   ↓
🔧 Opcodes (Virtual Machine Instructions)
   ↓
🖥️  Virtual Machine (Execution Engine)
   ↓
💾 Storage Backend (B-Tree + Pager)
   ↓
📊 Result Rows`}
                </pre>
              </CardContent>
            </Card>

            <h3 className="text-2xl font-bold text-tech-blue mb-4">🎯 Key Design Principles</h3>
            <div className="grid md:grid-cols-2 gap-4 mb-12">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary rounded-full"></span>
                  <strong>Compiler-based</strong>: Traditional compiler phases
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-tech-blue rounded-full"></span>
                  <strong>Stack-based VM</strong>: Bytecode execution
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-tech-green rounded-full"></span>
                  <strong>B-Tree Storage</strong>: Efficient row storage
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-tech-purple rounded-full"></span>
                  <strong>Modular Design</strong>: Clean separation
                </div>
              </div>
            </div>

            <h2 className="text-3xl font-bold gradient-text mb-8">🚀 Running the Project</h2>

            <h3 className="text-xl font-bold mb-4">💻 Execute SQL Queries</h3>
            <CodeBlock language="bash" id="basic-commands">
{`# Run a single SQL query
python main.py "CREATE TABLE users (id INTEGER, name TEXT, age INTEGER);"
python main.py "INSERT INTO users VALUES (1, 'Alice', 25);"
python main.py "SELECT * FROM users WHERE age > 20;"`}
            </CodeBlock>

            <h3 className="text-xl font-bold mb-4 mt-8">🪟 Windows PowerShell</h3>
            <CodeBlock language="powershell" id="windows-commands">
{`python main.py "SELECT * FROM users WHERE age > 30;"`}
            </CodeBlock>

            <h3 className="text-xl font-bold mb-4 mt-8">🧪 Run Test Suite</h3>
            <CodeBlock language="bash" id="test-commands">
{`# Execute all test cases
python main.py testcase.txt`}
            </CodeBlock>

            <h2 className="text-3xl font-bold gradient-text mb-8">🔨 Complete SQL Support</h2>

            <div className="grid md:grid-cols-2 gap-6 mb-12">
              <Card className="bg-green-950/20 border-green-800/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-green-400 mb-4">✅ Fully Implemented</h3>
                  <ul className="space-y-2 text-sm">
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">CREATE TABLE</code> - Table creation</li>
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">INSERT INTO</code> - Row insertion</li>
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">SELECT FROM WHERE</code> - Queries</li>
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">UPDATE SET WHERE</code> - Row updates</li>
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">DELETE FROM WHERE</code> - Row deletion</li>
                    <li><code className="bg-muted/30 px-2 py-1 rounded text-xs">DROP TABLE</code> - Table removal</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-blue-950/20 border-blue-800/30">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-blue-400 mb-4">🎯 Advanced Features</h3>
                  <ul className="space-y-2 text-sm">
                    <li><strong>Persistent Storage</strong>: B-Tree disk storage</li>
                    <li><strong>Type System</strong>: INTEGER, TEXT, REAL</li>
                    <li><strong>WHERE Clauses</strong>: Complex filtering</li>
                    <li><strong>Schema Validation</strong>: Type checking</li>
                    <li><strong>Error Recovery</strong>: Comprehensive handling</li>
                  </ul>
                </CardContent>
              </Card>
            </div>

            <h2 className="text-3xl font-bold gradient-text mb-8">🔬 Example Usage</h2>
            <CodeBlock language="sql" id="example-usage">
{`-- Create a table
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);

-- Insert data
INSERT INTO employees VALUES (1, 'John Doe', 50000);
INSERT INTO employees VALUES (2, 'Jane Smith', 60000);

-- Query data
SELECT * FROM employees WHERE salary > 55000;

-- Update records
UPDATE employees SET salary = 65000 WHERE name = 'Jane Smith';

-- Delete records
DELETE FROM employees WHERE id = 1;

-- Drop table
DROP TABLE employees;`}
            </CodeBlock>

            <h2 className="text-3xl font-bold gradient-text mb-8">📈 Performance Features</h2>
            <div className="grid md:grid-cols-2 gap-4 mb-12">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                    <span className="text-xs">🌳</span>
                  </div>
                  <div>
                    <div className="font-semibold">B-Tree indexing</div>
                    <div className="text-sm text-muted-foreground">O(log n) row access</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-tech-blue/20 flex items-center justify-center">
                    <span className="text-xs">💾</span>
                  </div>
                  <div>
                    <div className="font-semibold">Page caching</div>
                    <div className="text-sm text-muted-foreground">LRU cache for reduced I/O</div>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-tech-green/20 flex items-center justify-center">
                    <span className="text-xs">⚡</span>
                  </div>
                  <div>
                    <div className="font-semibold">Bytecode optimization</div>
                    <div className="text-sm text-muted-foreground">Efficient VM instructions</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-tech-purple/20 flex items-center justify-center">
                    <span className="text-xs">📦</span>
                  </div>
                  <div>
                    <div className="font-semibold">Compact storage</div>
                    <div className="text-sm text-muted-foreground">Efficient serialization</div>
                  </div>
                </div>
              </div>
            </div>

            <h2 className="text-3xl font-bold gradient-text mb-8">👨‍💻 Author</h2>
            <Card className="bg-gradient-to-r from-primary/10 to-tech-blue/10 border-primary/30">
              <CardContent className="p-6">
                <div className="text-center">
                  <h3 className="text-xl font-bold mb-2">Built by Krish Sharma</h3>
                  <p className="text-muted-foreground mb-4">
                    A passionate developer exploring the depths of systems programming and database internals.
                  </p>
                  <Button 
                    variant="outline" 
                    className="group"
                    onClick={() => window.open('https://github.com/Krrish777/Sqlite_Python', '_blank')}
                  >
                    <Github className="w-4 h-4 mr-2" />
                    View on GitHub
                    <ExternalLink className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            <div className="text-center mt-12 p-8 bg-gradient-to-r from-green-950/30 to-blue-950/30 rounded-lg border border-green-800/30">
              <h2 className="text-3xl font-bold text-green-400 mb-4">🎉 Project Status: COMPLETE!</h2>
              <p className="text-muted-foreground">
                This SQLite-like database engine is fully functional and ready for educational use, 
                further development, and learning database internals! 🚀
              </p>
            </div>

          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Documentation;