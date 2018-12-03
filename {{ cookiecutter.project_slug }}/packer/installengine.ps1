Set-ExecutionPolicy Unrestricted -Scope LocalMachine -Force -ErrorAction Ignore

# Don't set this before Set-ExecutionPolicy as it throws an error
$ErrorActionPreference = "stop"

# todo download or port in engine


# todo install wheels needed for engine wrap &"pip" install @(Get-ChildItem -Recurse -Filter *.whl)


[System.Environment]::SetEnvironmentVariable('POLYSWARM_ENGINE', '{{ cookiecutter.engine_name_slug }}', 'machine')
nssm install microengine c:\Python35\Scripts\microengine.exe """--backend {{ cookiecutter.package_slug }}"""
nssm set microengine AppDirectory C:\{{ cookiecutter.engine_name }}
nssm set microengine AppExit Default Restart
nssm set microengine AppRestartDelay 250
nssm set microengine AppStdOut c:\engine.log
nssm set microengine AppStdErr c:\engine.log
nssm set microengine Start SERVICE_DISABLED

# NOTE terraform sets KEYFILE, API_KEY, PASSWORD, BACKEND, and POLYSWARMD_ADDR systemwide in userdata at deploy time
