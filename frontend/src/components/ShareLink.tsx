import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Copy, Check, Link } from 'lucide-react';
import { toast } from 'sonner';

interface ShareLinkProps {
  link: string;
}

export function ShareLink({ link }: ShareLinkProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      toast.success('Link copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    } catch {
      toast.error('Failed to copy link');
    }
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <h3 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wide flex items-center gap-2">
        <Link className="w-4 h-4" />
        Share Interview
      </h3>
      <div className="flex items-center gap-2">
        <div className="flex-1 bg-code-bg border border-border rounded-md px-3 py-2 font-mono text-sm text-foreground truncate">
          {link}
        </div>
        <Button
          variant="outline"
          size="icon"
          onClick={handleCopy}
          className="shrink-0"
        >
          {copied ? (
            <Check className="w-4 h-4 text-accent" />
          ) : (
            <Copy className="w-4 h-4" />
          )}
        </Button>
      </div>
      <p className="mt-2 text-xs text-muted-foreground">
        Share this link with your candidate to start the interview
      </p>
    </div>
  );
}
