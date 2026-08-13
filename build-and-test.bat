@echo off
REM =====================================================================
REM CppCheckDocker — local build and integration-test driver (Windows).
REM
REM Requirements:
REM   * Docker Desktop running
REM   * Git for Windows (bash.exe on PATH) — used to run the POSIX test
REM     harness at test\integration\run.sh
REM
REM Optional arguments:
REM   %1  CPPCHECK_VERSION  (default: 2.21.1)
REM   %2  UBUNTU_VERSION    (default: 24.04)
REM
REM Exit codes:
REM   0   build + all tests passed
REM   1   docker not available
REM   2   image build failed
REM   3   version smoke test failed
REM   4   bash / integration harness not available or failed
REM =====================================================================

setlocal EnableDelayedExpansion

set "CPPCHECK_VERSION=%~1"
if "%CPPCHECK_VERSION%"=="" set "CPPCHECK_VERSION=2.21.1"

set "UBUNTU_VERSION=%~2"
if "%UBUNTU_VERSION%"=="" set "UBUNTU_VERSION=24.04"

set "IMAGE=cppcheck:%CPPCHECK_VERSION%"
set "SCRIPT_DIR=%~dp0"

echo.
echo === CppCheckDocker local build ===
echo   Cppcheck version : %CPPCHECK_VERSION%
echo   Ubuntu version   : %UBUNTU_VERSION%
echo   Image tag        : %IMAGE%
echo   Working dir      : %SCRIPT_DIR%
echo.

REM ---------- prereqs ----------
where docker >nul 2>&1
if errorlevel 1 (
    echo ERROR: docker not on PATH. Start Docker Desktop and reopen this shell.
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: docker daemon not reachable. Is Docker Desktop running?
    exit /b 1
)

REM ---------- build ----------
echo === Building image ===
pushd "%SCRIPT_DIR%" >nul
docker build ^
    --build-arg CPPCHECK_VERSION=%CPPCHECK_VERSION% ^
    --build-arg UBUNTU_VERSION=%UBUNTU_VERSION% ^
    -t %IMAGE% ^
    -t cppcheck:latest ^
    .
if errorlevel 1 (
    popd >nul
    echo.
    echo ERROR: docker build failed.
    exit /b 2
)
popd >nul

REM ---------- version smoke test ----------
echo.
echo === Version smoke test ===
for /f "usebackq delims=" %%V in (`docker run --rm %IMAGE% --version`) do set "ACTUAL_VERSION=%%V"
echo   actual   : !ACTUAL_VERSION!
echo   expected : Cppcheck %CPPCHECK_VERSION%
if not "!ACTUAL_VERSION!"=="Cppcheck %CPPCHECK_VERSION%" (
    echo ERROR: version mismatch.
    exit /b 3
)

REM ---------- integration tests ----------
echo.
echo === Integration tests ===

REM Find bash.exe from Git for Windows.
set "BASH_EXE="
for %%B in (
    "%ProgramFiles%\Git\bin\bash.exe"
    "%ProgramFiles(x86)%\Git\bin\bash.exe"
    "%LOCALAPPDATA%\Programs\Git\bin\bash.exe"
) do (
    if exist %%~B set "BASH_EXE=%%~B"
)
if "%BASH_EXE%"=="" (
    where bash >nul 2>&1
    if not errorlevel 1 (
        for /f "usebackq delims=" %%B in (`where bash`) do set "BASH_EXE=%%B"
    )
)
if "%BASH_EXE%"=="" (
    echo ERROR: bash.exe not found. Install Git for Windows or add bash to PATH.
    exit /b 4
)

echo   Using bash: %BASH_EXE%
"%BASH_EXE%" -c "cd '%SCRIPT_DIR:\=/%' && test/integration/run.sh %IMAGE%"
if errorlevel 1 (
    echo.
    echo ERROR: integration tests failed.
    exit /b 4
)

echo.
echo === All checks passed ===
echo Image %IMAGE% is ready. Try:
echo   docker run --rm -v "%%CD%%:/work:ro" %IMAGE% --enable=all src/
exit /b 0
