import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { ProgrammingLanguage } from '@/types/interview';

interface LanguageSelectorProps {
  value: ProgrammingLanguage;
  onChange: (language: ProgrammingLanguage) => void;
  disabled?: boolean;
}

const languages: { value: ProgrammingLanguage; label: string; icon: string }[] = [
  { value: 'javascript', label: 'JavaScript', icon: 'JS' },
  { value: 'typescript', label: 'TypeScript', icon: 'TS' },
  { value: 'python', label: 'Python', icon: 'PY' },
  { value: 'java', label: 'Java', icon: 'JV' },
  { value: 'cpp', label: 'C++', icon: 'C+' },
  { value: 'go', label: 'Go', icon: 'GO' },
  { value: 'rust', label: 'Rust', icon: 'RS' },
];

export function LanguageSelector({ value, onChange, disabled }: LanguageSelectorProps) {
  return (
    <Select value={value} onValueChange={onChange} disabled={disabled}>
      <SelectTrigger className="w-[180px] bg-secondary border-border font-mono">
        <SelectValue placeholder="Select language" />
      </SelectTrigger>
      <SelectContent className="bg-card border-border">
        {languages.map((lang) => (
          <SelectItem
            key={lang.value}
            value={lang.value}
            className="font-mono cursor-pointer"
          >
            <span className="flex items-center gap-2">
              <span className="w-6 h-6 flex items-center justify-center bg-muted rounded text-xs font-bold text-primary">
                {lang.icon}
              </span>
              {lang.label}
            </span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
