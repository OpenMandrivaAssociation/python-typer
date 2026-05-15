%define module typer
%bcond tests 1

Name:		python-typer
Version:	0.25.1
Release:	1
Summary:	Typer, build great CLIs. Easy to code. Based on Python type hints
License:	MIT
Group:		Development/Python
URL:		https://github.com/fastapi/typer
Source0:	%{URL}/archive/%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(annotated-doc)
BuildRequires:	python%{pyver}dist(click)
BuildRequires:	python%{pyver}dist(pdm-backend)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pre-commit)
BuildRequires:	python%{pyver}dist(rich)
BuildRequires:	python%{pyver}dist(shellingham)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	procps-ng
BuildRequires:	python%{pyver}dist(click)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-xdist)
%endif
Requires:	python%{pyver}dist(annotated-doc) >= 0.02
Requires:	python%{pyver}dist(click) >= 8.2.1
Requires:	python%{pyver}dist(rich) >= 13.8.0
Requires:	python%{pyver}dist(shellingham) >= 1.3.0

# python-typer binary name-conflict with ErLang TyPer application
Conflicts:	erlang
# typer-slim is obsoleted upstream and is only a wrapper around typer,
# meaning we have no reason to have duplicated packages.
%rename python-typer-slim

%description
Typer is a library for building CLI applications that users will love using
and developers will love creating. Based on Python type hints.

It's also a command line tool to run scripts, automatically converting them
to CLI applications.

%prep -a
# LLM crap
rm -r typer/.agents

%install -a
install -d '%{buildroot}%{_datadir}/bash-completion/completions' \
	'%{buildroot}%{_datadir}/fish/vendor_completions.d' \
	'%{buildroot}%{_datadir}/zsh/site-functions/'

export PYTHONPATH="%{buildroot}%{python_sitelib}"
export _TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION=1

'%{buildroot}%{_bindir}/typer' --show-completion bash \
    > '%{buildroot}%{_datadir}/bash-completion/completions/typer'
'%{buildroot}%{_bindir}/typer' --show-completion fish \
    > '%{buildroot}%{_datadir}/fish/vendor_completions.d/typer.fish'
'%{buildroot}%{_bindir}/typer' --show-completion zsh \
    > '%{buildroot}%{_datadir}/zsh/site-functions/_typer'

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
# Env variables taken from scripts/test.sh
export TERMINAL_WIDTH=3000
export _TYPER_FORCE_DISABLE_TERMINAL=1
export _TYPER_RUN_INSTALL_COMPLETION_TESTS=1
skiptests+="not test_enum and not test_tutorial003 and not test_tutorial001"
skiptests+=" and not test_script_completion_run"
skiptests+=" and not test_completion_show_invalid_shell"
skiptests+=" and not test_invalid_score"
pytest -rs -k "$skiptests"
%endif

%files
%doc README.md
%{_bindir}/typer
%{_datadir}/bash-completion/completions/%{module}
%{_datadir}/fish/vendor_completions.d/%{module}.fish
%{_datadir}/zsh/site-functions/_%{module}
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
