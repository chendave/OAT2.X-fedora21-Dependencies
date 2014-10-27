%define section	free

Name:		oldkilim
Version:	1.1.3
Release:	2_1fc
Epoch:		0
Summary:	A generic configuration framework for Java
License:	BSD
URL:		http://kilim.objectweb.org/
Group:		Development/Libraries/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
Source0:	http://download.us.forge.objectweb.org/kilim/Kilim_1_1_3-src.tar.gz
Requires:	nanoxml-lite
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	nanoxml-lite
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Kilim is a generic configuration framework for Java, which can be used
easily with existing applications, frameworks, and systems. It was
originally built into Jonathan in order to allow fine configuration of
its various frameworks (protocols, resource management policies, etc.)
without requiring specific code, and has since grown independently of
Jonathan.

%package	javadoc
Summary:	Javadoc for %{name}
Group:		Development/Documentation

%description	javadoc
Javadoc for %{name}.

%prep
%setup -q -n kilim
find . -name "*.jar" -exec rm -f {} \;
find . -type d -name "CVS" | xargs rm -rf

%build
export CLASSPATH=$(build-classpath nanoxml-lite)
pushd externals
for jar in $(echo $CLASSPATH | sed 's/:/ /g'); do
ln -sf ${jar} .
done
popd
ant distrib javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 distrib/kilim.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 distrib/kilim-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tools-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/apis/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
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
%{_javadir}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
#%ghost %dir %{_javadocdir}/%{name}-%{version}

%changelog
* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.3-2jpp_1rh
- First Red Hat build

* Tue Aug 24 2004 Fernando Nasser <fnasser@redhat.com> 0:1.1.3-2jpp
- Rebuild with Ant 1.6.2

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.1.3-1jpp
- release
