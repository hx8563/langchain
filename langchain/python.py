"""Mock Python REPL."""
import sys
import traceback
from io import StringIO
from typing import Dict, Optional

from pydantic import BaseModel, Field


class PythonREPL(BaseModel):
    """Simulates a standalone Python REPL."""

    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
    locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

    def run(self, command: str) -> str:
        """Run command with own globals/locals and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self.globals, self.locals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception:
            sys.stdout = old_stdout
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace_info = traceback.format_exception(exc_type, exc_value, exc_traceback)
            output = "\n".join(trace_info)
        return output
