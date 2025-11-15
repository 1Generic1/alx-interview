✅ Step 1: Download and Extract SDelete

Go to the Microsoft Sysinternals SDelete page:
https://learn.microsoft.com/en-us/sysinternals/downloads/sdelete

This will download a ZIP file, usually named something like:

SDelete.zip


Right-click the ZIP file and choose:
Extract All...
Extract the contents to a memorable folder, for example:

makefile
Copy code
C:\SysinternalsTools\SDelete
🧑‍💻 Step 2: Open PowerShell as Administrator
Press Start, type PowerShell.

Right-click Windows PowerShell, then choose:

csharp
Copy code
Run as administrator
Change directory to the folder where you extracted sdelete.exe:

powershell
Copy code
cd "C:\SysinternalsTools\SDelete"
You should see files like:

Copy code
sdelete.exe
Eula.txt
📜 Step 3: Accept the License Agreement
Run SDelete once to accept the EULA:
.\sdelete.exe
You'll be prompted to accept the license agreement. Press Y to accept.

🔐 Step 4: Securely Delete a File
You can now use SDelete to securely erase a file.

Example:
powershell
Copy code
sdelete -p 5 -s -z "t.txt"
Explanation of flags:
-p 5: Overwrite the file 5 times (more passes = better security).

-s: (Optional) If you're deleting a folder, this makes it delete all files inside, including subdirectories.

-z: Zero out free space on the disk after deletion, to clean remnants of previously deleted files.

🛑 After this, the file is permanently unrecoverable.

🧩 Step 5: Add SDelete to System PATH (Optional but Recommended)
Adding SDelete to your system PATH lets you run it from any location in Command Prompt or PowerShell.

How to Add to PATH:
Press Windows + R, type:

Copy code
sysdm.cpl
Press Enter — this opens System Properties.

Go to the Advanced tab, then click:

mathematica
Copy code
Environment Variables…
Under System variables, find and select:

mathematica
Copy code
Path
Click Edit, then New, and add the folder where you extracted SDelete:

makefile
Copy code
C:\SysinternalsTools\SDelete
Click OK to save and close all windows.

🔁 Step 6: Test It from Anywhere
Open a new Command Prompt or PowerShell window.

Type:

powershell

sdelete
If it runs and shows the usage info, it's now available globally.

📌 Summary
Step	Action
1	Download & extract SDelete.zip
2	Run PowerShell as Administrator
3	Run .sdelete.exe once to accept the EULA
4	Use sdelete -p -s -z to securely delete files
5	Add SDelete's folder to System PATH
6	Test it from any command window


Download SDelete.zip from the official Microsoft Sysinternals site.

Extract it to C:\SysinternalsTools\SDelete (you can change this path).

Run sdelete.exe once to accept the license (you’ll need to press Y manually).

Add the SDelete folder to the System PATH (if not already added).

# Set variables
$downloadUrl = "https://download.sysinternals.com/files/SDelete.zip"
$destinationFolder = "C:\SysinternalsTools\SDelete"
$zipPath = "$env:TEMP\SDelete.zip"

# Step 1: Create destination folder
if (-not (Test-Path $destinationFolder)) {
    New-Item -Path $destinationFolder -ItemType Directory -Force
}

# Step 2: Download SDelete.zip
Write-Host "Downloading SDelete from Microsoft..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

# Step 3: Extract the ZIP file
Write-Host "Extracting SDelete to $destinationFolder..." -ForegroundColor Cyan
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $destinationFolder)

# Step 4: Run sdelete.exe once to accept the EULA
Write-Host "Launching sdelete.exe. You must manually accept the license (press Y)..." -ForegroundColor Yellow
Start-Process -FilePath "$destinationFolder\sdelete.exe" -Wait

# Step 5: Add folder to System PATH if not already there
$existingPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($existingPath -notlike "*$destinationFolder*") {
    Write-Host "Adding $destinationFolder to system PATH..." -ForegroundColor Cyan
    $newPath = "$existingPath;$destinationFolder"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    Write-Host "✅ SDelete path added to system PATH." -ForegroundColor Green
} else {
    Write-Host "ℹ️ Path already exists in system PATH." -ForegroundColor Yellow
}

# Cleanup
Remove-Item $zipPath -Force
Write-Host "🎉 SDelete setup complete! You can now use 'sdelete' from any command window." -ForegroundColor Green


✅ How to Use the Script

Open PowerShell as Administrator

Press Start → Type PowerShell → Right-click → Run as administrator

Paste and run the script above.

📝 After Running the Script

You’ll still need to press Y once manually when the EULA prompt appears.

After that, you can use SDelete like this from any folder:

sdelete -p 2 -z "C:\Path\to\file.txt"