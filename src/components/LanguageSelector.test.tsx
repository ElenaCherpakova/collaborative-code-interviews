import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LanguageSelector } from '@/components/LanguageSelector';

describe('LanguageSelector', () => {
  it('should render the selector with current value', () => {
    render(
      <LanguageSelector value="javascript" onChange={() => {}} />
    );
    
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });

  it('should be disabled when disabled prop is true', () => {
    render(
      <LanguageSelector value="javascript" onChange={() => {}} disabled={true} />
    );
    
    expect(screen.getByRole('combobox')).toBeDisabled();
  });

  it('should call onChange when a new language is selected', async () => {
    const handleChange = vi.fn();
    render(
      <LanguageSelector value="javascript" onChange={handleChange} />
    );
    
    // Open the dropdown
    fireEvent.click(screen.getByRole('combobox'));
    
    // Wait for the dropdown to open and click Python option
    const pythonOption = await screen.findByText('Python');
    fireEvent.click(pythonOption);
    
    expect(handleChange).toHaveBeenCalledWith('python');
  });
});
