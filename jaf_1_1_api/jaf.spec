%define		javalibdir		/usr/share/java

Summary: JavaBeans Activation Framework
Name: jaf
Version: 1.0.1
Release: 3
License: LGPL
Group: Development/Libraries
Url: http://java.sun.com/products/javabeans/glasgow/jaf.html
BuildArch: noarch
Source0: jaf1_0_1.zip
Source1: %{name}.profile
BuildRequires: java-1.7.0-openjdk
BuildRoot: %{_tmppath}/jaf-root

%description

With the JavaBeansTM Activation Framework standard extension,
developers who use JavaTM technology can take advantage of standard
services to determine the type of an arbitrary piece of data,
encapsulate access to it, discover the operations available on it, and
to instantiate the appropriate bean to perform said operation(s). For
example, if a browser obtained a JPEG image, this framework would
enable the browser to identify that stream of data as an JPEG image,
and from that type, the browser could locate and instantiate an object
that could manipulate, or view that image.

%package docs
Group: Documentation
Summary: Documentation %{name}

%description docs
Documentation %{name}, the JavaBeans Activation Framework.

With the JavaBeansTM Activation Framework standard extension,
developers who use JavaTM technology can take advantage of standard
services to determine the type of an arbitrary piece of data,
encapsulate access to it, discover the operations available on it, and
to instantiate the appropriate bean to perform said operation(s). For
example, if a browser obtained a JPEG image, this framework would
enable the browser to identify that stream of data as an JPEG image,
and from that type, the browser could locate and instantiate an object
that could manipulate, or view that image.

%package demo
Group: Documentation
Summary: Example Code for %{name}

%description demo
Example Code for %{name}, the JavaBeans Activation Framework.

With the JavaBeansTM Activation Framework standard extension,
developers who use JavaTM technology can take advantage of standard
services to determine the type of an arbitrary piece of data,
encapsulate access to it, discover the operations available on it, and
to instantiate the appropriate bean to perform said operation(s). For
example, if a browser obtained a JPEG image, this framework would
enable the browser to identify that stream of data as an JPEG image,
and from that type, the browser could locate and instantiate an object
that could manipulate, or view that image.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{javalibdir}
install -d $RPM_BUILD_ROOT/etc/profile.d

install activation.jar $RPM_BUILD_ROOT/%{javalibdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/profile.d/%{name}.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt RELNOTES.txt
%attr(644,root,root) %{javalibdir}/*.jar
%attr(755,root,root) /etc/profile.d/%{name}.sh

%files docs
%defattr(644,root,root,755)
%doc docs/*

%files demo
%defattr(644,root,root,755)
%doc demo

%changelog
* Mon May 16 2001 Bob Tanner <tanner@real-time.com>
- Change from mkdir -p to install -d (better platform support)
- Used macros for build root, in case people wish to change it
- Made permission settings in 1 location. I personally like them in the %file
  section rather then specifing them with install --mode.
- Cleaned up setup, rpm is smart about unpacking files
- Added Build dependencies, so check for a jdk is not necessary
- Formatting clean up. I use emacs and the shell-script major mode with rpm
  minor mode to keep a "standard" format.

* Wed Nov 15 2000 Ben Reed <ben@opennms.org>
- initial release
