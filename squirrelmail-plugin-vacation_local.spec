%define		_plugin	vacation_local
%define		mversion	1.4
Summary:	Vacation plugin for Squirrelmail
Summary(pl):	Wtyczka vacation dla Squirrelmail
Name:		squirrelmail-plugin-%{_plugin}
Version:	2.0
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.squirrelmail.org/plugins/%{_plugin}-%{version}-%{mversion}.tar.gz
# Source0-md5:	c050a2e9c066b7aa1d008edd74796c93
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-binary-fix.patch
URL:		http://www.squirrelmail.org/
Requires:	php-ftp
Requires:	squirrelmail >= 1.4.6-1
Obsoletes:	squirrelmail-plugin-vacation
Obsoletes:	squirrelmail-vacation
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_datadir}/squirrelmail/plugins/%{_plugin}
%define		_sysconfdir	/etc/webapps/squirrelmail

%description
This plugin allows users to create an auto-respond message to all
incoming email while they're away.

Warning: This package contains file with suid bit set!

%description -l pl
Ta wtyczka umo¿liwia u¿ytkownikom stworzenie i w³±czenie automatycznej
odpowiedzi na wszystkie przychodz±ce maile.

Uwaga: ten pakiet zawiera plik z ustawionym bitem suid!

%prep
%setup -q -n %{_plugin}
%patch0 -p1
%patch1 -p1

%build
%{__make} -C vacation_binary \
	CFLAGS="%{rpmcflags}" \
	LFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_plugindir} $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_sbindir}

install vacation_binary/squirrelmail_vacation_proxy $RPM_BUILD_ROOT%{_sbindir}
install *.php $RPM_BUILD_ROOT%{_plugindir}
mv config.php.sample $RPM_BUILD_ROOT%{_sysconfdir}/vacation_local_config.php
ln -s %{_sysconfdir}/vacation_local_config.php $RPM_BUILD_ROOT%{_plugindir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL README
%attr(4755,root,root) %{_sbindir}/squirrelmail_vacation_proxy
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vacation_local_config.php
%dir %{_plugindir}
%{_plugindir}/*.php
