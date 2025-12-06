"""Mock code execution service."""
import asyncio
import random
from app.models import ProgrammingLanguage


class CodeExecutor:
    """Mock code executor that simulates code execution."""
    
    # Mock outputs for different languages
    MOCK_OUTPUTS = {
        ProgrammingLanguage.PYTHON: "Hello from Python!\n",
        ProgrammingLanguage.JAVASCRIPT: "Hello from JavaScript!\n",
        ProgrammingLanguage.TYPESCRIPT: "Hello from TypeScript!\n",
        ProgrammingLanguage.JAVA: "Hello from Java!\n",
        ProgrammingLanguage.CPP: "Hello from C++!\n",
        ProgrammingLanguage.GO: "Hello from Go!\n",
        ProgrammingLanguage.RUST: "Hello from Rust!\n",
    }
    
    async def execute(self, code: str, language: ProgrammingLanguage) -> tuple[str, str | None, float]:
        """
        Execute code and return (output, error, execution_time).
        
        This is a mock implementation that simulates execution.
        In production, this would use a sandboxed environment.
        """
        # Simulate execution time
        execution_time = random.uniform(50, 200)
        await asyncio.sleep(execution_time / 1000)  # Convert to seconds
        
        # Check for common error patterns in code
        error = None
        output = ""
        
        if "error" in code.lower() or "throw" in code.lower():
            error = f"Simulated error in {language.value} code"
        elif "print" in code.lower() or "console.log" in code.lower() or "System.out" in code:
            # Try to extract what's being printed
            if '"' in code or "'" in code:
                # Simple extraction of string literals
                import re
                matches = re.findall(r'["\']([^"\']+)["\']', code)
                if matches:
                    output = "\n".join(matches) + "\n"
                else:
                    output = self.MOCK_OUTPUTS.get(language, "Output\n")
            else:
                output = self.MOCK_OUTPUTS.get(language, "Output\n")
        else:
            # Default output for the language
            output = self.MOCK_OUTPUTS.get(language, "Code executed successfully\n")
        
        return output, error, execution_time


# Global executor instance
code_executor = CodeExecutor()
