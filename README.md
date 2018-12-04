# About

This is a template project for wrapping scan engines into PolySwarm.

It supports both Linux (Docker) and Windows (AMI)-based engines. 
You must use python3 >= 3.5.4.

# Getting Started

1. Install `cookiecutter`:
```bash
pip install cookiecutter
```

2. Start a new engine project:
```bash
cookiecutter https://github.com/polyswarm/engine-template
```

# Prompts

When creating an engine with `cookiecutter`, you'll receive several prompts:
1. `engine_name`: the name of your engine
1. `engine_name_slug`: engine_name converted to a slug (usually accept the default)
1. `project_slug`: name for project directory as a slug (usually accept the default)
1. `author_org`: the name of your organization
1. `author_org_slug`: author_org converted to a slug (usually accept the default)
1. `author_name`: your name
1. `author_email`: your email address
1. `platform`: Windows or Linux-based
1. `has_backend`: whether your scan engine "frontend" is disjoint from your scan engine "backend" by way of a network socket (see below)
1. `aws_account_for_ami`: (Windows only) the AWS account ID you will use for hosting the Windows AMIs you generate with `cookiecutter`

## has_backend

Most of these are straightforward, save `has_backend`.

When wrapping your scan engine, inheritance of `polyswarm-client` classes and implementation of class functionality are referred to as "frontend" changes.
If your scan engine "frontend" must reach out across a network or local socket to a separate process that does the real scanning work (the "backend"), then you have a disjoint "backend" and you should answer `yes` to `has_backend`.
If instead your scan engine can easily be encapsulated in a single Docker image (Linux) or AMI (Windows), then you should select `no` for `has_backend`.

Example of disjoint frontend / backend:
* ClamAV: https://github.com/polyswarm/polyswarm-client/blob/5959742f0014a582baf5046c7bf6694c23f7435e/src/microengine/clamav.py#L18

Example of only a frontend (has_backend is false):
* Yara: https://github.com/polyswarm/polyswarm-client/blob/master/src/microengine/yara.py

# Creating a Linux Engine

Linux Docker projects are based directly on `polyswarm-client`.

If your scanner does not have a disjoint "backend" (see above), configuration is likely as simple as:
1. Make modifications to `myengine.py` per tutorials found at `https://docs.polyswarm.io`.
2. Have these modifications call out to, e.g. your command line scanner binary.
3. Include your scanner binary / SDK in the `Dockerfile`.
4. If your scanner does have a disjoint "backend", then you'll also need to author a Docker Compose file (`docker-compose.yml`) that describes this backend service and exposes it to the frontend `polyswarm-client` modifications.

See references in `has_backend` section above for examples.


# Creating a Windows Engine

Docker on Windows leaves a lot to be desired, so instead we use [Packer](https://www.packer.io/) to build Windows-based [AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html).

Windows-based engines are built in 2 stages:
1. We build a skeleton Windows AMI with Python on [Windows builds of `polyswarm-client` libraries installed](https://github.com/polyswarm/polyswarm-client).
2. `cookiecutter` produces a template microengine wrap project that contains a Packer template and Continuous Integration (CI) instructions to build & push the resultant AMI.

# Wrapping Up

Once your engine is complete, you'll likely want to initialize it as a git repo, commit your files, and push it to your host of choice. Run all git commands from the root of your engine directory.

```bash
cd engine-MYENGINE
git init
git add YOUR_LIST_OF_FILES
git commit -m "YOUR COMMIT MESSAGE"

... more git commands ...
```
