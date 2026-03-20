[Setup]
AppId={{C8B7A9D8-7D9F-4F67-9A44-QUIZIY001}}
AppName=Quiz.iy
AppVersion=1.0.0
AppPublisher=ayanomaliy
DefaultDirName={autopf}\Quiz.iy
DefaultGroupName=Quiz.iy
OutputDir=installer-output
OutputBaseFilename=Quiz.iy-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\quiziy.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Quiz.iy"; Filename: "{app}\quiziy.exe"
Name: "{autodesktop}\Quiz.iy"; Filename: "{app}\quiziy.exe"

[Run]
Filename: "{app}\quiziy.exe"; Description: "Launch Quiz.iy"; Flags: nowait postinstall skipifsilent