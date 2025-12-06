import Editor from '@monaco-editor/react';
import type { ProgrammingLanguage } from '@/types/interview';

interface CodeEditorProps {
  code: string;
  language: ProgrammingLanguage;
  onChange: (value: string) => void;
  onCursorChange?: (position: { line: number; column: number }) => void;
  readOnly?: boolean;
}

// Map our language types to Monaco language identifiers
const languageMap: Record<ProgrammingLanguage, string> = {
  javascript: 'javascript',
  typescript: 'typescript',
  python: 'python',
  java: 'java',
  cpp: 'cpp',
  go: 'go',
  rust: 'rust',
};

export function CodeEditor({
  code,
  language,
  onChange,
  onCursorChange,
  readOnly = false,
}: CodeEditorProps) {
  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      onChange(value);
    }
  };

  return (
    <div className="h-full w-full rounded-lg overflow-hidden border border-border">
      <Editor
        height="100%"
        language={languageMap[language]}
        value={code}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "'JetBrains Mono', monospace",
          lineNumbers: 'on',
          glyphMargin: true,
          folding: true,
          lineDecorationsWidth: 10,
          lineNumbersMinChars: 3,
          renderLineHighlight: 'line',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          wordWrap: 'on',
          padding: { top: 16, bottom: 16 },
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: 'on',
          smoothScrolling: true,
        }}
        onMount={(editor) => {
          // Track cursor position changes
          editor.onDidChangeCursorPosition((e) => {
            if (onCursorChange) {
              onCursorChange({
                line: e.position.lineNumber,
                column: e.position.column,
              });
            }
          });
        }}
      />
    </div>
  );
}
