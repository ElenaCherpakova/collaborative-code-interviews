import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { LanguageSelector } from '@/components/LanguageSelector';
import { createInterview } from '@/services/api';
import type { ProgrammingLanguage } from '@/types/interview';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

interface CreateInterviewDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CreateInterviewDialog({ open, onOpenChange }: CreateInterviewDialogProps) {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [creatorName, setCreatorName] = useState('');
  const [language, setLanguage] = useState<ProgrammingLanguage>('javascript');
  const [isCreating, setIsCreating] = useState(false);

  const handleCreate = async () => {
    if (!title.trim() || !creatorName.trim()) {
      toast.error('Please fill in all fields');
      return;
    }

    setIsCreating(true);

    try {
      const interview = await createInterview({
        title: title.trim(),
        creatorName: creatorName.trim(),
        language,
      });

      toast.success('Interview created successfully!');
      onOpenChange(false);
      navigate(`/interview/${interview.id}`);
    } catch (error) {
      toast.error('Failed to create interview');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md bg-card border-border">
        <DialogHeader>
          <DialogTitle className="text-xl">Create New Interview</DialogTitle>
          <DialogDescription className="text-muted-foreground">
            Set up a coding interview session for your candidate.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="title">Interview Title</Label>
            <Input
              id="title"
              placeholder="e.g., Frontend Developer Interview"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="bg-secondary border-border"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Your Name</Label>
            <Input
              id="name"
              placeholder="e.g., John Doe"
              value={creatorName}
              onChange={(e) => setCreatorName(e.target.value)}
              className="bg-secondary border-border"
            />
          </div>
          <div className="space-y-2">
            <Label>Programming Language</Label>
            <LanguageSelector value={language} onChange={setLanguage} />
          </div>
        </div>
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            variant="hero"
            onClick={handleCreate}
            disabled={isCreating || !title.trim() || !creatorName.trim()}
          >
            {isCreating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Creating...
              </>
            ) : (
              'Create Interview'
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
