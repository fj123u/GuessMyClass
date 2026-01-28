; Script Inno Setup pour GuessMyClass
; Mis à jour : 04/12/2025

#define MyAppName "GuessMyClass"
#define MyAppVersion "1.0"
#define MyAppExeName "GuessMyClass.exe"
#define MyAppPublisher "Votre Nom"
#define MyAppURL "https://votre-site-web.com"
#define MyAppSourcePath "GMC_fonctionnel\dist"
#define MyIconPath "GMC_fonctionnel\gmc.ico"
#define MyLicenseFile "GMC_fonctionnel\docs\licence.txt"

[Setup]
AppId={{6F48AC12-B30A-4D97-9E3F-72E8C160F2A1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

AllowNoIcons=yes
SetupIconFile={#MyIconPath}

UninstallDisplayIcon={app}\{#MyAppExeName}

OutputDir=dist_installer
OutputBaseFilename={#MyAppName}_Installer

; --- Compression maximale mais stable ---
Compression=lzma2/ultra64
SolidCompression=yes

; --- Windows 10 minimum ---
MinVersion=10.0

DisableDirPage=no
DisableProgramGroupPage=yes
LanguageDetectionMethod=locale

; --- Affichage de la licence ---
LicenseFile={#MyLicenseFile}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[CustomMessages]
english.LaunchProgram=Launch %1
english.AdditionalIcons=Additional icons:
english.CreateDesktopIcon=Create a Desktop icon

french.LaunchProgram=Lancer %1
french.AdditionalIcons=Icônes supplémentaires :
french.CreateDesktopIcon=Créer un raccourci sur le Bureau

[Files]
; Inclut automatiquement TOUT le contenu du dist dans le dossier d'installation
Source: "{#MyAppSourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Menu Démarrer
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Icône Bureau (optionnelle)
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
