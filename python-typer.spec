%define module typer
%define oname typer
# disable test on abf
%bcond_with test

# NOTE Update the python-typer-slim package prior to updating this package
# NOTE in order to keep them in sync.
# NOTE Upstream python-typer & python-typer-slim releases are version synced.

Name:		python-typer
Version:	0.15.2
Release:	2
Summary:	Typer, build great CLIs. Easy to code. Based on Python type hints
URL:		https://pypi.org/project/typer/
License:	MIT
Group:		Development/Python
Source0:	https://files.pythonhosted.org/packages/source/t/typer/typer-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch

BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pdm-backend)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pre-commit)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(typer-slim)
BuildRequires:	python%{pyver}dist(click) >= 8.0.0
BuildRequires:	python%{pyver}dist(typing-extensions) >= 3.7.4.3
BuildRequires:	python%{pyver}dist(rich) >= 10.11.0
BuildRequires:	python%{pyver}dist(shellingham) >= 1.3.0
%if %{with test}
BuildRequires:	python%{pyver}dist(click) >= 8.0.0
BuildRequires:	python%{pyver}dist(markdown-it-py)
BuildRequires:	python%{pyver}dist(mdurl)
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-xdist)
BuildRequires:	python%{pyver}dist(rich) >= 10.11.0
BuildRequires:	python%{pyver}dist(shellingham) >= 1.3.0
BuildRequires:	python%{pyver}dist(typing-extensions) >= 3.7.4.3
%endif
Requires:	python%{pyver}dist(typer-slim) >= %{version}
Requires:	python%{pyver}dist(click) >= 8.0.0
Requires:	python%{pyver}dist(typing-extensions) >= 3.7.4.3
Requires:	python%{pyver}dist(rich) >= 10.11.0
Requires:	python%{pyver}dist(shellingham) >= 1.3.0
# python-typer binary name-conflict with ErLang TyPer application
Conflicts:	erlang

%description
Typer is a library for building CLI applications that users will love using
and developers will love creating. Based on Python type hints.

It's also a command line tool to run scripts, automatically converting them
to CLI applications.

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
%py_build

%install
%py3_install
# Remove conflicting files that are included with the python-typer-slim package
rm -r %{buildroot}%{py_sitedir}/typer

%if %{with test}
%check
pip install -e .[test]
%{__python} -m pytest --import-mode append -v -rs -k 'not test_show_completion and not test_install_completion' #"${ignore-}"
%endif

%files
%{_bindir}/typer
%{py_sitedir}/%{oname}-%{version}.dist-info
%license LICENSE
%doc README.md
