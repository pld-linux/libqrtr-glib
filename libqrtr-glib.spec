#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Library to use and monitor the QRTR bus
Summary(pl.UTF-8):	Biblioteka do korzystania i monitorowania szyny QRTR
Name:		libqrtr-glib
Version:	1.0.0
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	https://www.freedesktop.org/software/libqmi/%{name}-%{version}.tar.xz
# Source0-md5:	c831b1478d430e2b587e84ae13ffea02
URL:		https://www.freedesktop.org/software/libqmi/libqrtr-glib/latest/
BuildRequires:	glib2-devel >= 1:2.48
BuildRequires:	gobject-introspection-devel >= 0.9.6
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	linux-libc-headers >= 7:4.7
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.48
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
Requires:	glib2-devel >= 1:2.48
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

%build
%configure \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libqrtr-glib.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
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
