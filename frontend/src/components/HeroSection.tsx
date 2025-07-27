import { Database, Zap, Github, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import heroImage from "@/assets/database-hero.jpg";
import ParticleSystem from "@/components/ParticleSystem";

const HeroSection = () => {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 py-20 relative overflow-hidden">
      <ParticleSystem />
      
      <div className="max-w-4xl mx-auto text-center space-y-8 relative z-10">
        {/* Animated Hero Image */}
        <div className="relative animate-fade-in">
          <div className="relative inline-block">
            <img 
              src={heroImage} 
              alt="Database Engine" 
              className="w-32 h-24 object-cover rounded-2xl mx-auto mb-4 glow-blue"
            />
            <div className="absolute -top-2 -right-2">
              <Zap className="w-8 h-8 text-electric-cyan animate-pulse" />
            </div>
          </div>
        </div>

        {/* Main Title */}
        <div className="space-y-4 animate-fade-in-delayed">
          <h1 className="text-5xl md:text-7xl font-bold gradient-text leading-tight">
            SQLite-Like
            <br />
            Database Engine
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto">
            A high-performance, Python-based database engine built from scratch for educational excellence
          </p>
        </div>

        {/* Tagline */}
        <div className="flex justify-center space-x-6 text-sm md:text-base animate-fade-in-delayed">
          <span className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-success-green"></div>
            <span>Fast</span>
          </span>
          <span className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-primary"></div>
            <span>Reliable</span>
          </span>
          <span className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-electric-cyan"></div>
            <span>Educational</span>
          </span>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-delayed">
          <Button 
            variant="hero" 
            size="lg" 
            className="group"
            onClick={() => window.open('https://github.com/Krrish777/Sqlite_Python', '_blank')}
          >
            <Github className="w-5 h-5 mr-2" />
            View Source Code
            <ExternalLink className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Link to="/demo">
            <Button variant="tech" size="lg">
              <Database className="w-5 h-5 mr-2" />
              Try Demo
            </Button>
          </Link>
        </div>

        {/* Tech Stack Badges */}
        <div className="flex flex-wrap justify-center gap-3 animate-slide-up">
          {[
            "Python 3.11+",
            "B+ Trees", 
            "ACID Compliance",
            "SQL Parser"
          ].map((tech) => (
            <span key={tech} className="tech-badge">
              {tech}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HeroSection;