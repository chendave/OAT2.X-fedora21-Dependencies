Name:		monolog
Version:	2.0
Release:	1fc_1
Epoch:		0
Summary:	API for monitoring and logging
License:	LGPL
URL:		http://monolog.objectweb.org/
Group:		Development/Libraries/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
Source0:	monolog_%{version}_src.tar.gz
## http://forge.objectweb.org/monolog/Monolog_1.9.1_src.zip
## cvs -d:pserver:anonymous@cvs.forge.objectweb.org:/cvsroot/monolog login
##  cvs -z3 -d:pserver:anonymous@cvs.forge.objectweb.org:/cvsroot/monolog export -r MONOLOG_1_9_2 monolog

BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	ant
BuildRequires:	log4j
BuildRequires:	mx4j
BuildRequires:	objectweb-anttask
BuildRequires:  p6spy
BuildRequires:  velocity
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Monolog is an API of monitoring and logging.

%package	javadoc
Summary:	Javadoc for %{name}
Group:		Development/Documentation

%description	javadoc
Javadoc for %{name}.


%prep
rm -rf $RPM_BUILD_DIR/%{name}
                                                                                
%setup -q -n %{name}
find . -name "*.jar" -exec rm -f {} \;

# also build ow_util_io.jar (required by medor)
mv shared.old/src/io src/org/objectweb/util
mv shared.old/archive/ow_util_io.xml archive

%build
export CLASSPATH=$(build-classpath log4j mx4j/mx4j objectweb-anttask p6spy velocity)
pushd externals
for jar in $(echo $CLASSPATH | sed 's/:/ /g'); do
ln -sf ${jar} .
done
popd
ant jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

rm -f output/dist/lib/ow_util_all*.jar
rm -f output/dist/lib/ow_util_ant*.jar
for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
$RPM_BUILD_ROOT%{_javadir}/%{name}/`basename ${jar} .jar`-%{version}.jar
done

(cd $RPM_BUILD_ROOT%{_javadir}//%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%clean

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}

%changelog
* Wed Jul 27 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0-1jpp_1rh
- Upgrade to 2.0

* Wed Jul 20 2005 Fernando Nasser <fnasser@redhat.com> 0:1.9.2-1jpp_2rh
  From Gary Benson <gbenson@redhat.com>
- Also build ow_util_io.jar, as required by medor.

* Fri Jun 10 2005 Fernando Nasser <fnasser@redhat.com> 0:1.9.2-1jpp_1rh
- Merge with upstream for upgrade

* Fri Jun 10 2005 Fernando Nasser <fnasser@redhat.com> 0:1.9.2-1jpp
- Upgrade to 1.9.2

* Fri Jun 03 2005 Fernando Nasser <fnasser@redhat.com> 0:1.9.1-1jpp_1rh
- Merge with upstream for upgrade

* Fri Jun 03 2005 Fernando Nasser <fnasser@redhat.com> 0:1.9.1-1jpp
- Upgrade to 1.9.1

* Fri Nov 12 2004 Fernando Nasser <fnasser@redhat.com> 0:1.8.6-1jpp_1rh
- Merge with upstream for upgrade

* Fri Nov 12 2004 Fernando Nasser <fnasser@redhat.com> 0:1.8.6-1jpp
- Upgrade to 1.8.6
- No more dependencies on fractal; those were moved to monolog-fractal

* Fri Nov 12 2004 Fernando Nasser <fnasser@redhat.com> 0:1.8.3-1jpp_1rh
- Merge with upstream for upgrade

* Fri Nov 12 2004 Ralph Apel <r.apel at r-apel.de> 0:1.8.3-1jpp
- Upgrade to 1.8.3 from CVS for jonas and some other objectweb packages
- Drop fractal/fractal-util from CLASSPATH: doesn't exist any more
- Drop monolog/ow_monolog from CLASSPATH: not required (but owanttask is!)
- Drop monolog as a BuildRequires
- Drop fractal/fractal-adl from CLASSPATH: not required
- Include source of org.objectweb.fractal.api.control.AttributeController
- Drop fractal as a BuildRequires

- Drop xalan-j2 from CLASSPATH and as a BuildRequires: not used
- There are no non-optional runtime Requires
- There are no external dependencies left, because ADLConverter includes
  sources which are compiled at build time

* Tue Sep 21 2004 Ralph Apel <r.apel at r-apel.de> 0:1.8-2jpp
- Decouple ow_util_ant_tasks.jar, don't include it in package
- Require separate owanttask 1.2
- Still require monolog
- Automatically convert ADL description to ADL 2 for fractal 2.2 during prep

* Mon Aug 23 2004 Fernando Nasser <fnasser@redhat.com> 0:1.8-1jpp
- Upgrade to 1.8
- Rebuilt with Ant 1.6.2

* Thu Jan 29 2004 David Walluck <david@anti-microsoft.org> 0:1.7-2jpp
- don't own %%{_javadir}

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.7-1jpp
- release
