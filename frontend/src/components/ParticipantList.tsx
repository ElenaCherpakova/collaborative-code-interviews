import type { Participant } from '@/types/interview';
import { cn } from '@/lib/utils';

interface ParticipantListProps {
  participants: Participant[];
  currentUserId?: string;
}

export function ParticipantList({ participants, currentUserId }: ParticipantListProps) {
  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <h3 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wide">
        Participants ({participants.length})
      </h3>
      <div className="space-y-2">
        {participants.map((participant) => (
          <div
            key={participant.id}
            className={cn(
              'flex items-center gap-3 p-2 rounded-md transition-colors',
              participant.id === currentUserId && 'bg-secondary/50'
            )}
          >
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
              style={{ backgroundColor: participant.color + '20', color: participant.color }}
            >
              {participant.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">
                {participant.name}
                {participant.id === currentUserId && (
                  <span className="text-muted-foreground ml-1">(you)</span>
                )}
              </p>
              <p className="text-xs text-muted-foreground capitalize">
                {participant.role}
              </p>
            </div>
            <div className="flex items-center gap-1">
              <span
                className={cn(
                  'w-2 h-2 rounded-full',
                  participant.isOnline ? 'bg-accent animate-pulse-subtle' : 'bg-muted-foreground'
                )}
              />
              <span className="text-xs text-muted-foreground">
                {participant.isOnline ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
