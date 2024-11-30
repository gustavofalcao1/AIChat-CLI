[Setup]
OutputDir=.
OutputBaseFilename=aichat-setup
AppName=AiChat CLI
AppVersion=1.0
DefaultDirName={pf}\AiChat
DefaultGroupName=AiChat
PrivilegesRequired=admin

[Files]
Source: "dist\aichat-cli.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AiChat CLI"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\aichat-cli.exe'"""; WorkingDir: "{app}"
Name: "{commondesktop}\AiChat CLI"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\aichat-cli.exe'"""; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\aichat-cli.exe'"""; Description: "{cm:LaunchProgram,AiChat CLI}"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Code]
const
  WM_SETTINGCHANGE = $001A;

procedure ExecuteCommand(Command: String; var ResultCode: Integer);
begin
  if not Exec('powershell.exe', '-Command "' + Command + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    MsgBox('Failed to execute: ' + Command, mbError, MB_OK);
    WizardForm.ProgressGauge.Style := npbstNormal;
    WizardForm.ProgressGauge.Position := 0;
    WizardForm.StatusLabel.Caption := 'Installation failed.';
    Abort;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  OldPath: string;
  NewPath: string;
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    WizardForm.ProgressGauge.Style := npbstMarquee;
    WizardForm.ProgressGauge.Position := 0;
    WizardForm.StatusLabel.Caption := 'Preparing installation...';

    ExecuteCommand('if (Test-Path AIChat-CLI) { Remove-Item -Recurse -Force AIChat-CLI }', ResultCode);
    WizardForm.ProgressGauge.Position := 10;

    ExecuteCommand('git clone https://github.com/gustavofalcao1/AIChat-CLI.git', ResultCode);
    WizardForm.ProgressGauge.Position := 30;

    ExecuteCommand('cd AIChat-CLI; python -m venv venv', ResultCode);
    WizardForm.ProgressGauge.Position := 50;

    ExecuteCommand('cd AIChat-CLI; .\\venv\\Scripts\\Activate.ps1; pip install -r requirements.txt', ResultCode);
    WizardForm.ProgressGauge.Position := 70;

    ExecuteCommand('cd AIChat-CLI; .\\venv\\Scripts\\Activate.ps1; python setup.py install', ResultCode);
    WizardForm.ProgressGauge.Position := 90;

    ExecuteCommand('cd AIChat-CLI; .\\venv\\Scripts\\Activate.ps1; python build.py', ResultCode);
    WizardForm.ProgressGauge.Position := 100;

    ExecuteCommand('Remove-Item -Recurse -Force AIChat-CLI', ResultCode);
  end;

  if CurStep = ssPostInstall then
  begin
    if not RegQueryStringValue(HKCU, 'Environment', 'Path', OldPath) then
      OldPath := '';
    if Pos(';' + ExpandConstant('{app}'), OldPath) = 0 then
    begin
      NewPath := OldPath + ';' + ExpandConstant('{app}');
      if not RegWriteStringValue(HKCU, 'Environment', 'Path', NewPath) then
        MsgBox('Failed to update user PATH variable.', mbError, MB_OK);
      SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 0);
    end;

    // Adiciona um alias ao PowerShell para o comando 'aichat'
    ExecuteCommand('Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force', ResultCode);
    ExecuteCommand('if (!(Test-Path -Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }', ResultCode);
    ExecuteCommand('Add-Content -Path $PROFILE -Value "`nSet-Alias -Name aichat -Value ' + ExpandConstant('{app}\aichat-cli.exe') + '"', ResultCode);
  end;
end;