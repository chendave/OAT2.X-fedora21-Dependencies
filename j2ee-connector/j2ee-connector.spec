%define name		j2ee-connector
%define cvs_name	j2ee_connector
%define version		1.5
%define cvs_version	1_5
%define release		3_2fc
%define section		non-free

Summary:	J2EE(tm) Connector Architecture
Url:		http://java.sun.com/products/j2ee

Source0:	%{cvs_name}-%{cvs_version}-fr-spec-classes.zip

# If you do not want -javadoc built, give rpmbuild option '--without javadoc'
%define with_javadoc %{!?_without_javadoc:1}%{?_without_javadoc:0}

%if %{with_javadoc}
Source1:	%{cvs_name}-%{cvs_version}-fr-spec-docs.zip
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
License:	Sun Binary Code License
Group:		Development/Libraries/Java
BuildArch:	noarch
BuildRequires:	jpackage-utils >= 0:1.5
Requires:	jpackage-utils >= 0:1.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The J2EE Connector architecture provides a Java solution to the problem
of connectivity between the many application servers and EISs already in
existence.  By using the J2EE Connector architecture, EIS vendors no
longer need to customize their product for each application server.

Application server vendors who conform to the J2EE Connector
architecture do not need to add custom code whenever they want to add
connectivity to a new EIS.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -c

%if %{with_javadoc}
%setup -q -D -T -a 1
rm docs/connector-api-docs.jar
%endif

# fix files perms
chmod -R go=u-w *

%build
%jar xf connector-api.jar
%jar cf %{name}-%{version}.jar javax

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755                        $RPM_BUILD_ROOT%{_javadir}
install -p -m 0644 %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s              %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -d -m 0755                   $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m 0644 connector_1_5.xsd $RPM_BUILD_ROOT%{_datadir}/%{name}

# javadoc
%if %{with_javadoc}
install -d -m 0755       $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/*             $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f                    %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.xsd

%if %{with_javadoc}
%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
%endif

%changelog
* Mon Dec 06 2004 Fernando Nasser <fnasser@redhat.com> 0:1.5-3jpp_2rh
- Rebuild

* Mon Oct 18 2004 Fernando Nasser <fnasser@redhat.com> 0:1.5-3jpp_1rh
- First Red Hat build

* Wed Jan 14 2004 Ralph Apel <r.apel@r-apel.de> 0:1.5-3jpp
- upgrade to FR

* Tue Oct 07 2003 Leonid Dubinsky <dub@podval.org> 0:1.5-2jpp
- conditionalize javadoc subpackage
- mark javadoc as %%doc
- own versionless javadoc symlink (%%ghost)
- add dependence on jpackage-utils

* Sun May 11 2003 David Walluck <david@anti-microsoft.org> 0:1.5-1jpp
- 1.5 PFD2
- update for JPackage 1.5

* Wed Mar 26 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.0-2jpp
- For jpackage-utils 1.5

* Tue Jan 22 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.0-1jpp
- Initial release
