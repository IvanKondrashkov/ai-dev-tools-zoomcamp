import asyncio
import tempfile
import os
import shutil
from pathlib import Path
from typing import Tuple, Optional
import subprocess


async def execute_go_code(code: str, timeout: int = 10) -> Tuple[Optional[str], Optional[str]]:
    """
    Execute Go code on the server.
    Returns (output, error) tuple.
    """
    temp_dir = None
    try:
        # First check if 'go' is available before creating files
        try:
            subprocess.run(["go", "version"], check=True, capture_output=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None, "Go is not installed on the server. Please install Go to enable Go code execution."
        
        # Create temporary directory for Go code
        temp_dir = tempfile.mkdtemp(prefix="go_exec_")
        go_file = Path(temp_dir) / "main.go"
        
        # Write code to file
        go_file.write_text(code, encoding="utf-8")
        
        # Execute Go code
        
        # Run the Go code
        process = await asyncio.create_subprocess_exec(
            "go",
            "run",
            str(go_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
        except asyncio.TimeoutExpired:
            process.kill()
            await process.wait()
            return None, f"Code execution timed out after {timeout} seconds"
        
        output = stdout.decode("utf-8", errors="replace") if stdout else ""
        error = stderr.decode("utf-8", errors="replace") if stderr else ""
        
        # If there's stderr but no stdout, it's likely a compilation/runtime error
        if error and not output:
            return None, error
        
        return output, None
        
    except Exception as e:
        return None, f"Execution error: {str(e)}"
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_java_code(code: str, timeout: int = 10) -> Tuple[Optional[str], Optional[str]]:
    """
    Execute Java code on the server.
    Returns (output, error) tuple.
    """
    temp_dir = None
    try:
        # First check if Java is available before creating files
        try:
            subprocess.run(["java", "-version"], check=True, capture_output=True, timeout=5)
            subprocess.run(["javac", "-version"], check=True, capture_output=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None, "Java/JDK is not installed on the server. Please install JDK to enable Java code execution."
        
        # Create temporary directory for Java code
        temp_dir = tempfile.mkdtemp(prefix="java_exec_")
        
        # Check if code already has a class definition
        if "public class" not in code and "class" not in code:
            # Wrap code in a Main class
            java_code = f"""public class Main {{
    public static void main(String[] args) {{
        {code}
    }}
}}"""
        else:
            java_code = code
        
        # Extract class name from code
        class_name = "Main"
        if "public class" in java_code:
            # Try to extract class name
            start = java_code.find("public class") + len("public class")
            end = java_code.find("{", start)
            if end > start:
                class_name = java_code[start:end].strip().split()[0]
        
        java_file = Path(temp_dir) / f"{class_name}.java"
        java_file.write_text(java_code, encoding="utf-8")
        
        # Compile Java code
        compile_process = await asyncio.create_subprocess_exec(
            "javac",
            str(java_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
        )
        
        compile_stdout, compile_stderr = await asyncio.wait_for(
            compile_process.communicate(), timeout=10
        )
        
        if compile_process.returncode != 0:
            error = compile_stderr.decode("utf-8", errors="replace") if compile_stderr else "Compilation failed"
            return None, f"Compilation error: {error}"
        
        # Execute compiled Java code
        run_process = await asyncio.create_subprocess_exec(
            "java",
            "-cp",
            str(temp_dir),
            class_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                run_process.communicate(), timeout=timeout
            )
        except asyncio.TimeoutExpired:
            run_process.kill()
            await run_process.wait()
            return None, f"Code execution timed out after {timeout} seconds"
        
        output = stdout.decode("utf-8", errors="replace") if stdout else ""
        error = stderr.decode("utf-8", errors="replace") if stderr else ""
        
        # If there's stderr but no stdout, it's likely a runtime error
        if error and not output:
            return None, error
        
        return output, None
        
    except Exception as e:
        return None, f"Execution error: {str(e)}"
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_code_server(code: str, language: str, timeout: int = 10) -> Tuple[Optional[str], Optional[str]]:
    """
    Execute code on the server for supported languages.
    Returns (output, error) tuple.
    """
    if language == "go":
        return await execute_go_code(code, timeout)
    elif language == "java":
        return await execute_java_code(code, timeout)
    else:
        return None, f"Server-side execution not supported for {language}"

