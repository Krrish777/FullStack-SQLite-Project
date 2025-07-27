import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import InteractiveCodeEditor from "@/components/InteractiveCodeEditor";

const TechnicalSpecs = () => {
  const techCategories = [
    {
      title: "Storage Engine",
      items: ["B+ Tree Indexing", "Page-based Storage", "WAL", "Buffer Pool"]
    },
    {
      title: "SQL Engine", 
      items: ["Parser", "Query Optimizer", "Join Algorithms", "Aggregates"]
    },
    {
      title: "Transaction System",
      items: ["MVCC", "Deadlock Detection", "Lock Manager", "Recovery"]
    },
    {
      title: "Data Types",
      items: ["INTEGER", "TEXT", "REAL", "BLOB"]
    }
  ];

  const codeExample = `import sqlite_engine

# Initialize database connection
db = SQLiteEngine("example.db")

# Create table with indexes
db.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP
    );
""")

# Insert data with transaction
with db.transaction():
    db.execute("""
        INSERT INTO users (name, email, created_at)
        VALUES (?, ?, ?)
    """, ("John Doe", "john@example.com", datetime.now()))

# Complex query with joins
result = db.execute("""
    SELECT u.name, p.title, p.created_at
    FROM users u
    JOIN posts p ON u.id = p.user_id
    WHERE u.created_at > ?
    ORDER BY p.created_at DESC
    LIMIT 10
""", (last_week,))

for row in result:
    print(f"{row['name']}: {row['title']}")`;

  return (
    <section className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-6">
            Technical Specifications
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Advanced database algorithms and data structures implemented with academic rigor
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start">
          {/* Technical Categories */}
          <div className="space-y-8 animate-slide-up">
            {techCategories.map((category, index) => (
              <Card key={category.title} className="group hover:bg-secondary/50 transition-colors duration-300">
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-4 text-primary group-hover:text-accent transition-colors">
                    {category.title}
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {category.items.map((item) => (
                      <Badge 
                        key={item} 
                        variant="secondary" 
                        className="hover:bg-primary hover:text-primary-foreground transition-colors cursor-default"
                      >
                        {item}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Interactive Code Editor */}
          <div className="animate-fade-in-delayed">
            <InteractiveCodeEditor />
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechnicalSpecs;