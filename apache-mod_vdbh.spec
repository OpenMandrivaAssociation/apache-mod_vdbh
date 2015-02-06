#Module-Specific definitions
%define mod_name mod_vdbh
%define mod_conf 21_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A Virtual Database Hosting DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	1.0.3
Release:	23
Group:		System/Servers
License:	GPL
URL:		http://www.synthemesc.com/mod_vdbh/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	mysql-devel
BuildRequires:	file
Epoch:		1

%description
mod_vdbh is an Apache Web Server module allowing mass virtual
hosting without the need for file based configuration. The virtual
host paths are translated from a MySQL database at request time,
thus the configuration can be changed without having to restart
Apache Web Server.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -DHAVE_STDDEF_H -I%{_includedir}/mysql -L%{_libdir} -Wl,-lmysqlclient -c mod_vdbh.c
    
%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-22mdv2012.0
+ Revision: 773234
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-21
+ Revision: 678433
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-20
+ Revision: 645771
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-19mdv2011.0
+ Revision: 627209
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-18mdv2011.0
+ Revision: 626503
- rebuilt against mysql-5.5.8 libs

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-16mdv2011.0
+ Revision: 588079
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1:1.0.3-15mdv2010.1
+ Revision: 537597
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-14mdv2010.1
+ Revision: 516217
- rebuilt for apache-2.2.15

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-13mdv2010.1
+ Revision: 507475
- rebuild

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-12mdv2010.0
+ Revision: 406668
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-11mdv2009.1
+ Revision: 326508
- rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-10mdv2009.1
+ Revision: 311294
- rebuilt against mysql-5.1.30 libs

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-9mdv2009.0
+ Revision: 235119
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-8mdv2009.0
+ Revision: 215663
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-7mdv2008.1
+ Revision: 181958
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-6mdv2008.0
+ Revision: 82692
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2007.1
+ Revision: 140769
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-4mdv2007.0
+ Revision: 79539
- Import apache-mod_vdbh

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-3mdv2007.0
- rebuild

* Sun Dec 18 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-2mdk
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-1mdk
- rebuilt against MySQL-5.0.15
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.0.3-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.0.3-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.0.3-4mdk
- use the %macro

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.0.3-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.0.3-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.0.3-1mdk
- rebuilt for apache 2.0.53

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_1.0.3-2mdk
- rebuilt against MySQL-4.1.x system libs
- nuke redundant deps

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_1.0.3-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_1.0.3-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.0.3-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_1.0.3-1mdk
- built for apache 2.0.49

