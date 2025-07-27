import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Pause, RotateCcw, TreePine } from "lucide-react";

interface BTreeNode {
  id: string;
  keys: number[];
  children: string[];
  isLeaf: boolean;
  x: number;
  y: number;
  highlighted: boolean;
}

const AlgorithmAnimations = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [step, setStep] = useState(0);
  const [currentOperation, setCurrentOperation] = useState<string>("");
  
  const initialTree: Record<string, BTreeNode> = {
    "root": {
      id: "root",
      keys: [10, 20],
      children: ["node1", "node2", "node3"],
      isLeaf: false,
      x: 300,
      y: 50,
      highlighted: false
    },
    "node1": {
      id: "node1",
      keys: [5, 8],
      children: [],
      isLeaf: true,
      x: 150,
      y: 150,
      highlighted: false
    },
    "node2": {
      id: "node2",
      keys: [15, 17],
      children: [],
      isLeaf: true,
      x: 300,
      y: 150,
      highlighted: false
    },
    "node3": {
      id: "node3",
      keys: [25, 30],
      children: [],
      isLeaf: true,
      x: 450,
      y: 150,
      highlighted: false
    }
  };

  const [tree, setTree] = useState<Record<string, BTreeNode>>(initialTree);

  const insertSteps = [
    { operation: "Insert 12", nodeId: "root", description: "Starting at root, comparing 12 with keys [10, 20]" },
    { operation: "Navigate", nodeId: "node2", description: "12 > 10 and 12 < 20, go to middle child" },
    { operation: "Insert", nodeId: "node2", description: "Insert 12 into leaf node [15, 17]" },
    { operation: "Complete", nodeId: "node2", description: "Node now contains [12, 15, 17]" }
  ];

  useEffect(() => {
    if (!isPlaying) return;
    
    const timer = setInterval(() => {
      setStep(prev => {
        if (prev >= insertSteps.length - 1) {
          setIsPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, 2000);

    return () => clearInterval(timer);
  }, [isPlaying, insertSteps.length]);

  useEffect(() => {
    setTree(prevTree => {
      const newTree = { ...prevTree };
      
      // Reset all highlights
      Object.keys(newTree).forEach(nodeId => {
        newTree[nodeId] = { ...newTree[nodeId], highlighted: false };
      });

      // Highlight current step
      if (step < insertSteps.length) {
        const currentStep = insertSteps[step];
        if (newTree[currentStep.nodeId]) {
          newTree[currentStep.nodeId] = { 
            ...newTree[currentStep.nodeId], 
            highlighted: true 
          };
        }

        // Update node2 with inserted key in step 3
        if (step === 3) {
          newTree["node2"] = {
            ...newTree["node2"],
            keys: [12, 15, 17]
          };
        }
        
        setCurrentOperation(currentStep.description);
      }

      return newTree;
    });
  }, [step]);

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const reset = () => {
    setIsPlaying(false);
    setStep(0);
    setCurrentOperation("");
    setTree(initialTree);
  };

  return (
    <Card className="feature-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TreePine className="w-5 h-5 text-primary" />
          B+ Tree Algorithm Animation
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Watch how data insertion works in B+ tree structures
        </p>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] w-full bg-background border border-border rounded-lg relative overflow-hidden">
          {/* B+ Tree Visualization */}
          <svg width="100%" height="100%" className="absolute inset-0">
            {/* Connections */}
            {!tree.root.isLeaf && tree.root.children.map((childId, index) => {
              const child = tree[childId];
              if (!child) return null;
              return (
                <line
                  key={`${tree.root.id}-${childId}`}
                  x1={tree.root.x}
                  y1={tree.root.y + 30}
                  x2={child.x}
                  y2={child.y}
                  stroke="hsl(var(--border))"
                  strokeWidth="2"
                />
              );
            })}
            
            {/* Nodes */}
            {Object.values(tree).map(node => (
              <g key={node.id}>
                <rect
                  x={node.x - 40}
                  y={node.y}
                  width="80"
                  height="30"
                  fill={node.highlighted ? "hsl(var(--primary))" : "hsl(var(--card))"}
                  stroke="hsl(var(--border))"
                  strokeWidth="2"
                  rx="4"
                  className="transition-all duration-500"
                />
                <text
                  x={node.x}
                  y={node.y + 20}
                  textAnchor="middle"
                  fontSize="12"
                  fill={node.highlighted ? "hsl(var(--primary-foreground))" : "hsl(var(--foreground))"}
                  className="transition-all duration-500"
                >
                  {node.keys.join(", ")}
                </text>
              </g>
            ))}
          </svg>
        </div>
        
        <div className="mt-4 space-y-4">
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={togglePlay}
              disabled={step >= insertSteps.length - 1 && !isPlaying}
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isPlaying ? "Pause" : "Play"}
            </Button>
            <Button variant="outline" size="sm" onClick={reset}>
              <RotateCcw className="w-4 h-4 mr-2" />
              Reset
            </Button>
            <span className="text-sm text-muted-foreground">
              Step {step + 1} of {insertSteps.length}
            </span>
          </div>
          
          <div className="p-3 bg-muted rounded-lg">
            <p className="text-sm font-medium">Current Operation:</p>
            <p className="text-sm text-muted-foreground mt-1">
              {currentOperation || "Click Play to start the animation"}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AlgorithmAnimations;