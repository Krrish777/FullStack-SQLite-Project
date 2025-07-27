import DatabaseSchemaVisualizer from "@/components/DatabaseSchemaVisualizer";
import AlgorithmAnimations from "@/components/AlgorithmAnimations";
import QueryFlowVisualization from "@/components/QueryFlowVisualization";
import ThemeSwitcher, { themes, TerminalTheme } from "@/components/ThemeSwitcher";
import { useState } from "react";

const EducationalFeatures = () => {
  const [currentTheme, setCurrentTheme] = useState<TerminalTheme>(themes[0]);

  return (
    <section className="py-20 px-4 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-6">
            Educational Features
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Interactive visualizations and tools to understand database internals
          </p>
        </div>

        <div className="grid gap-8">
          {/* First Row */}
          <div className="grid lg:grid-cols-2 gap-8">
            <DatabaseSchemaVisualizer />
            <AlgorithmAnimations />
          </div>
          
          {/* Second Row */}
          <div className="grid lg:grid-cols-2 gap-8">
            <QueryFlowVisualization />
            <ThemeSwitcher 
              currentTheme={currentTheme} 
              onThemeChange={setCurrentTheme} 
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default EducationalFeatures;