Name:           ow2-jta-1.1-spec
Version:        1.0.8
Release:        1%{?dist}
Summary:        This is the  ow2-jta-1.1-spec's spec file.
License:        GPLv2+
URL:            http://www.fedoraproject.org
Source0:    %{name}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires: objectweb-asm
BuildRequires: java-1.7.0-openjdk

%description
Very short description since we have nothing to say.
%prep
%setup -q

%build
javac `find . -name *.java`
jar cvf %{name}-%{version}.jar `find . -name *.class` 

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_javadir}
install -p -m 644 %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_javadir}/%{name}-%{version}.jar

%changelog
 * Tue Mar 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-1
- This is first version
