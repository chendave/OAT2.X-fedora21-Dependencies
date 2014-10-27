%define version		1.0.1
%define release		1_1fc
%define	section		free
%define	jarname		carol_irmi


Name:		carol-irmi
Summary:	IRMI: Intercepting RMI implementation for the Java platform
Url:		http://carol.objectweb.org/
Version:	%{version}
Release:	%{release}
Epoch:		0
License:	LGPL
Group:		Development/Libraries/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
BuildArch:	noarch
Source0:	carol-irmi-%{version}-src.tgz

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:	ant >= 0:1.6
BuildRequires:  apache-commons-collections >= 3.1
Requires:  apache-commons-collections >= 3.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The irmi package is a JDK agnostic RMI implementation supporting
pluggable interceptors and local call optimization. It uses standard
JRMP stubs and uses the javax.rmi.CORBA.PortableRemoteObjectDelegate
interface to plug into any JDK. This implementation may be enabled by
setting the system property named javax.rmi.CORBA.PortableRemoteObjectClass
to the value "org.objectweb.carol.irmi.PRO".


%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n irmi
chmod -R go=u-w *

find . -name "*.jar" \
       -exec rm -f {} \; 

%build
build-jar-repository externals commons-collections

ant test jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
                                                                                
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/irmi.jar \
        $RPM_BUILD_ROOT%{_javadir}/ow_%{jarname}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
ln -sf ow_%{jarname}-%{version}.jar ow_%{jarname}.jar
popd

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_javadir}/ow_%{jarname}.jar
%{_javadir}/ow_%{jarname}-%{version}.jar


%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%changelog
* Wed Sep 28 2005 Fernando Nasser <fnasser at redhat.com> 0:1.0.1-1jpp_1rh
- Upgrade to 1.0.1

* Mon Jun 06 2005 Fernando Nasser <fnasser at redhat.com> 0:1.0-1jpp_3rh
- Rebuild with new jar file names

* Mon Jun 06 2005 Fernando Nasser <fnasser at redhat.com> 0:1.0-1jpp_2rh
- Rebuild

* Sun Jun 05 2005 Fernando Nasser <fnasser at redhat.com> 0:1.0-1jpp_1rh
- First release

