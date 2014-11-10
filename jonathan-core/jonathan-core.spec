%define section	free

Name:		jonathan-core
Version:	4.1
Release:	1_1fc
Epoch:		0
Summary:	Distributed Object Platform (DOP) written entirely in Java
License:	LGPL
URL:		http://jonathan.objectweb.org/
Group:		Development/Libraries/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
Source0:	jonathancore-%{version}-src.tar.gz
# cvs -d:pserver:anonymous@cvs.forge.objectweb.org:/cvsroot/jonathan login
# cvs -z3 -d:pserver:anonymous@cvs.forge.objectweb.org:/cvsroot/jonathan export -r JONATHAN_CORE_4_1 jonathancore

Requires:	monolog
Requires:	nanoxml-lite
Requires:	oldkilim
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	objectweb-anttask
BuildRequires:	oldkilim
BuildRequires:	monolog
BuildRequires:	nanoxml-lite
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Jonathan is a Distributed Object Platform (DOP) written entirely in
Java. Jonathan was developed originally at the research labs of France
Télécom in the context of the European project ReTINA, whose aim was to
define an architecture for telecommunications distributed environments.
Telecommunications applications such as multimedia services have
stringent requirements in terms of scalability, adaptability and
realtime. Jonathan's response to this is through its "openness" in the
sense that contrary to standard DOPs (and in particular, most CORBA
ORBs), the abstractions that make up its internal machinery are
accessible by an application programmer and may be specialized to meet
specific requirements.

Jonathan is organised around a very small kernel (namely Kilim) that
essentially lets the infrastructure components communicate. Currently,
these components consist of a number of independently developed
protocols, marshallers, stub factories, etc.

Different personalities can be built using these components. A
personality is a set of normalized Application Programming Interfaces:
Java RMI is a personality, CORBA is another, COM still another...
Jonathan provides two personnalities:

    * David is a CORBA ORB implementation. David lacks a number of CORBA
      features (POA, interface repository, Dynamic Any,...) and provides only
      a naive naming service implementation. However, our ambition is to fill
      these gaps and to provide a reference CORBA implementation.

    * Jeremie provides an RMI-like programming style.

%package	javadoc
Summary:	Javadoc for %{name}
Group:		Development/Documentation

%description	javadoc
Javadoc for %{name}.

%prep
%setup -q -n jonathancore
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=

pushd config
    ln -sf $(build-classpath oldkilim-tools) kilim-tools.jar
    ln -sf $(build-classpath objectweb-anttask) ow_util_ant_tasks.jar
    ln -sf $(build-classpath nanoxml-lite) nanoxml-lite-2.2.1.jar
popd
pushd externals
    ln -sf $(build-classpath oldkilim) kilim.jar
    ln -sf $(build-classpath monolog/ow_monolog) ow_monolog.jar
popd

#ant jonathan javadoc
ant jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 output/dist/lib/jonathan-core.jar \
                  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/ && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/* \
                  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}

%changelog
* Fri Mar 04 2005 Fernando Nasser <fnasser@redhat.com> 0:4.1-1jpp
- Upgrade to 4.1
- Remove patch (incorporated upstream)

* Fri Dec 17 2004 Fernando Nasser <fnasser@redhat.com> 0:4.0-2jpp_1rh
- Merge with upstream for fix

* Fri Dec 17 2004 Fernando Nasser <fnasser@redhat.com> 0:4.0-2jpp
- Add patch to fix resource name so it can work with oldkilim 1.1.3

* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com> 0:4.0-0.cvs.1jpp_1rh
- First Red Hat build

* Tue Sep 21 2004 Ralph Apel <r.apel at r-apel.de> 0:4.0-0.cvs.1jpp
- First release of this code base
