/**
 * Centralized API service for all backend calls.
 * Connects to FastAPI backend based on OpenAPI specification.
 */

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

// Backend API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Helper function to handle API responses
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'An error occurred' }));
    throw new Error(error.message || `HTTP ${response.status}: ${response.statusText}`);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }
  
  return response.json();
}

/**
 * Creates a new interview session
 */
export async function createInterview(
  request: CreateInterviewRequest
): Promise<Interview> {
  const response = await fetch(`${API_BASE_URL}/interviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  return handleResponse<Interview>(response);
}

/**
 * Gets an interview by ID
 */
export async function getInterview(interviewId: string): Promise<Interview | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/interviews/${interviewId}`);
    return handleResponse<Interview>(response);
  } catch (error) {
    console.error('Failed to get interview:', error);
    return null;
  }
}

/**
 * Joins an existing interview session
 */
export async function joinInterview(
  request: JoinInterviewRequest
): Promise<{ interview: Interview; participant: Participant }> {
  const response = await fetch(`${API_BASE_URL}/interviews/${request.interviewId}/join`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      participantName: request.participantName,
      role: request.role,
    }),
  });

  return handleResponse<{ interview: Interview; participant: Participant }>(response);
}

/**
 * Updates code in an interview (real-time sync)
 */
export async function updateCode(request: UpdateCodeRequest): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/interviews/${request.interviewId}/code`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code: request.code,
      participantId: request.participantId,
    }),
  });

  await handleResponse<void>(response);
}

/**
 * Executes code on the backend
 */
export async function executeCode(
  request: ExecuteCodeRequest
): Promise<ExecuteCodeResponse> {
  const response = await fetch(`${API_BASE_URL}/interviews/${request.interviewId}/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code: request.code,
      language: request.language,
      participantId: request.participantId,
    }),
  });

  return handleResponse<ExecuteCodeResponse>(response);
}

/**
 * Updates participant cursor position
 */
export async function updateCursorPosition(
  interviewId: string,
  participantId: string,
  position: { line: number; column: number }
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/interviews/${interviewId}/participants/${participantId}/cursor`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(position),
    }
  );

  await handleResponse<void>(response);
}

/**
 * Leaves an interview session
 */
export async function leaveInterview(
  interviewId: string,
  participantId: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/interviews/${interviewId}/participants/${participantId}/leave`,
    {
      method: 'POST',
    }
  );

  await handleResponse<void>(response);
}

/**
 * Gets default code template for a language
 */
export function getDefaultCodeTemplate(language: ProgrammingLanguage): string {
  return defaultCodeTemplates[language];
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

/**
 * Subscribes to real-time updates via WebSocket
 * TODO: Implement WebSocket connection to backend
 */
export function subscribeToInterview(
  interviewId: string,
  participantId: string,
  callbacks: {
    onCodeChange?: (code: string, updatedBy: string) => void;
    onParticipantJoined?: (participant: Participant) => void;
    onParticipantLeft?: (participantId: string) => void;
    onCursorMoved?: (participantId: string, position: { line: number; column: number }) => void;
    onExecutionCompleted?: (execution: any) => void;
  }
): () => void {
  // For now, use polling as a fallback
  // This should be replaced with WebSocket connection
  const WS_URL = import.meta.env.VITE_WS_URL || `ws://localhost:8000/ws/interviews/${interviewId}?participantId=${participantId}`;
  
  // Placeholder - WebSocket implementation would go here
  console.log('WebSocket URL:', WS_URL);
  
  // Return unsubscribe function
  return () => {
    console.log('Unsubscribing from interview updates');
  };
}
