import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Monitor, Palette } from "lucide-react";

export interface TerminalTheme {
  id: string;
  name: string;
  background: string;
  foreground: string;
  accent: string;
  prompt: string;
  cursor: string;
  preview: string;
}

const themes: TerminalTheme[] = [
  {
    id: 'default',
    name: 'Cyber Tech',
    background: 'hsl(220 27% 8%)',
    foreground: 'hsl(210 40% 98%)',
    accent: 'hsl(200 100% 60%)',
    prompt: 'hsl(170 100% 50%)',
    cursor: 'hsl(200 100% 60%)',
    preview: 'user@db:~$ SELECT * FROM users;'
  },
  {
    id: 'matrix',
    name: 'Matrix Green',
    background: 'hsl(120 100% 5%)',
    foreground: 'hsl(120 100% 70%)',
    accent: 'hsl(120 100% 50%)',
    prompt: 'hsl(120 100% 80%)',
    cursor: 'hsl(120 100% 60%)',
    preview: 'neo@matrix:~$ SELECT * FROM reality;'
  },
  {
    id: 'ocean',
    name: 'Ocean Blue',
    background: 'hsl(220 50% 8%)',
    foreground: 'hsl(200 80% 85%)',
    accent: 'hsl(200 100% 70%)',
    prompt: 'hsl(180 100% 60%)',
    cursor: 'hsl(200 100% 70%)',
    preview: 'captain@ocean:~$ SELECT * FROM depths;'
  },
  {
    id: 'amber',
    name: 'Vintage Amber',
    background: 'hsl(30 20% 8%)',
    foreground: 'hsl(45 100% 70%)',
    accent: 'hsl(45 100% 60%)',
    prompt: 'hsl(45 100% 80%)',
    cursor: 'hsl(45 100% 70%)',
    preview: 'retro@terminal:~$ SELECT * FROM history;'
  },
  {
    id: 'purple',
    name: 'Neon Purple',
    background: 'hsl(280 50% 8%)',
    foreground: 'hsl(300 80% 85%)',
    accent: 'hsl(300 100% 70%)',
    prompt: 'hsl(320 100% 60%)',
    cursor: 'hsl(300 100% 70%)',
    preview: 'hacker@neon:~$ SELECT * FROM cyberspace;'
  },
  {
    id: 'forest',
    name: 'Forest Dark',
    background: 'hsl(140 30% 6%)',
    foreground: 'hsl(140 40% 80%)',
    accent: 'hsl(140 60% 60%)',
    prompt: 'hsl(140 80% 70%)',
    cursor: 'hsl(140 60% 60%)',
    preview: 'ranger@forest:~$ SELECT * FROM nature;'
  }
];

interface ThemeSwitcherProps {
  currentTheme: TerminalTheme;
  onThemeChange: (theme: TerminalTheme) => void;
}

const ThemeSwitcher = ({ currentTheme, onThemeChange }: ThemeSwitcherProps) => {
  return (
    <Card className="feature-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Palette className="w-5 h-5 text-primary" />
          Terminal Theme Switcher
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Choose from multiple terminal color schemes
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {themes.map((theme) => (
            <div
              key={theme.id}
              className={`relative cursor-pointer rounded-lg border-2 transition-all duration-300 hover:scale-105 ${
                currentTheme.id === theme.id 
                  ? 'border-primary shadow-lg shadow-primary/20' 
                  : 'border-border hover:border-primary/50'
              }`}
              onClick={() => onThemeChange(theme)}
            >
              {/* Theme Preview */}
              <div 
                className="h-20 rounded-t-lg p-3 font-mono text-xs"
                style={{ 
                  backgroundColor: theme.background,
                  color: theme.foreground
                }}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-2 h-2 rounded-full bg-red-500"></div>
                  <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                </div>
                <div style={{ color: theme.accent }}>
                  {theme.preview}
                </div>
                <div className="flex items-center">
                  <span style={{ color: theme.cursor }}>█</span>
                </div>
              </div>
              
              {/* Theme Info */}
              <div className="p-3 bg-card rounded-b-lg">
                <h4 className="font-medium text-sm">{theme.name}</h4>
                <div className="flex items-center gap-1 mt-2">
                  <div 
                    className="w-3 h-3 rounded-full border border-border"
                    style={{ backgroundColor: theme.background }}
                  ></div>
                  <div 
                    className="w-3 h-3 rounded-full border border-border"
                    style={{ backgroundColor: theme.accent }}
                  ></div>
                  <div 
                    className="w-3 h-3 rounded-full border border-border"
                    style={{ backgroundColor: theme.prompt }}
                  ></div>
                </div>
              </div>
              
              {/* Active Indicator */}
              {currentTheme.id === theme.id && (
                <div className="absolute top-2 right-2">
                  <div className="w-3 h-3 rounded-full bg-primary animate-pulse"></div>
                </div>
              )}
            </div>
          ))}
        </div>
        
        <div className="mt-4 p-3 bg-muted rounded-lg">
          <p className="text-sm">
            <Monitor className="inline w-4 h-4 mr-1" />
            Current theme: <span className="font-medium">{currentTheme.name}</span>
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ThemeSwitcher;
export { themes };