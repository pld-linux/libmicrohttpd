#
# Conditional build
%bcond_with	tests	# perform "make check"
#
Summary:	Embeded HTTP server library
Summary(pl.UTF-8):	Biblioteka wbudowanego serwera HTTP
Name:		libmicrohttpd
Version:	1.0.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
# Source0-md5:	b41c83799a478ea9c774e50ed22446bc
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libmicrohttpd/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.20.2
BuildRequires:	gnutls-devel >= 2.8.6
BuildRequires:	libgcrypt-devel >= 1.2.4
BuildRequires:	libmagic-devel
BuildRequires:	libtool >= 2:2.4.0
BuildRequires:	pkgconfig
BuildRequires:	texinfo
%if %{with tests}
BuildRequires:	curl-devel >= 7.16.4
%endif
Requires:	gnutls >= 2.8.6
Requires:	libgcrypt >= 1.2.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.

%description -l pl.UTF-8
GNU libmicrohttpd jest małą biblioteką C, w założeniu umożliwiającą
uruchomienie serwera HTTP jako części innej aplikacji.

%package devel
Summary:	Header files to develop libmicrohttpd applications
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania aplikacji używających libmicrohttpd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gnutls-devel >= 2.8.6
Requires:	libgcrypt-devel >= 1.2.4
Requires:	openssl-devel

%description devel
Header files to develop libmicrohttpd applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania aplikacji używających libmicrohttpd.

%package static
Summary:	Static libmicrohttpd libraries
Summary(pl.UTF-8):	Biblioteka statyczna libmicrohttpd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmicrohttpd libraries.

%description static -l pl.UTF-8
Biblioteka statyczna libmicrohttpd.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with tests}
	--enable-curl \
	--enable-client-side \
%endif
	--enable-https \
	--disable-messages

%{__make}
%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmicro*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmicrohttpd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmicrohttpd.so.12

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmicrohttpd.so
%{_includedir}/microhttpd.h
%{_infodir}/libmicrohttpd.info*
%{_infodir}/libmicrohttpd-tutorial.info*
%{_infodir}/libmicrohttpd_performance_data.png
%{_mandir}/man3/libmicrohttpd.3*
%{_pkgconfigdir}/libmicrohttpd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmicrohttpd.a
