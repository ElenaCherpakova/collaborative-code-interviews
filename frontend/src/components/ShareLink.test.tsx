import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ShareLink } from '@/components/ShareLink';

// Mock navigator.clipboard
const mockWriteText = vi.fn();
Object.assign(navigator, {
  clipboard: {
    writeText: mockWriteText,
  },
});

// Mock sonner toast
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe('ShareLink', () => {
  const mockLink = 'http://localhost:3000/interview/test-123';

  beforeEach(() => {
    mockWriteText.mockClear();
    mockWriteText.mockResolvedValue(undefined);
  });

  it('should render the share link', () => {
    render(<ShareLink link={mockLink} />);
    
    expect(screen.getByText(mockLink)).toBeInTheDocument();
  });

  it('should render the share heading', () => {
    render(<ShareLink link={mockLink} />);
    
    expect(screen.getByText('Share Interview')).toBeInTheDocument();
  });

  it('should render copy button', () => {
    render(<ShareLink link={mockLink} />);
    
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('should copy link to clipboard when button is clicked', async () => {
    render(<ShareLink link={mockLink} />);
    
    const copyButton = screen.getByRole('button');
    fireEvent.click(copyButton);
    
    expect(mockWriteText).toHaveBeenCalledWith(mockLink);
  });

  it('should render helper text', () => {
    render(<ShareLink link={mockLink} />);
    
    expect(
      screen.getByText(/Share this link with your candidate/i)
    ).toBeInTheDocument();
  });
});
