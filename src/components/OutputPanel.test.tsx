import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { OutputPanel } from '@/components/OutputPanel';

describe('OutputPanel', () => {
  it('should show placeholder when no output', () => {
    render(<OutputPanel output="" isExecuting={false} />);
    
    expect(screen.getByText(/Click "Run Code" to execute/i)).toBeInTheDocument();
  });

  it('should show executing state', () => {
    render(<OutputPanel output="" isExecuting={true} />);
    
    expect(screen.getByText(/Running.../i)).toBeInTheDocument();
    expect(screen.getByText(/Executing code.../i)).toBeInTheDocument();
  });

  it('should display output when available', () => {
    render(<OutputPanel output="Hello, World!" isExecuting={false} />);
    
    expect(screen.getByText('Hello, World!')).toBeInTheDocument();
  });

  it('should display error when available', () => {
    render(
      <OutputPanel output="" error="SyntaxError: Unexpected token" isExecuting={false} />
    );
    
    expect(screen.getByText('SyntaxError: Unexpected token')).toBeInTheDocument();
  });

  it('should display execution time when available', () => {
    render(
      <OutputPanel output="Done" isExecuting={false} executionTime={123.456} />
    );
    
    expect(screen.getByText('123ms')).toBeInTheDocument();
  });

  it('should show error icon when error is present', () => {
    render(<OutputPanel output="" error="Error" isExecuting={false} />);
    
    // Check that error styling is applied (red text)
    const errorText = screen.getByText('Error');
    expect(errorText).toHaveClass('text-destructive');
  });

  it('should prioritize error over output', () => {
    render(
      <OutputPanel output="Some output" error="Error message" isExecuting={false} />
    );
    
    expect(screen.getByText('Error message')).toBeInTheDocument();
    expect(screen.queryByText('Some output')).not.toBeInTheDocument();
  });
});
