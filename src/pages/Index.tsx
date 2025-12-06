import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { CreateInterviewDialog } from '@/components/CreateInterviewDialog';
import { Code2, Users, Zap, Terminal, Share2, Eye } from 'lucide-react';

const Index = () => {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const features = [
    {
      icon: Code2,
      title: 'Real-time Collaboration',
      description: 'Edit code together with instant sync across all participants.',
    },
    {
      icon: Terminal,
      title: 'Safe Code Execution',
      description: 'Run code safely in the browser with instant output feedback.',
    },
    {
      icon: Share2,
      title: 'Shareable Links',
      description: 'Generate unique links to invite candidates instantly.',
    },
    {
      icon: Eye,
      title: 'Syntax Highlighting',
      description: 'Support for JavaScript, TypeScript, Python, Java, and more.',
    },
    {
      icon: Users,
      title: 'Multi-participant',
      description: 'Multiple interviewers can join and observe the session.',
    },
    {
      icon: Zap,
      title: 'Instant Setup',
      description: 'No installation required. Start interviewing in seconds.',
    },
  ];

  return (
    <div className="min-h-screen bg-background gradient-mesh">
      {/* Hero Section */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center glow-primary">
              <Code2 className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold text-foreground">CodeInterview</span>
          </div>
          <Button variant="outline" onClick={() => setIsCreateDialogOpen(true)}>
            Start Interview
          </Button>
        </nav>
      </header>

      <main>
        {/* Hero */}
        <section className="container mx-auto px-4 py-20 text-center">
          <div className="max-w-3xl mx-auto animate-slide-up">
            <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
              Conduct{' '}
              <span className="text-primary">Technical Interviews</span>
              <br />
              Without the Hassle
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
              A collaborative coding platform designed for seamless technical interviews.
              Real-time editing, code execution, and instant sharing.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button
                variant="hero"
                size="xl"
                onClick={() => setIsCreateDialogOpen(true)}
              >
                <Zap className="w-5 h-5" />
                Create Interview
              </Button>
              <Button variant="outline" size="xl">
                Learn More
              </Button>
            </div>
          </div>

          {/* Code Preview */}
          <div className="mt-16 max-w-4xl mx-auto animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <div className="bg-card border border-border rounded-xl overflow-hidden shadow-2xl">
              <div className="flex items-center gap-2 px-4 py-3 bg-secondary/50 border-b border-border">
                <div className="w-3 h-3 rounded-full bg-destructive/60" />
                <div className="w-3 h-3 rounded-full bg-syntax-function/60" />
                <div className="w-3 h-3 rounded-full bg-accent/60" />
                <span className="ml-2 text-sm text-muted-foreground font-mono">interview.js</span>
              </div>
              <div className="p-6 bg-code-bg font-mono text-left text-sm">
                <div className="flex gap-4">
                  <div className="text-muted-foreground select-none">
                    {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
                      <div key={n}>{n}</div>
                    ))}
                  </div>
                  <div>
                    <div><span className="text-syntax-keyword">function</span> <span className="text-syntax-function">findMedian</span>(<span className="text-foreground">arr</span>) {'{'}</div>
                    <div>  <span className="text-syntax-keyword">const</span> sorted = arr.<span className="text-syntax-function">sort</span>((a, b) =&gt; a - b);</div>
                    <div>  <span className="text-syntax-keyword">const</span> mid = Math.<span className="text-syntax-function">floor</span>(sorted.length / <span className="text-syntax-number">2</span>);</div>
                    <div>  </div>
                    <div>  <span className="text-syntax-keyword">return</span> sorted.length % <span className="text-syntax-number">2</span> !== <span className="text-syntax-number">0</span></div>
                    <div>    ? sorted[mid]</div>
                    <div>    : (sorted[mid - <span className="text-syntax-number">1</span>] + sorted[mid]) / <span className="text-syntax-number">2</span>;</div>
                    <div>{'}'}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section className="container mx-auto px-4 py-20">
          <h2 className="text-3xl font-bold text-center text-foreground mb-12">
            Everything You Need for Technical Interviews
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="bg-card border border-border rounded-xl p-6 hover:border-primary/50 transition-all duration-300 animate-fade-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto px-4 py-20 text-center">
          <div className="bg-card border border-border rounded-2xl p-12 max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Ready to Streamline Your Interviews?
            </h2>
            <p className="text-muted-foreground mb-8">
              Start conducting professional technical interviews in minutes.
            </p>
            <Button
              variant="hero"
              size="xl"
              onClick={() => setIsCreateDialogOpen(true)}
            >
              Get Started — It's Free
            </Button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground text-sm">
          <p>© 2024 CodeInterview. Built for developers, by developers.</p>
        </div>
      </footer>

      <CreateInterviewDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
      />
    </div>
  );
};

export default Index;
