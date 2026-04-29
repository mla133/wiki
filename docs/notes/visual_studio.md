# Markdown

# MSBuild Command-Line Usage (Visual Studio 2019)

This repository documents how **Visual Studio 2019 builds solutions**, how to invoke **MSBuild from the command line**, and how to safely work with MSBuild when **multiple Visual Studio versions** are installed on the same machine.
The guidance here applies to:
- Visual Studio 2019 (MSBuild **16.x**)
- Mixed environments with VS 2019 + VS 2022
- Local development, scripting, and CI usage
---

## Table of Contents
- [How Visual Studio Builds Solutions](#how-visual-studio-builds-solutions)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Command-Line Build Options](#command-line-build-options)
- [When `msbuild` Is Not Found](#when-msbuild-is-not-found)
- [Locating Visual Studio 2019 and MSBuild](#locating-visual-studio-2019-and-msbuild)
- [Adding MSBuild to PATH (User Scope)](#adding-msbuild-to-path-user-scope)
- [Reverting the PATH Change](#reverting-the-path-change)
- [Verifying the Active MSBuild Version](#verifying-the-active-msbuild-version)
- [Recommended Best Practice (PATH-Free Builds)](#recommended-best-practice-path-free-buildses
   - Calls the appropriate compiler:
     - `csc.exe` for C#
     - `cl.exe` / `link.exe` for C++

**Building from the command line uses the exact same MSBuild engine.**

---

## Prerequisites
- Visual Studio 2019 installed    (Community, Professional, or Enterprise)
- Workloads installed for your project type:
  - **C++**: “Desktop development with C++”
  - **.NET**: “.NET desktop development” or equivalent
- PowerShell or Command Prompt

---

## Quick Start
### Using Developer Command Prompt (recommended for interactive use)
1. Open **Developer Command Prompt for VS 2019**
2. Navigate to the solution directory
3. Build:

```powershell
msbuild AccuMate.sln /p:Configuration=Release
```

This prompt automatically sets:

- PATH
- MSBuild
- Compiler toolchains
- Windows SDKs


## Command-Line Build Options
MSBuild (recommended)
```powershell
msbuild AccuMate.sln /p:Configuration=Release
```
### Common options:
```powershell
msbuild AccuMate.sln /m
msbuild AccuMate.sln /t:Clean
msbuild AccuMate.sln /t:Rebuild
msbuild AccuMate.sln /p:Configuration=Release /p:Platform=x64
```

/m enables parallel builds
/t: selects build targets

---

## When msbuild Is Not Found
If you see:
```powershell
msbuild : The term 'msbuild' is not recognized
```

This is expected unless:

* You are using the Developer Command Prompt, or
* MSBuild has been added to PATH


### Locating Visual Studio 2019 and MSBuild
When multiple Visual Studio versions are installed, do not guess paths.
Use vswhere (official and reliable)
PowerShell-safe command:

```powershell

"$Env:ProgramFiles(x86)\Microsoft Visual Studio\Installer\vswhere.exe"
  -version '[16.0,17.0)' 
  -products * 
  -property installationPath
```

* Visual Studio 2019 → 16.x
* Visual Studio 2022 → 17.x


### Locate MSBuild.exe Directly
```powershell
"$Env:ProgramFiles(x86)\Microsoft Visual Studio\Installer\vswhere.exe" 
  -version '[16.0,17.0)' 
  -requires Microsoft.Component.MSBuild 
  -find 'MSBuild\**\Bin\MSBuild.exe'
```

Typical result:
```
C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\MSBuild\Current\Bin\MSBuild.exe
```

### Adding MSBuild to PATH (User Scope)
This modifies only your user environment (no admin required).
```powershell
:SetEnvironmentVariable(  "Path",  :GetEnvironmentVariable("Path", "User") + ";C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\MSBuild\Current\Bin",  "User")
```
Notes:

* Close and reopen all shells after running
* Prefer User PATH over Machine PATH
* Avoid mixing MSBuild 16.x and 17.x unintentionally


### Reverting the PATH Change
To remove MSBuild 2019 from the User PATH:
```powershell
$remove = 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\MSBuild\Current\Bin':SetEnvironmentVariable(  'Path',  (:GetEnvironmentVariable('Path','User') -split ';' | Where-Object { $_ -ne $remove }) -join ';',  'User')
```
Restart shells to apply.

### Verifying the Active MSBuild Version
```powershell
where msbuild
msbuild -version
```

Expected for Visual Studio 2019:
```
Microsoft (R) Build Engine version 16.x.x
```

If you see 17.x, you are using Visual Studio 2022 instead.

### Recommended Best Practice (PATH-Free Builds)
For scripts and CI, avoid modifying PATH entirely.
```powershell
$msbuild = "$Env:ProgramFiles(x86)\Microsoft Visual Studio\Installer\vswhere.exe"   -version '[16.0,17.0)'   -requires Microsoft.Component.MSBuild   -find 'MSBuild\**\Bin\MSBuild.exe'& $msbuild AccuMate.sln /p:Configuration=Release
```

Benefits:

* Always selects the correct MSBuild version
* Safe with multiple Visual Studio installs
* CI-friendly and reproducible

---

Key Takeaways

* Visual Studio is a front-end to MSBuild
* MSBuild is the authoritative build engine
* vswhere is the correct way to locate build tools
* Prefer explicit MSBuild invocation in scripts
* Avoid global PATH pollution when possible
