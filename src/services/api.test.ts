import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  createInterview,
  getInterview,
  joinInterview,
  updateCode,
  executeCode,
  getDefaultCodeTemplate,
} from '@/services/api';

// Mock window.location for shareable link generation
Object.defineProperty(window, 'location', {
  value: {
    origin: 'http://localhost:3000',
  },
  writable: true,
});

describe('API Service', () => {
  describe('createInterview', () => {
    it('should create a new interview with correct properties', async () => {
      const request = {
        title: 'Test Interview',
        creatorName: 'John Doe',
        language: 'javascript' as const,
      };

      const interview = await createInterview(request);

      expect(interview).toHaveProperty('id');
      expect(interview.title).toBe('Test Interview');
      expect(interview.language).toBe('javascript');
      expect(interview.participants).toHaveLength(1);
      expect(interview.participants[0].name).toBe('John Doe');
      expect(interview.participants[0].role).toBe('interviewer');
      expect(interview.participants[0].isOnline).toBe(true);
      expect(interview.shareableLink).toContain(interview.id);
    });

    it('should use default code template for the selected language', async () => {
      const request = {
        title: 'Python Interview',
        creatorName: 'Jane Doe',
        language: 'python' as const,
      };

      const interview = await createInterview(request);

      expect(interview.code).toContain('def solution');
      expect(interview.code).toContain('# Welcome to the coding interview');
    });
  });

  describe('getInterview', () => {
    it('should return the interview if it exists', async () => {
      const created = await createInterview({
        title: 'Get Test',
        creatorName: 'Test User',
        language: 'typescript',
      });

      const retrieved = await getInterview(created.id);

      expect(retrieved).not.toBeNull();
      expect(retrieved?.id).toBe(created.id);
      expect(retrieved?.title).toBe('Get Test');
    });

    it('should return null for non-existent interview', async () => {
      const retrieved = await getInterview('non-existent-id');

      expect(retrieved).toBeNull();
    });
  });

  describe('joinInterview', () => {
    it('should add a new participant to the interview', async () => {
      const interview = await createInterview({
        title: 'Join Test',
        creatorName: 'Host',
        language: 'javascript',
      });

      const { interview: updatedInterview, participant } = await joinInterview({
        interviewId: interview.id,
        participantName: 'Candidate',
        role: 'candidate',
      });

      expect(updatedInterview.participants).toHaveLength(2);
      expect(participant.name).toBe('Candidate');
      expect(participant.role).toBe('candidate');
      expect(participant.isOnline).toBe(true);
    });

    it('should throw error for non-existent interview', async () => {
      await expect(
        joinInterview({
          interviewId: 'fake-id',
          participantName: 'Test',
          role: 'candidate',
        })
      ).rejects.toThrow('Interview not found');
    });
  });

  describe('updateCode', () => {
    it('should update the code in the interview', async () => {
      const interview = await createInterview({
        title: 'Update Test',
        creatorName: 'Test',
        language: 'javascript',
      });

      const newCode = 'console.log("Hello World");';
      await updateCode({
        interviewId: interview.id,
        code: newCode,
        participantId: interview.participants[0].id,
      });

      const updated = await getInterview(interview.id);
      expect(updated?.code).toBe(newCode);
    });
  });

  describe('executeCode', () => {
    it('should execute JavaScript code and return output', async () => {
      const interview = await createInterview({
        title: 'Execute Test',
        creatorName: 'Test',
        language: 'javascript',
      });

      const result = await executeCode({
        interviewId: interview.id,
        code: 'console.log("Hello, World!");',
        language: 'javascript',
        participantId: interview.participants[0].id,
      });

      expect(result.output).toBe('Hello, World!');
      expect(result.error).toBeUndefined();
      expect(result.executionTime).toBeGreaterThanOrEqual(0);
    });

    it('should handle code with multiple console.log calls', async () => {
      const interview = await createInterview({
        title: 'Multi Log Test',
        creatorName: 'Test',
        language: 'javascript',
      });

      const result = await executeCode({
        interviewId: interview.id,
        code: `
          console.log("First");
          console.log("Second");
          console.log("Third");
        `,
        language: 'javascript',
        participantId: interview.participants[0].id,
      });

      expect(result.output).toContain('First');
      expect(result.output).toContain('Second');
      expect(result.output).toContain('Third');
    });

    it('should handle code execution errors', async () => {
      const interview = await createInterview({
        title: 'Error Test',
        creatorName: 'Test',
        language: 'javascript',
      });

      const result = await executeCode({
        interviewId: interview.id,
        code: 'throw new Error("Test error");',
        language: 'javascript',
        participantId: interview.participants[0].id,
      });

      expect(result.error).toBeDefined();
      expect(result.error).toContain('Test error');
    });

    it('should return mock output for non-JavaScript languages', async () => {
      const interview = await createInterview({
        title: 'Python Test',
        creatorName: 'Test',
        language: 'python',
      });

      const result = await executeCode({
        interviewId: interview.id,
        code: 'print("Hello")',
        language: 'python',
        participantId: interview.participants[0].id,
      });

      expect(result.output).toContain('Mock Execution');
      expect(result.output).toContain('python');
    });

    it('should store execution history in the interview', async () => {
      const interview = await createInterview({
        title: 'History Test',
        creatorName: 'Test',
        language: 'javascript',
      });

      await executeCode({
        interviewId: interview.id,
        code: 'console.log("Test");',
        language: 'javascript',
        participantId: interview.participants[0].id,
      });

      const updated = await getInterview(interview.id);
      expect(updated?.executions).toHaveLength(1);
      expect(updated?.executions[0].code).toContain('console.log');
    });
  });

  describe('getDefaultCodeTemplate', () => {
    it('should return JavaScript template', () => {
      const template = getDefaultCodeTemplate('javascript');
      expect(template).toContain('function solution');
      expect(template).toContain('console.log');
    });

    it('should return Python template', () => {
      const template = getDefaultCodeTemplate('python');
      expect(template).toContain('def solution');
      expect(template).toContain('print');
    });

    it('should return TypeScript template', () => {
      const template = getDefaultCodeTemplate('typescript');
      expect(template).toContain('function solution');
      expect(template).toContain(': string');
    });

    it('should return Java template', () => {
      const template = getDefaultCodeTemplate('java');
      expect(template).toContain('public class Solution');
      expect(template).toContain('public static void main');
    });

    it('should return C++ template', () => {
      const template = getDefaultCodeTemplate('cpp');
      expect(template).toContain('#include');
      expect(template).toContain('std::cout');
    });

    it('should return Go template', () => {
      const template = getDefaultCodeTemplate('go');
      expect(template).toContain('package main');
      expect(template).toContain('func solution');
    });

    it('should return Rust template', () => {
      const template = getDefaultCodeTemplate('rust');
      expect(template).toContain('fn solution');
      expect(template).toContain('fn main()');
    });
  });
});
