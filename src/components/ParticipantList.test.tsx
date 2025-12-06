import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ParticipantList } from '@/components/ParticipantList';
import type { Participant } from '@/types/interview';

describe('ParticipantList', () => {
  const mockParticipants: Participant[] = [
    {
      id: '1',
      name: 'John Doe',
      role: 'interviewer',
      isOnline: true,
      color: '#22d3ee',
    },
    {
      id: '2',
      name: 'Jane Smith',
      role: 'candidate',
      isOnline: true,
      color: '#4ade80',
    },
    {
      id: '3',
      name: 'Bob Wilson',
      role: 'interviewer',
      isOnline: false,
      color: '#f472b6',
    },
  ];

  it('should render participant count correctly', () => {
    render(<ParticipantList participants={mockParticipants} />);
    
    expect(screen.getByText(/Participants \(3\)/i)).toBeInTheDocument();
  });

  it('should render all participant names', () => {
    render(<ParticipantList participants={mockParticipants} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('Bob Wilson')).toBeInTheDocument();
  });

  it('should display participant roles', () => {
    render(<ParticipantList participants={mockParticipants} />);
    
    expect(screen.getAllByText('interviewer')).toHaveLength(2);
    expect(screen.getByText('candidate')).toBeInTheDocument();
  });

  it('should show online/offline status', () => {
    render(<ParticipantList participants={mockParticipants} />);
    
    expect(screen.getAllByText('Online')).toHaveLength(2);
    expect(screen.getByText('Offline')).toBeInTheDocument();
  });

  it('should mark current user with (you)', () => {
    render(<ParticipantList participants={mockParticipants} currentUserId="1" />);
    
    expect(screen.getByText('(you)')).toBeInTheDocument();
  });

  it('should render avatar initials', () => {
    render(<ParticipantList participants={mockParticipants} />);
    
    expect(screen.getByText('J')).toBeInTheDocument(); // John
    expect(screen.getByText('B')).toBeInTheDocument(); // Bob
  });

  it('should handle empty participant list', () => {
    render(<ParticipantList participants={[]} />);
    
    expect(screen.getByText(/Participants \(0\)/i)).toBeInTheDocument();
  });
});
