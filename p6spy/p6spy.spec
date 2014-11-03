%define section  free
%define jbossdir %{_localstatedir}/jboss

Summary:        Database statement interceptor for Java
Name:           p6spy
Version:        1.3
Release:        2_1
Epoch:          0
Group:          Database
License:        P6Spy Software License
URL:            http://p6spy.sourceforge.net/
BuildArch:      noarch
Source0:        p6spy-1.3.tar.gz
#Patch0:         %{name}-jboss3.patch
Patch1:         %{name}-javadoc-crosslink.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  regexp
BuildRequires:  gnu.regexp
BuildRequires:  log4j
BuildRequires:  jdbc-stdext
#BuildRequires:  jboss
BuildRequires:  log4j-javadoc
BuildRequires:  java-javadoc
Requires:       regexp
Requires:       gnu.regexp
Requires:       log4j
Requires:       jdbc-stdext

%description
P6Spy is an open source framework for applications that intercept and
optionally modify database statements.

%package        javadoc
Group:          Development/Documentation
Summary:        Javadoc for %{name}

%description    javadoc
%{summary}.

%package        manual
Summary:        Manual for %{name}
Group:          Database

%description    manual
%{summary}.


%prep
%setup -q
#%patch0 -p0
%patch1 -p0
rm -rf javadocs documentation/Templates documentation/_notes com/p6spy/management/jboss
mkdir lib


%build
CLASSPATH=%(build-classpath regexp gnu.regexp log4j jdbc-stdext)
export CLASSPATH
#export CLASSPATH=$CLASSPATH:\
#%{jbossdir}/lib/jboss-common.jar:\
#%{jbossdir}/lib/jboss-system.jar:\
#%{jbossdir}/lib/jboss-jmx.jar
# Tests would need a DB to test against :(
ant \
  -Dbuild.sysclasspath=last \
  -Dlog4j.javadoc=%{_javadocdir}/log4j \
  -Dj2se.javadoc=%{_javadocdir}/java \
  clean release


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/p6spy.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# webapp
# TODO: dist/p6spy.war to tomcat/jboss+jetty webapps dir
# TODO: make %{_javadir}/p6spy.jar available in tomcat/jboss+jetty classpath


%clean
rm -rf $RPM_BUILD_ROOT


%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}


%files
%defattr(0644,root,root,0755)
%doc license.txt spy.properties
%{_javadir}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc documentation/*


%changelog
* Fri Oct 15 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp_1rh
- First Red Hat build

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com>  - 0:1.3-2jpp
- Rebuild with Ant 1.6.2

* Sat Jan 10 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3-1jpp
- Update to 1.3.
- New style versionless javadoc symlinking.
- Crosslink with local J2SE javadocs.

* Sun Jul 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2-1jpp
- Update to 1.2.
- JPackage 1.5'ified.

* Sat Jan 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.0.4-0.beta.1jpp
- Update to 1.0.4 beta.

* Thu Oct 10 2002 Ville Skyttä <ville.skytta at iki.fi> 1.0-0.beta.2jpp
- Author released a new source jar with (package only) bugs fixed, using it.
  The software version was not bumped though, brr.

* Mon Oct  7 2002 Ville Skyttä <ville.skytta at iki.fi> 1.0-0.beta.1jpp
- First JPackage release.
