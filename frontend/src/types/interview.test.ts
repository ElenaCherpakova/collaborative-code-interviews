import { describe, it, expect } from 'vitest';
import type {
  Interview,
  Participant,
  CodeExecution,
  ProgrammingLanguage,
} from '@/types/interview';

describe('Interview Types', () => {
  it('should allow creating a valid Interview object', () => {
    const interview: Interview = {
      id: 'test-id',
      title: 'Test Interview',
      code: 'console.log("Hello");',
      language: 'javascript',
      participants: [],
      executions: [],
      createdAt: new Date(),
      shareableLink: 'http://test.com/interview/test-id',
    };

    expect(interview.id).toBe('test-id');
    expect(interview.language).toBe('javascript');
  });

  it('should allow creating a valid Participant object', () => {
    const participant: Participant = {
      id: 'participant-1',
      name: 'John Doe',
      role: 'interviewer',
      isOnline: true,
      color: '#22d3ee',
      cursorPosition: { line: 1, column: 1 },
    };

    expect(participant.role).toBe('interviewer');
    expect(participant.cursorPosition?.line).toBe(1);
  });

  it('should allow creating a valid CodeExecution object', () => {
    const execution: CodeExecution = {
      id: 'exec-1',
      code: 'console.log("test");',
      language: 'javascript',
      output: 'test',
      executedAt: new Date(),
      executedBy: 'user-1',
    };

    expect(execution.output).toBe('test');
    expect(execution.error).toBeUndefined();
  });

  it('should validate all programming language types', () => {
    const languages: ProgrammingLanguage[] = [
      'javascript',
      'typescript',
      'python',
      'java',
      'cpp',
      'go',
      'rust',
    ];

    expect(languages).toHaveLength(7);
    languages.forEach((lang) => {
      expect(typeof lang).toBe('string');
    });
  });

  it('should allow participant with optional cursor position', () => {
    const participant: Participant = {
      id: 'p1',
      name: 'Test',
      role: 'candidate',
      isOnline: false,
      color: '#000',
    };

    expect(participant.cursorPosition).toBeUndefined();
  });

  it('should allow code execution with error', () => {
    const execution: CodeExecution = {
      id: 'exec-2',
      code: 'throw new Error("test");',
      language: 'javascript',
      output: '',
      error: 'Error: test',
      executedAt: new Date(),
      executedBy: 'user-1',
    };

    expect(execution.error).toBe('Error: test');
    expect(execution.output).toBe('');
  });
});
