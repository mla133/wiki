# File: note.ps1

# Set directory path and file name
$dir = "~\wiki"
$file = "inbox.md"

# Create the directory if it doesn't exist
if (!(Test-Path $dir)) {
	New-Item -ItemType Directory -Path $dir
}

# Append the current date to the file
(Get-Date) | Add-Content -Path $file

# Check if any command-line arguments were passed
if ($args.Length -ne 0) {
	# Append the arguments to the file
	$args | Add-Content -Path $file
}

# Open the file in Notepad (vim)
vim $file
