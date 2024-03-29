#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# check target
#
Summary:	The Typesafe Signal Framework for C++
Summary(pl.UTF-8):	Środowisko sygnałów z kontrolą typów dla C++
Name:		libsigc++3
Version:	3.6.0
Release:	1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libsigc++/3.6/libsigc++-%{version}.tar.xz
# Source0-md5:	b7205d5465ac15fbc0c781d39b4011be
URL:		https://libsigcplusplus.github.io/libsigcplusplus/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
%{?with_apidocs:BuildRequires:	docbook-style-xsl-nons}
%{?with_apidocs:BuildRequires:	doxygen >= 1:1.8.9}
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtool >= 2:2.0
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	m4
BuildRequires:	mm-common >= 0.9.12
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	libsigc++-examples < 1
Conflicts:	libsigc++ < 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library implements a full callback system for use in widget
libraries, abstract interfaces, and general programming. Originally
part of the Gtk-- widget set, libsigc++ is now a seperate library to
provide for more general use. It is the most complete library of its
kind with the ablity to connect an abstract callback to a class
method, function, or function object. It contains adaptor classes for
connection of dissimilar callbacks and has an ease of use unmatched by
other C++ callback libraries.

%description -l pl.UTF-8
Ta biblioteka jest implementacją pełnego systemu callbacków do
używania w bibliotekach widgetów, interfejsach abstrakcyjnych i
ogólnym programowaniu. Oryginalnie była to część zestawu widgetów
Gtk--, ale jest teraz oddzielną biblioteką ogólniejszego
przeznaczenia. Jest to kompletna biblioteka tego typu z możliwością
łączenia abstrakcyjnych callbacków z metodami klas, funkcjami lub
obiektami funkcji. Zawiera klasy adapterów do łączenia różnych
callbacków.

%package devel
Summary:	Development tools for the Typesafe Signal Framework for C++
Summary(pl.UTF-8):	Narzędzia programistyczne do środowiska libsig++
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel >= 6:7
Requires:	m4

%description devel
Development tools for the Typesafe Signal Framework for C++.

%description devel -l pl.UTF-8
Narzędzia programistyczne do środowiska libsigc++ - sygnałów z
kontrolą typów.

%package static
Summary:	Static Typesafe Signal Framework for C++ libraries
Summary(pl.UTF-8):	Statyczna biblioteka libsigc++
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static Typesafe Signal Framework for C++ libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libsigc++ - środowiska sygnałów z kontrolą typów.

%package doc
Summary:	Reference documentation for libsigc++
Summary(pl.UTF-8):	Szczegółowa dokumentacja dla libsigc++
Group:		Documentation
BuildArch:	noarch

%description doc
Reference documentation for libsigc++.

%description doc -l pl.UTF-8
Szczegółowa dokumentacja dla libsigc++.

%prep
%setup -q -n libsigc++-%{version}

%build
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{__enable_disable apidocs documentation}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsigc-3.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libsigc-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigc-3.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsigc-3.0.so
%{_includedir}/sigc++-3.0
%{_libdir}/sigc++-3.0
%{_pkgconfigdir}/sigc++-3.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsigc-3.0.a
%endif

%if %{with apidocs}
%files doc
%defattr(644,root,root,755)
%{_datadir}/devhelp/books/libsigc++-3.0
%{_docdir}/libsigc++-3.0
%endif
