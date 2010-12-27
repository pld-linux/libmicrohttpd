#
# Conditional build
%bcond_with	tests
#
Summary:	Embeded HTTP server library
Summary(pl.UTF-8):	Biblioteka wbudowanego serwera HTTP
Name:		libmicrohttpd
Version:	0.9.4
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
# Source0-md5:	31f37439095e1f7143af97207f03aa14
URL:		http://www.gnu.org/software/libmicrohttpd/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	libgcrypt-devel >= 1.2.4
BuildRequires:	libtool
%if %{with tests}
BuildRequires:	curl-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.

%description -l pl.UTF-8
GNU libmicrohttpd jest małą biblioteką C, w założeniu umożliwiającą
uruchomienie serwera HTTP jako część innej aplikacji.

%package devel
Summary:	Header files to develop libmicrohttpd applications
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania aplikacji używających libmicrohttpd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

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
%attr(755,root,root) %ghost %{_libdir}/libmicrohttpd.so.10

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmicrohttpd.so
%{_libdir}/libmicrohttpd.la
%{_includedir}/microhttpd.h
%{_infodir}/microhttpd.info*
%{_mandir}/man3/libmicrohttpd.3*
%{_pkgconfigdir}/libmicrohttpd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmicrohttpd.a
