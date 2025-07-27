import { 
  Database, 
  Zap, 
  Shield, 
  Code2, 
  Blocks, 
  MemoryStick,
  CheckCircle,
  Gauge,
  Lock,
  FileCode,
  Puzzle,
  HardDrive
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: CheckCircle,
    title: "Full SQL Support",
    description: "Complete SELECT, INSERT, UPDATE, DELETE operations with complex joins and subqueries for comprehensive data manipulation.",
    color: "success-green"
  },
  {
    icon: Gauge,
    title: "High Performance", 
    description: "Optimized B+ tree indexing and intelligent query execution engine ensuring lightning-fast data access and retrieval.",
    color: "primary"
  },
  {
    icon: Lock,
    title: "ACID Compliance",
    description: "Full transaction support with atomicity, consistency, isolation, and durability guarantees for data integrity.",
    color: "warning-amber"
  },
  {
    icon: FileCode,
    title: "Python Native",
    description: "Clean, educational code structure written in pure Python for easy understanding and academic learning.",
    color: "tech-blue"
  },
  {
    icon: Puzzle,
    title: "Extensible Design",
    description: "Modular architecture with plugin support allowing easy extension and customization for different use cases.",
    color: "electric-cyan"
  },
  {
    icon: HardDrive,
    title: "Memory Efficient",
    description: "Smart buffer management and page-based storage system optimizing memory usage and disk I/O operations.",
    color: "primary"
  }
];

const FeaturesSection = () => {
  return (
    <section className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-6">
            Powerful Features
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Built with modern database principles and optimized for both performance and educational value
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <Card 
                key={feature.title}
                className="feature-card group animate-fade-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <CardContent className="p-6 text-center space-y-4">
                  <div className="relative inline-block">
                    <div className={`w-16 h-16 rounded-full bg-gradient-to-br from-${feature.color}/20 to-${feature.color}/10 flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300`}>
                      <IconComponent className={`w-8 h-8 text-${feature.color}`} />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-foreground">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;