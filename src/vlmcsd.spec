Name:           vlmcsd
Version:        svn1113
Release:        1%{?dist}
Summary:        A fully Microsoft compatible KMS server

License:        Unknown
URL:            https://github.com/Wind4/vlmcsd
Source0:        https://github.com/Wind4/vlmcsd/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        vlmcsd.service
Source2:        kms.xml
Patch0:         vlmcsd-svn1113-build.patch


BuildRequires:    rpm-build
BuildRequires:    make
BuildRequires:    gcc

Requires:         systemd

%description
vlmcsd is a fully Microsoft compatible KMS server that provides product
activation services to clients. It is meant as  a  drop-in  replacement
for  a Microsoft KMS server (Windows computer with KMS key entered). It
currently supports KMS protocol versions 4, 5 and 6.
Although vlmcsd does neither require an activation key nor a payment to
anyone,  it  is not meant to run illegal copies of Windows. Its purpose
is to ensure that owners of legal copies can use their software without
restrictions,  e.g.  if  you buy a new computer or motherboard and your
key will be refused activation from Microsoft servers due  to  hardware
changes.

%prep
%autosetup

%build
%set_build_flags
%make_build STRIP=0
%make_build unixdocs

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/vlmcsd.service
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
install -p -m 644 %{SOURCE2} %{buildroot}%{_prefix}/lib/firewalld/services/kms.xml

%pre
/usr/sbin/groupadd -r vlmcsd 2> /dev/null || :
/usr/sbin/useradd -c "vlmcsd" -g vlmcsd -s /sbin/nologin -r vlmcsd -M 2> /dev/null || :

%post
%systemd_post vlmcsd.service
%firewalld_reload

%preun
%systemd_preun vlmcsd.service

%postun
%systemd_postun
%firewalld_reload

%clean
rm -rf %{buildroot}

%files
%{_bindir}/vlmcs
%{_bindir}/vlmcsd
/etc/%{name}/vlmcsd.ini
/etc/%{name}/vlmcsd.kmd
%{_mandir}/man1/vlmcs.1.gz
%{_mandir}/man5/vlmcsd.ini.5.gz
%{_mandir}/man7/vlmcsd.7.gz
%{_mandir}/man8/vlmcsd.8.gz
%{_unitdir}/vlmcsd.service
%{_prefix}/lib/firewalld/services/kms.xml

%changelog
* Sat May 02 2020 - svn1113-1
- Add firewalld service.
- Add system build flags.
- Fix building debug RPMs.
- Fix docs build.
