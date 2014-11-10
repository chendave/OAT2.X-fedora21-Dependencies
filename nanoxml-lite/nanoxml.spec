# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free

Name:           nanoxml
Version:        2.2.3
Release:        5%{?dist}
Epoch:          0
Summary:        NanoXML is a small XML parser for Java
License:        zlib License
Group:          Text Processing/Markup/XML
URL:            http://nanoxml.cyberelf.be/
Source0:        http://nanoxml.cyberelf.be/downloads/NanoXML-2.2.3.tar.gz
Source1:        http://repo1.maven.org/maven2/be/cyberelf/nanoxml/nanoxml/2.2.3/nanoxml-2.2.3.pom
Source2:        http://repo1.maven.org/maven2/be/cyberelf/nanoxml/lite/2.2.3/lite-2.2.3.pom
Source3:        java-1.5.0-package-list
Patch0:         %{name}-build.patch
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  java-devel >= 0:1.5.0
Requires:       java >= 0:1.5.0
Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The intent of NanoXML is to be a small parser which is easy to use.
Although many features were added to NanoXML, it is very small.
The full parser with builder fits in a JAR file of about 32K.

%package        lite
Summary:        Lite version of %{name}
Group:          Text Processing/Markup/XML

%description    lite
Lite version of %{name}.

%package        manual
Summary:        Manual for %{name}
Group:          Text Processing/Markup/XML

%description    manual
Documentation for %{name}.

%package        manual-lite
Summary:        Manual for the lite version of %{name}
Group:          Text Processing/Markup/XML

%description    manual-lite
Documentation for the lite version of %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Text Processing/Markup/XML

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n NanoXML-%{version}
%patch0 -b .sav0
cp %{SOURCE3} package-list
find . -name "*.jar" | xargs -r rm -f

%build
sh ./build.sh

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 Output/%{name}-lite.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-lite-%{version}.jar
install -pm 644 Output/%{name}-sax.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-sax-%{version}.jar
install -pm 644 Output/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
#%add_to_maven_depmap be.cyberelf.nanoxml %{name} %{version} JPP %{name}
install -m 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}-lite.pom
#%add_to_maven_depmap be.cyberelf.nanoxml lite %{version} JPP %{name}-lite

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr Documentation/JavaDoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink


%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%post lite

%postun lite

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-sax-%{version}.jar
%{_javadir}/%{name}-sax.jar
#%{_mavendepmapfragdir}/*
%{_datadir}/maven2/poms/*


%files lite
%defattr(-,root,root,-)
%{_javadir}/%{name}-lite-%{version}.jar
%{_javadir}/%{name}-lite.jar
#%{_mavendepmapfragdir}/*
%{_datadir}/maven2/poms/*

%files manual
%defattr(0644,root,root,0755)
%doc Documentation/NanoXML-Java/*

%files manual-lite
%defattr(0644,root,root,0755)
%doc Documentation/NanoXML-Lite/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Wed Mar 18 2009 Ralph Apel <r.apel@r-apel.de> - 0:2.2.3-5.jpp5
- First JPP-5 release

* Thu Jul 20 2006 Ralph Apel <r.apel@r-apel.de> - 0:2.2.3-4jpp
- First JPP-1.7 release
- Drop BR java-javadoc, add package-list as Source instead

* Mon Aug 23 2004 Fernando Nasser <fnasser@redhat.com> - 0:2.2.3-3jpp
- Updated URL
- Pro-forma rebuild with Ant 1.6.2 present

* Sat Jan 10 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.3-2jpp
- Add Epoch.
- Change group to Text Processing/Markup/XML.
- Add unversioned javadoc dir symlinks, mark javadoc as %%doc.
- Install manual as normal %%doc, not into %%{_javadocdir}.
- BuildRequires java-devel (not ant).
- Don't use bundled SAX jar.

* Sat Dec 27 2003 Thomas Leonard <tle@sirius.sued.tremium.de> - 2.2.3-1
- Initial build.
