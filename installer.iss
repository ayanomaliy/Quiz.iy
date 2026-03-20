#define MyAppName "Quiz.iy"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ayanomaliy"
#define MyAppURL "https://github.com/ayanomaliy/Quiz.iy"
#define MyAppExeName "quiziy.exe"

[Setup]
AppId={{C8B7A9D8-7D9F-4F67-9A44-QUIZIY001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Quiz.iy
DefaultGroupName=Quiz.iy
DisableDirPage=no
AllowNoIcons=yes
OutputDir=installer-output
OutputBaseFilename=Quiz.iy-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\quiziy.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Quiz.iy"; Filename: "{app}\quiziy.exe"
Name: "{autodesktop}\Quiz.iy"; Filename: "{app}\quiziy.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\quiziy.exe"; Description: "Launch Quiz.iy"; Flags: nowait postinstall skipifsilent