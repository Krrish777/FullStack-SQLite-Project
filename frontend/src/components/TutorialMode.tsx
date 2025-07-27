import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { X, ArrowRight, ArrowLeft, HelpCircle, Lightbulb } from "lucide-react";

interface TutorialStep {
  id: string;
  title: string;
  content: string;
  target?: string;
  position: 'top' | 'bottom' | 'left' | 'right' | 'center';
}

const tutorialSteps: TutorialStep[] = [
  {
    id: '1',
    title: 'Welcome to SQLite Database Engine',
    content: 'This interactive demo will guide you through the features of our educational database engine. Let\'s explore together!',
    position: 'center'
  },
  {
    id: '2',
    title: 'Interactive Terminal',
    content: 'Try typing SQL commands in the terminal below. Use syntax like SELECT, INSERT, CREATE TABLE to interact with the database.',
    target: '.terminal-container',
    position: 'top'
  },
  {
    id: '3',
    title: 'Syntax Highlighting',
    content: 'Notice how SQL keywords are highlighted in different colors as you type. This helps identify query structure.',
    target: '.terminal-input',
    position: 'top'
  },
  {
    id: '4',
    title: 'Auto-completion',
    content: 'Press Tab or Ctrl+Space to see auto-completion suggestions for SQL keywords and table names.',
    target: '.terminal-input',
    position: 'bottom'
  },
  {
    id: '5',
    title: 'Performance Metrics',
    content: 'After executing queries, you\'ll see execution time and performance metrics displayed here.',
    target: '.performance-display',
    position: 'top'
  },
  {
    id: '6',
    title: 'Multi-line Queries',
    content: 'Use Ctrl+Enter to execute complex multi-line SQL queries. Single Enter adds a new line.',
    target: '.terminal-input',
    position: 'bottom'
  }
];

interface TutorialModeProps {
  isActive: boolean;
  onClose: () => void;
}

const TutorialMode = ({ isActive, onClose }: TutorialModeProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isActive) {
      setIsVisible(true);
      setCurrentStep(0);
    } else {
      setIsVisible(false);
    }
  }, [isActive]);

  if (!isVisible) return null;

  const step = tutorialSteps[currentStep];
  const isLastStep = currentStep === tutorialSteps.length - 1;
  const isFirstStep = currentStep === 0;

  const nextStep = () => {
    if (isLastStep) {
      onClose();
    } else {
      setCurrentStep(prev => prev + 1);
    }
  };

  const prevStep = () => {
    if (!isFirstStep) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const getPositionClasses = () => {
    switch (step.position) {
      case 'center':
        return 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2';
      case 'top':
        return 'fixed top-4 left-1/2 transform -translate-x-1/2';
      case 'bottom':
        return 'fixed bottom-4 left-1/2 transform -translate-x-1/2';
      case 'left':
        return 'fixed left-4 top-1/2 transform -translate-y-1/2';
      case 'right':
        return 'fixed right-4 top-1/2 transform -translate-y-1/2';
      default:
        return 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2';
    }
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" />
      
      {/* Tutorial Card */}
      <Card className={`z-[60] w-80 max-w-sm animate-scale-in bg-background border shadow-xl ${getPositionClasses()}`}>
        <CardContent className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                <Lightbulb className="w-4 h-4 text-primary-foreground" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">{step.title}</h3>
                <p className="text-xs text-muted-foreground">
                  Step {currentStep + 1} of {tutorialSteps.length}
                </p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>
          
          <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
            {step.content}
          </p>
          
          {/* Progress Bar */}
          <div className="w-full bg-muted rounded-full h-1 mb-4">
            <div 
              className="bg-primary h-1 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
            />
          </div>
          
          <div className="flex justify-between items-center">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={prevStep}
              disabled={isFirstStep}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Previous
            </Button>
            
            <div className="flex items-center gap-1">
              {tutorialSteps.map((_, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full transition-all ${
                    index === currentStep ? 'bg-primary' : 'bg-muted'
                  }`}
                />
              ))}
            </div>
            
            <Button size="sm" onClick={nextStep}>
              {isLastStep ? 'Finish' : 'Next'}
              {!isLastStep && <ArrowRight className="w-4 h-4 ml-2" />}
            </Button>
          </div>
        </CardContent>
      </Card>
      
      {/* Highlight Target Element */}
      {step.target && (
        <style>
          {`
            ${step.target} {
              position: relative;
              z-index: 51;
              box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.5) !important;
              border-radius: 8px;
            }
          `}
        </style>
      )}
    </>
  );
};

interface TutorialButtonProps {
  onStart: () => void;
}

export const TutorialButton = ({ onStart }: TutorialButtonProps) => {
  return (
    <Button 
      variant="outline" 
      size="sm" 
      onClick={onStart}
      className="fixed bottom-4 right-4 z-40 shadow-lg"
    >
      <HelpCircle className="w-4 h-4 mr-2" />
      Tutorial
    </Button>
  );
};

export default TutorialMode;