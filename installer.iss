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
PrivilegesRequired=lowest
DefaultDirName={userdocs}\Quiz.iy
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

[Code]
function StartsWithText(const Prefix, S: string): Boolean;
begin
  Result := CompareText(Copy(S, 1, Length(Prefix)), Prefix) = 0;
end;

function IsInProgramFiles(const DirName: string): Boolean;
var
  PF, PF86: string;
begin
  PF := AddBackslash(ExpandConstant('{autopf}'));
  PF86 := AddBackslash(ExpandConstant('{autopf32}'));

  Result :=
    StartsWithText(PF, AddBackslash(DirName)) or
    StartsWithText(PF86, AddBackslash(DirName));
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  SelectedDir: string;
begin
  Result := True;

  if CurPageID = wpSelectDir then
  begin
    SelectedDir := WizardDirValue;

    if IsInProgramFiles(SelectedDir) then
    begin
      MsgBox(
        'Quiz.iy cannot be installed in Program Files because it needs write access to its own folder during normal use.' + #13#10#13#10 +
        'Please choose another folder, for example:' + #13#10 +
        ExpandConstant('{userdocs}\Quiz.iy'),
        mbError, MB_OK);
      Result := False;
    end;
  end;
end;