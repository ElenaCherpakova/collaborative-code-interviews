/**
 * Centralized API service for all backend calls.
 * Currently mocked - will be replaced with real API calls later.
 */

import { v4 as uuidv4 } from 'uuid';
import type {
  Interview,
  CreateInterviewRequest,
  JoinInterviewRequest,
  UpdateCodeRequest,
  ExecuteCodeRequest,
  ExecuteCodeResponse,
  Participant,
  ProgrammingLanguage,
} from '@/types/interview';

// Mock data store (simulates backend database)
const mockInterviews: Map<string, Interview> = new Map();

// Simulated network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Clears all mock data (for testing purposes)
 */
export function clearMockData(): void {
  mockInterviews.clear();
}


// Default code templates for each language
const defaultCodeTemplates: Record<ProgrammingLanguage, string> = {
  javascript: `// Welcome to the coding interview!
// Write your solution below

function solution(input) {
  // Your code here
  return input;
}

// Test your solution
console.log(solution("Hello, World!"));
`,
  typescript: `// Welcome to the coding interview!
// Write your solution below

function solution(input: string): string {
  // Your code here
  return input;
}

// Test your solution
console.log(solution("Hello, World!"));
`,
  python: `# Welcome to the coding interview!
# Write your solution below

def solution(input):
    # Your code here
    return input

# Test your solution
print(solution("Hello, World!"))
`,
  java: `// Welcome to the coding interview!
// Write your solution below

public class Solution {
    public static String solution(String input) {
        // Your code here
        return input;
    }
    
    public static void main(String[] args) {
        System.out.println(solution("Hello, World!"));
    }
}
`,
  cpp: `// Welcome to the coding interview!
// Write your solution below

#include <iostream>
#include <string>

std::string solution(const std::string& input) {
    // Your code here
    return input;
}

int main() {
    std::cout << solution("Hello, World!") << std::endl;
    return 0;
}
`,
  go: `// Welcome to the coding interview!
// Write your solution below

package main

import "fmt"

func solution(input string) string {
    // Your code here
    return input
}

func main() {
    fmt.Println(solution("Hello, World!"))
}
`,
  rust: `// Welcome to the coding interview!
// Write your solution below

fn solution(input: &str) -> String {
    // Your code here
    input.to_string()
}

fn main() {
    println!("{}", solution("Hello, World!"));
}
`,
};

// Participant colors for cursor display
const participantColors = [
  '#22d3ee', // cyan
  '#4ade80', // green
  '#f472b6', // pink
  '#fb923c', // orange
  '#a78bfa', // purple
  '#fbbf24', // yellow
];

/**
 * Creates a new interview session
 */
export async function createInterview(
  request: CreateInterviewRequest
): Promise<Interview> {
  await delay(300); // Simulate network delay

  const interviewId = uuidv4();
  const participantId = uuidv4();

  const interview: Interview = {
    id: interviewId,
    title: request.title,
    code: defaultCodeTemplates[request.language],
    language: request.language,
    participants: [
      {
        id: participantId,
        name: request.creatorName,
        role: 'interviewer',
        isOnline: true,
        color: participantColors[0],
      },
    ],
    executions: [],
    createdAt: new Date(),
    shareableLink: `${window.location.origin}/interview/${interviewId}`,
  };

  mockInterviews.set(interviewId, interview);

  return interview;
}

/**
 * Gets an interview by ID
 */
export async function getInterview(interviewId: string): Promise<Interview | null> {
  await delay(200);

  return mockInterviews.get(interviewId) || null;
}

/**
 * Joins an existing interview session
 */
export async function joinInterview(
  request: JoinInterviewRequest
): Promise<{ interview: Interview; participant: Participant }> {
  await delay(300);

  const interview = mockInterviews.get(request.interviewId);

  if (!interview) {
    throw new Error('Interview not found');
  }

  const participantId = uuidv4();
  const colorIndex = interview.participants.length % participantColors.length;

  const participant: Participant = {
    id: participantId,
    name: request.participantName,
    role: request.role,
    isOnline: true,
    color: participantColors[colorIndex],
  };

  interview.participants.push(participant);

  return { interview, participant };
}

