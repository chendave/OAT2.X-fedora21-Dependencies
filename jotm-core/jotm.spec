%define name		jotm
%define version		2.0.10
%define release		1_2fc
%define	section		free

Name:		%{name}
Summary:	JOTM : A Java Open Transaction Manager
Url:		http://jotm.objectweb.org/
Version:	%{version}
Release:	%{release}
Epoch:		0
License:	BSD-style
Group:		Development/Libraries/Java
BuildArch:	noarch
Source0:	jotm-%{version}-src.tgz

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:	ant >= 0:1.6
BuildRequires:	carol >= 2.0
BuildRequires:	howl-logger >= 0:0.1.8
BuildRequires:	j2ee-connector
BuildRequires:	apache-commons-cli
BuildRequires:	apache-commons-logging
BuildRequires:	jonathan-core >= 4.1
BuildRequires:	jonathan-jeremie >= 4.2
BuildRequires:	jta
BuildRequires:	jts
BuildRequires:	log4j
BuildRequires:	oldkilim

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Today the JOTM team delivers to you a Java Open Source 
implementation of the JTA APIs. This implementation is 
fully functional and mature since it has been used for 
several years in the JOnAS application server project.
Tomorrow we aim at delivering adaptable software that 
can be used in a wide range of use cases involving 
transaction management. In particular we are currently 
looking at covering transaction models such as flat, 
CNT, ONT, BTP and transaction standards including JTA, 
JTS, OTS.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Documentation

%description javadoc
%{summary}.

%package demo
Summary:	Examples for %{name}
Group:		Development/Documentation

%description demo
%{summary}.

%package manual
Summary:	Documents for %{name}
Group:		Development/Documentation

%description manual
%{summary}.

%prep
%setup -q -n %{name}
chmod -R go=u-w *

#find . -name "*.jar" -exec rm -f {} \;
find . -name "*.jar" \
       -exec rm -f {} \;

%build
pushd externals
ln -sf $(build-classpath carol/ow_carol) carol.jar
ln -sf $(build-classpath howl-logger) howl.jar
ln -sf $(build-classpath commons-cli) commons-cli.jar
ln -sf $(build-classpath commons-logging) commons-logging.jar
ln -sf $(build-classpath j2ee-connector) connector-1_5.jar
ln -sf $(build-classpath jonathan-core) jonathan.jar
ln -sf $(build-classpath jonathan-jeremie) jeremie.jar
ln -sf $(build-classpath jta) jta-spec1_0_1.jar
ln -sf $(build-classpath jts) jts1_0.jar
ln -sf $(build-classpath oldkilim) kilim.jar
ln -sf $(build-classpath log4j) log4j.jar
popd
ant

%install

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 output/dist/lib/%{name}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-%{version}.jar
install -m 644 output/dist/lib/%{name}_iiop_stubs.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}/iiop-stubs-%{version}.jar
install -m 644 output/dist/lib/%{name}_jrmp_stubs.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}/jrmp-stubs-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# examples and configuration
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples
cp -pr output/dist/examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/conf
cp -pr output/dist/conf/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/conf

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr output/dist/doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc output/dist/LICENSE.txt
%{_javadir}/%{name}
%{_datadir}/%{name}-%{version}/conf

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root)
%{_datadir}/%{name}-%{version}/examples

%files manual
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

%changelog
* Mon Jun 06 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.10-1jpp_2rh
- Use howl-logger package

* Sat Jun 04 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.10-1jpp_1rh
- Merge for upgrade

* Sat Jun 04 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.10-1jpp
- Upgrade to 2.0.10

* Thu Apr 28 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.9-1jpp_1rh
- Upgrade to 2.0.9
- Remove patch already incorporated in new release

* Tue Apr 19 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.8-1jpp_2rh
- Add patch for compatibility with Carol 2.0

* Mon Mar 28 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.8-1jpp_1rh
- Upgrade to 2.0.8

* Fri Mar 04 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.5-1jpp_2rh
- Rebuild

* Fri Mar 04 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.5-1jpp_1rh
- Merge with upstream for upgrade

* Mon Mar 04 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.5-1jpp
- Upgrade to 2.0.5

* Mon Feb 28 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.3-1jpp_1rh
- First Red Hat build

* Mon Feb 28 2005 Fernando Nasser <fnasser@redhat.com> 0:2.0.3-1jpp
- Upgrade to 2.0.3
- Remove patch -- fix incorporated upstream
- Add dependency on 'howl'
- Change dependency on jonathan to dependencies on jonathan-core and
  jonathan-jeremie
- Fix link to carol jar in externals
- Configuration directory changed to conf from config

* Mon Oct 04 2004 Ralph Apel <r.apel at r-apel.de> 0:1.5.3-1jpp
- First release

