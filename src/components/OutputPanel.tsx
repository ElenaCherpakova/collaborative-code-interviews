import { Terminal, CheckCircle, XCircle, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface OutputPanelProps {
  output: string;
  error?: string;
  isExecuting: boolean;
  executionTime?: number;
}

export function OutputPanel({ output, error, isExecuting, executionTime }: OutputPanelProps) {
  const hasOutput = output || error;

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-2 bg-secondary/50 border-b border-border">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-muted-foreground" />
          <span className="text-sm font-medium">Output</span>
        </div>
        {isExecuting ? (
          <div className="flex items-center gap-1 text-primary">
            <div className="w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <span className="text-xs">Running...</span>
          </div>
        ) : hasOutput ? (
          <div className="flex items-center gap-2">
            {error ? (
              <XCircle className="w-4 h-4 text-destructive" />
            ) : (
              <CheckCircle className="w-4 h-4 text-accent" />
            )}
            {executionTime !== undefined && (
              <span className="text-xs text-muted-foreground flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {executionTime.toFixed(0)}ms
              </span>
            )}
          </div>
        ) : null}
      </div>
      <div className="flex-1 overflow-auto p-4 bg-code-bg font-mono text-sm">
        {isExecuting ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
            <span className="ml-2">Executing code...</span>
          </div>
        ) : error ? (
          <pre className={cn(
            'whitespace-pre-wrap break-words text-destructive',
            'animate-fade-in'
          )}>
            {error}
          </pre>
        ) : output ? (
          <pre className={cn(
            'whitespace-pre-wrap break-words text-foreground',
            'animate-fade-in'
          )}>
            {output}
          </pre>
        ) : (
          <p className="text-muted-foreground italic">
            Click "Run Code" to execute and see output here...
          </p>
        )}
      </div>
    </div>
  );
}
