#
# Conditional build
%bcond_with	tests	# perform "make check"
#
Summary:	Embeded HTTP server library
Summary(pl.UTF-8):	Biblioteka wbudowanego serwera HTTP
Name:		libmicrohttpd
Version:	0.9.33
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
# Source0-md5:	013b10f9de1cda5448b29c81305354a3
Patch0:		%{name}-info.patch
Patch1:		%{name}-link.patch
URL:		http://www.gnu.org/software/libmicrohttpd/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	gnutls-devel >= 2.8.6
BuildRequires:	libgcrypt-devel >= 1.2.4
BuildRequires:	libmagic-devel
BuildRequires:	libtool
# for microspdy
BuildRequires:	openssl-devel >= 0.9.8
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
%patch1 -p1

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

%{__rm} $RPM_BUILD_ROOT%{_bindir}/demo

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
%attr(755,root,root) %{_bindir}/microspdy2http
%attr(755,root,root) %{_libdir}/libmicrohttpd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmicrohttpd.so.10
%attr(755,root,root) %{_libdir}/libmicrospdy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmicrospdy.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmicrohttpd.so
%attr(755,root,root) %{_libdir}/libmicrospdy.so
%{_libdir}/libmicrohttpd.la
%{_libdir}/libmicrospdy.la
%{_includedir}/microhttpd.h
%{_includedir}/microspdy.h
%{_infodir}/libmicrohttpd.info*
%{_infodir}/libmicrohttpd-tutorial.info*
%{_mandir}/man3/libmicrohttpd.3*
%{_pkgconfigdir}/libmicrohttpd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmicrohttpd.a
%{_libdir}/libmicrospdy.a