/**
 * Updates code in an interview (real-time sync)
 */
export async function updateCode(request: UpdateCodeRequest): Promise<void> {
  // No delay for real-time updates
  const interview = mockInterviews.get(request.interviewId);

  if (interview) {
    interview.code = request.code;
  }
}

/**
 * Executes code safely in the browser
 */
export async function executeCode(
  request: ExecuteCodeRequest
): Promise<ExecuteCodeResponse> {
  await delay(500); // Simulate execution time

  const startTime = performance.now();
  let output = '';
  let error: string | undefined;

  try {
    // Safe code execution using Function constructor for JavaScript
    if (request.language === 'javascript' || request.language === 'typescript') {
      // Capture console.log output
      const logs: string[] = [];
      const mockConsole = {
        log: (...args: unknown[]) => {
          logs.push(args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
          ).join(' '));
        },
        error: (...args: unknown[]) => {
          logs.push(`Error: ${args.join(' ')}`);
        },
        warn: (...args: unknown[]) => {
          logs.push(`Warning: ${args.join(' ')}`);
        },
      };

      try {
        // Create a sandboxed function
        const sandboxedCode = `
          (function(console) {
            ${request.code}
          })
        `;

        const fn = new Function('return ' + sandboxedCode)();
        fn(mockConsole);

        output = logs.join('\n') || 'Code executed successfully (no output)';
      } catch (execError) {
        // Catch errors thrown during code execution
        error = execError instanceof Error ? execError.message : 'Unknown error occurred';
        output = '';
      }
    } else {
      // For other languages, return a mock response
      output = `[Mock Execution - ${request.language}]\n\nCode would be executed on server.\nOutput would appear here.\n\nNote: Only JavaScript/TypeScript can be executed in browser.`;
    }
  } catch (outerError) {
    // Catch errors during function creation
    console.error('ExecuteCode Error:', outerError);
    error = outerError instanceof Error ? outerError.message : 'Unknown error occurred';
    output = '';
  }

  const executionTime = performance.now() - startTime;

  // Store execution in interview (always store, even on error)
  const interview = mockInterviews.get(request.interviewId);
  if (interview) {
    interview.executions.push({
      id: uuidv4(),
      code: request.code,
      language: request.language,
      output: error ? '' : output,
      executedAt: new Date(),
      executedBy: request.participantId,
    });
  }

  return {
    output,
    error,
    executionTime,
  };
}

/**
 * Updates participant cursor position
 */
export async function updateCursorPosition(
  interviewId: string,
  participantId: string,
  position: { line: number; column: number }
): Promise<void> {
  const interview = mockInterviews.get(interviewId);

  if (interview) {
    const participant = interview.participants.find(p => p.id === participantId);
    if (participant) {
      participant.cursorPosition = position;
    }
  }
}

/**
 * Leaves an interview session
 */
export async function leaveInterview(
  interviewId: string,
  participantId: string
): Promise<void> {
  await delay(100);

  const interview = mockInterviews.get(interviewId);

  if (interview) {
    const participant = interview.participants.find(p => p.id === participantId);
    if (participant) {
      participant.isOnline = false;
    }
  }
}

/**
 * Gets default code template for a language
 */
export function getDefaultCodeTemplate(language: ProgrammingLanguage): string {
  return defaultCodeTemplates[language];
}

/**
 * Subscribes to real-time updates (mocked with polling)
 */
export function subscribeToInterview(
  interviewId: string,
  callbacks: {
    onCodeChange?: (code: string) => void;
    onParticipantChange?: (participants: Participant[]) => void;
  }
): () => void {
  let lastCode = '';
  let lastParticipantCount = 0;

  const interval = setInterval(() => {
    const interview = mockInterviews.get(interviewId);

    if (interview) {
      if (interview.code !== lastCode && callbacks.onCodeChange) {
        lastCode = interview.code;
        callbacks.onCodeChange(interview.code);
      }

      if (interview.participants.length !== lastParticipantCount && callbacks.onParticipantChange) {
        lastParticipantCount = interview.participants.length;
        callbacks.onParticipantChange([...interview.participants]);
      }
    }
  }, 500);

  // Return unsubscribe function
  return () => clearInterval(interval);
}
