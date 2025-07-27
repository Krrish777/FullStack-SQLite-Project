import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, GitBranch, Database } from "lucide-react";

interface FlowStep {
  id: string;
  title: string;
  description: string;
  active: boolean;
  completed: boolean;
}

const QueryFlowVisualization = () => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentStep, setCurrentStep] = useState(-1);

  const initialSteps: FlowStep[] = [
    { id: "tokenizer", title: "🔤 Tokenizer", description: "Break SQL string into tokens (keywords, identifiers, operators)", active: false, completed: false },
    { id: "parser", title: "🌳 Parser", description: "Build Abstract Syntax Tree (AST) from token stream", active: false, completed: false },
    { id: "codegen", title: "⚡ Code Generator", description: "Convert AST into bytecode opcodes for Virtual Machine", active: false, completed: false },
    { id: "vm", title: "🖥️ Virtual Machine", description: "Execute bytecode instructions using stack-based VM", active: false, completed: false },
    { id: "btree", title: "🌲 B+ Tree Engine", description: "Navigate B+ tree for efficient row storage and retrieval", active: false, completed: false },
    { id: "pager", title: "💾 Page Manager", description: "Handle database file I/O with LRU page caching", active: false, completed: false },
    { id: "formatter", title: "📊 Result Formatter", description: "Format and return query results to user", active: false, completed: false }
  ];

  const [steps, setSteps] = useState<FlowStep[]>(initialSteps);

  useEffect(() => {
    if (!isAnimating) return;

    const timer = setInterval(() => {
      setCurrentStep(prev => {
        if (prev >= steps.length - 1) {
          setIsAnimating(false);
          return prev;
        }
        return prev + 1;
      });
    }, 1200);

    return () => clearInterval(timer);
  }, [isAnimating, steps.length]);

  useEffect(() => {
    setSteps(prevSteps => 
      prevSteps.map((step, index) => ({
        ...step,
        active: index === currentStep && isAnimating,
        completed: index < currentStep || (index === currentStep && !isAnimating)
      }))
    );
  }, [currentStep, isAnimating]);

  const startAnimation = () => {
    setIsAnimating(true);
    setCurrentStep(0);
    setSteps(initialSteps);
  };

  const resetAnimation = () => {
    setIsAnimating(false);
    setCurrentStep(-1);
    setSteps(initialSteps);
  };

  return (
    <Card className="feature-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-primary" />
          SQLite Engine Query Processing
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          See how SQL queries are processed through the SQLite-like engine pipeline
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Button onClick={startAnimation} disabled={isAnimating} size="sm">
              <Play className="w-4 h-4 mr-2" />
              Process Query: SELECT * FROM users
            </Button>
            <Button onClick={resetAnimation} variant="outline" size="sm">
              Reset
            </Button>
          </div>

          <div className="relative">
            {/* Flow Steps */}
            <div className="space-y-3">
              {steps.map((step, index) => (
                <div
                  key={step.id}
                  className={`relative flex items-center p-4 rounded-lg border-2 transition-all duration-500 ${
                    step.active 
                      ? 'border-primary bg-primary/10 scale-105' 
                      : step.completed 
                        ? 'border-success-green bg-success-green/10' 
                        : 'border-border bg-card'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-4 transition-all duration-500 ${
                    step.active 
                      ? 'bg-primary text-primary-foreground animate-pulse' 
                      : step.completed 
                        ? 'bg-success-green text-white' 
                        : 'bg-muted text-muted-foreground'
                  }`}>
                    {step.completed ? '✓' : index + 1}
                  </div>
                  
                  <div className="flex-1">
                    <h4 className="font-medium">{step.title}</h4>
                    <p className="text-sm text-muted-foreground">{step.description}</p>
                  </div>

                  <div className={`w-4 h-4 transition-all duration-500 ${
                    step.active ? 'text-primary animate-spin' : 'text-muted-foreground'
                  }`}>
                    <Database className="w-4 h-4" />
                  </div>

                  {/* Arrow to next step */}
                  {index < steps.length - 1 && (
                    <div className="absolute -bottom-4 left-8 w-0.5 h-4 bg-border"></div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {currentStep >= steps.length - 1 && (
            <div className="mt-4 p-4 bg-success-green/10 border border-success-green/20 rounded-lg">
              <p className="text-sm text-success-green font-medium">
                SQLite query processing completed! 🚀
              </p>
              <p className="text-xs text-muted-foreground mt-1">Results returned from B+ Tree storage</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default QueryFlowVisualization;