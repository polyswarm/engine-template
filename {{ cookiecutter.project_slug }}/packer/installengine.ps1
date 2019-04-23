Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force -ErrorAction Ignore

# Don't set this before Set-ExecutionPolicy as it throws an error
$ErrorActionPreference = "stop"

# CUSTOMIZE_HERE
# This is where you'd download or copy in your scanner binary using PowerShell.

# CUSTOMIZE_HERE
# As needed, download or copy Python wheel files into the wheel directory for installation.
&"pip" install @(Get-ChildItem -Recurse -Filter *.whl)

[System.Environment]::SetEnvironmentVariable('POLYSWARM_ENGINE', '{{ cookiecutter.participant_name_slug }}', 'machine')
nssm install microengine c:\Python35\Scripts\microengine.exe """--backend {{ cookiecutter.package_slug }}"""
nssm set microengine AppDirectory C:\{{ cookiecutter.participant_name }}
nssm set microengine AppExit Default Restart
nssm set microengine AppRestartDelay 250
nssm set microengine AppStdOut c:\engine.log
nssm set microengine AppStdErr c:\engine.log
nssm set microengine Start SERVICE_DISABLED
