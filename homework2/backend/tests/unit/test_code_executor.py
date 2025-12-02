"""
Unit tests for code executor functions.
These tests mock external dependencies.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from code_executor import execute_go_code, execute_java_code, execute_code_server
import asyncio


@pytest.mark.asyncio
async def test_execute_go_code_success():
    """Test successful Go code execution"""
    code = """
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
"""
    
    with patch('code_executor.asyncio.create_subprocess_exec') as mock_subprocess:
        # Mock successful execution
        process = AsyncMock()
        process.communicate = AsyncMock(return_value=(b"Hello, Go!\n", b""))
        mock_subprocess.return_value = process
        
        with patch('code_executor.tempfile.mkdtemp', return_value="/tmp/test"):
            with patch('code_executor.Path.write_text'):
                with patch('code_executor.subprocess.run', return_value=MagicMock()):
                    with patch('code_executor.shutil.rmtree'):
                        output, error = await execute_go_code(code, timeout=10)
                        
                        assert error is None
                        assert output is not None
                        assert "Hello, Go!" in output


@pytest.mark.asyncio
async def test_execute_go_code_not_installed():
    """Test Go code execution when Go is not installed"""
    code = "package main\nfunc main() {}"
    
    # Mock the version check to fail with FileNotFoundError
    # Now the check happens before file creation, so we don't need to mock Path.write_text
    with patch('code_executor.subprocess.run', side_effect=FileNotFoundError("go not found")):
        output, error = await execute_go_code(code, timeout=10)
        
        assert output is None
        assert error is not None
        assert "not installed" in error.lower() or "Go is not installed" in error


@pytest.mark.asyncio
async def test_execute_java_code_success():
    """Test successful Java code execution"""
    code = "System.out.println(\"Hello, Java!\");"
    
    with patch('code_executor.asyncio.create_subprocess_exec') as mock_subprocess:
        # Mock compilation
        compile_process = AsyncMock()
        compile_process.communicate = AsyncMock(return_value=(b"", b""))
        compile_process.returncode = 0
        
        # Mock execution
        run_process = AsyncMock()
        run_process.communicate = AsyncMock(return_value=(b"Hello, Java!\n", b""))
        
        mock_subprocess.side_effect = [compile_process, run_process]
        
        with patch('code_executor.tempfile.mkdtemp', return_value="/tmp/test"):
            with patch('code_executor.Path.write_text'):
                with patch('code_executor.subprocess.run', return_value=MagicMock()):
                    with patch('code_executor.shutil.rmtree'):
                        output, error = await execute_java_code(code, timeout=10)
                        
                        assert error is None
                        assert output is not None
                        assert "Hello, Java!" in output


@pytest.mark.asyncio
async def test_execute_java_code_compilation_error():
    """Test Java code execution with compilation error"""
    code = "invalid java code"
    
    with patch('code_executor.asyncio.create_subprocess_exec') as mock_subprocess:
        # Mock compilation failure
        compile_process = AsyncMock()
        compile_process.communicate = AsyncMock(return_value=(b"", b"Compilation error"))
        compile_process.returncode = 1
        
        mock_subprocess.return_value = compile_process
        
        with patch('code_executor.tempfile.mkdtemp', return_value="/tmp/test"):
            with patch('code_executor.Path.write_text'):
                with patch('code_executor.subprocess.run', return_value=MagicMock()):
                    with patch('code_executor.shutil.rmtree'):
                        output, error = await execute_java_code(code, timeout=10)
                        
                        assert output is None
                        assert error is not None
                        assert "Compilation error" in error


@pytest.mark.asyncio
async def test_execute_code_server_go():
    """Test execute_code_server with Go"""
    code = "package main\nfunc main() {}"
    
    with patch('code_executor.execute_go_code', new_callable=AsyncMock) as mock_go:
        mock_go.return_value = ("output", None)
        
        output, error = await execute_code_server(code, "go", timeout=10)
        
        assert error is None
        assert output == "output"
        mock_go.assert_called_once_with(code, 10)


@pytest.mark.asyncio
async def test_execute_code_server_java():
    """Test execute_code_server with Java"""
    code = "System.out.println(\"test\");"
    
    with patch('code_executor.execute_java_code', new_callable=AsyncMock) as mock_java:
        mock_java.return_value = ("output", None)
        
        output, error = await execute_code_server(code, "java", timeout=10)
        
        assert error is None
        assert output == "output"
        mock_java.assert_called_once_with(code, 10)


@pytest.mark.asyncio
async def test_execute_code_server_unsupported():
    """Test execute_code_server with unsupported language"""
    output, error = await execute_code_server("code", "python", timeout=10)
    
    assert output is None
    assert error is not None
    assert "not supported" in error

