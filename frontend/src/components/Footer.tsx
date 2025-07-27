import { Github, BookOpen, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="py-20 px-4 border-t border-border/50">
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <div className="animate-fade-in">
          <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-4">
            Ready to Explore?
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Dive into the source code and discover how a modern database engine works under the hood
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              variant="hero" 
              size="lg" 
              className="group"
              onClick={() => window.open('https://github.com/Krrish777/Sqlite_Python', '_blank')}
            >
              <Github className="w-5 h-5 mr-2" />
              View on GitHub
              <ExternalLink className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="tech" size="lg" asChild>
              <Link to="/docs">
                <BookOpen className="w-5 h-5 mr-2" />
                Documentation
              </Link>
            </Button>
          </div>
        </div>

        <div className="pt-8 border-t border-border/30 space-y-4 animate-fade-in-delayed">
          <p className="text-muted-foreground">
            <span className="font-semibold text-foreground">College Project</span> • Database Systems Course
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
            <span>Python 3.11+</span>
            <span>•</span>
            <span>MIT License</span>
            <span>•</span>
            <span>Open Source</span>
          </div>
          <p className="text-xs text-muted-foreground">
            Built with educational excellence and modern software engineering principles
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;