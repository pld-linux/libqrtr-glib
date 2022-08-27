#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Library to use and monitor the QRTR bus
Summary(pl.UTF-8):	Biblioteka do korzystania i monitorowania szyny QRTR
Name:		libqrtr-glib
Version:	1.2.2
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib/-/tags
Source0:	https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ff475b280ce8cce31e4d5e41fd6d0c43
URL:		https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib
BuildRequires:	glib2-devel >= 1:2.56
BuildRequires:	gobject-introspection-devel >= 0.9.6
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	linux-libc-headers >= 7:4.7
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	glib2 >= 1:2.56
Conflicts:	libqmi < 1.28.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libqrtr-glib is a glib-based library to use and manage the QRTR
(Qualcomm IPC Router) bus.

%description -l pl.UTF-8
libqrtr-glib to oparta na glibie biblioteka do korzystania i
zarządzania szyną QRTR (Qualcomm IPC Router).

%package devel
Summary:	Header files for libqrtr-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libqrtr-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.56
Conflicts:	libqmi-devel < 1.28.0

%description devel
Header files for libqrtr-glib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libqrtr-glib.

%package static
Summary:	Static libqrtr-glib library
Summary(pl.UTF-8):	Statyczna biblioteka libqrtr-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libqrtr-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka libqrtr-glib.

%package apidocs
Summary:	API documentation for libqrtr-glib library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libqrtr-glib
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libqrtr-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libqrtr-glib.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e '/^libqrtr_glib =/ s/shared_library/library/' src/libqrtr-glib/meson.build
%endif

%build
%meson build \
	%{!?with_apidocs:-Dgtk_doc=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libqrtr-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqrtr-glib.so.0
%{_libdir}/girepository-1.0/Qrtr-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqrtr-glib.so
%{_datadir}/gir-1.0/Qrtr-1.0.gir
%{_includedir}/libqrtr-glib
%{_pkgconfigdir}/qrtr-glib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqrtr-glib.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libqrtr-glib
%endif
