export type ProgrammingLanguage = 
  | 'javascript'
  | 'typescript'
  | 'python'
  | 'java'
  | 'cpp'
  | 'go'
  | 'rust';

export interface Participant {
  id: string;
  name: string;
  role: 'interviewer' | 'candidate';
  isOnline: boolean;
  cursorPosition?: { line: number; column: number };
  color: string;
}

export interface CodeExecution {
  id: string;
  code: string;
  language: ProgrammingLanguage;
  output: string;
  error?: string;
  executedAt: Date;
  executedBy: string;
}

export interface Interview {
  id: string;
  title: string;
  code: string;
  language: ProgrammingLanguage;
  participants: Participant[];
  executions: CodeExecution[];
  createdAt: Date;
  shareableLink: string;
}

export interface CreateInterviewRequest {
  title: string;
  language: ProgrammingLanguage;
  creatorName: string;
}

export interface JoinInterviewRequest {
  interviewId: string;
  participantName: string;
  role: 'interviewer' | 'candidate';
}

export interface UpdateCodeRequest {
  interviewId: string;
  code: string;
  participantId: string;
}

export interface ExecuteCodeRequest {
  interviewId: string;
  code: string;
  language: ProgrammingLanguage;
  participantId: string;
}

export interface ExecuteCodeResponse {
  output: string;
  error?: string;
  executionTime: number;
}
