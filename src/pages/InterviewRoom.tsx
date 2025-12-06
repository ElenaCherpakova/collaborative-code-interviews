import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { CodeEditor } from '@/components/CodeEditor';
import { LanguageSelector } from '@/components/LanguageSelector';
import { ParticipantList } from '@/components/ParticipantList';
import { ShareLink } from '@/components/ShareLink';
import { OutputPanel } from '@/components/OutputPanel';
import {
  getInterview,
  updateCode,
  executeCode,
  subscribeToInterview,
  getDefaultCodeTemplate,
} from '@/services/api';
import type { Interview, ProgrammingLanguage } from '@/types/interview';
import { toast } from 'sonner';
import { Play, Code2, ArrowLeft, Settings } from 'lucide-react';

export default function InterviewRoom() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [interview, setInterview] = useState<Interview | null>(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState<ProgrammingLanguage>('javascript');
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | undefined>();
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionTime, setExecutionTime] = useState<number | undefined>();
  const [isLoading, setIsLoading] = useState(true);

  // Current user ID (would come from auth in production)
  const currentUserId = interview?.participants[0]?.id;

  useEffect(() => {
    if (!id) {
      navigate('/');
      return;
    }

    const loadInterview = async () => {
      try {
        const data = await getInterview(id);
        if (data) {
          setInterview(data);
          setCode(data.code);
          setLanguage(data.language);
        } else {
          toast.error('Interview not found');
          navigate('/');
        }
      } catch {
        toast.error('Failed to load interview');
        navigate('/');
      } finally {
        setIsLoading(false);
      }
    };

    loadInterview();
  }, [id, navigate]);

  // Subscribe to real-time updates
  useEffect(() => {
    if (!id) return;

    const unsubscribe = subscribeToInterview(id, {
      onParticipantChange: (participants) => {
        setInterview((prev) =>
          prev ? { ...prev, participants } : prev
        );
      },
    });

    return unsubscribe;
  }, [id]);

  const handleCodeChange = useCallback(
    (newCode: string) => {
      setCode(newCode);
      if (id && currentUserId) {
        updateCode({
          interviewId: id,
          code: newCode,
          participantId: currentUserId,
        });
      }
    },
    [id, currentUserId]
  );

  const handleLanguageChange = useCallback(
    (newLanguage: ProgrammingLanguage) => {
      setLanguage(newLanguage);
      setCode(getDefaultCodeTemplate(newLanguage));
      setOutput('');
      setError(undefined);
    },
    []
  );

  const handleRunCode = async () => {
    if (!id || !currentUserId) return;

    setIsExecuting(true);
    setOutput('');
    setError(undefined);

    try {
      const result = await executeCode({
        interviewId: id,
        code,
        language,
        participantId: currentUserId,
      });

      if (result.error) {
        setError(result.error);
      } else {
        setOutput(result.output);
      }
      setExecutionTime(result.executionTime);
    } catch {
      setError('Failed to execute code');
    } finally {
      setIsExecuting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-muted-foreground">Loading interview...</p>
        </div>
      </div>
    );
  }

  if (!interview) {
    return null;
  }

  return (
    <div className="h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b border-border bg-card">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Code2 className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-sm font-semibold text-foreground">
                {interview.title}
              </h1>
              <p className="text-xs text-muted-foreground">
                {interview.participants.length} participant(s) online
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <LanguageSelector value={language} onChange={handleLanguageChange} />
          <Button
            variant="execute"
            onClick={handleRunCode}
            disabled={isExecuting}
          >
            {isExecuting ? (
              <>
                <div className="w-4 h-4 border-2 border-accent-foreground border-t-transparent rounded-full animate-spin" />
                Running...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Run Code
              </>
            )}
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="w-5 h-5" />
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Editor Area */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-4">
            <CodeEditor
              code={code}
              language={language}
              onChange={handleCodeChange}
            />
          </div>
          <div className="h-64 p-4 pt-0">
            <OutputPanel
              output={output}
              error={error}
              isExecuting={isExecuting}
              executionTime={executionTime}
            />
          </div>
        </div>

        {/* Sidebar */}
        <aside className="w-80 border-l border-border bg-sidebar p-4 space-y-4 overflow-auto">
          <ShareLink link={interview.shareableLink} />
          <ParticipantList
            participants={interview.participants}
            currentUserId={currentUserId}
          />
        </aside>
      </div>
    </div>
  );
}
