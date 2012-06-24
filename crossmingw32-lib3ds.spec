%define		realname	lib3ds
Summary:	The 3D Studio File Format Library - Mingw32 cross version
Summary(pl):	Biblioteka obs�uguj�ca format plik�w 3D Studio - wersja skro�na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/lib3ds/%{realname}-%{version}.tar.gz
# Source0-md5:	3a7f891d18af0151876b98bc05d3b373
URL:		http://lib3ds.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%description
lib3ds is a free alternative to Autodesk's 3DS File Toolkit for
handling 3DS files. It's main goal is to simplify the creation of 3DS
import and export filters.

%description -l pl
lib3ds to wolnodost�pna alternatywa dla 3DS File Toolkit Autodeska do
obs�ugi plik�w 3DS. G��wnym celem biblioteki jest uproszczenie
tworzenia filtr�w importuj�cych i eksportuj�cych 3DS.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

tail -n 116 aclocal.m4 | head -n 102 > acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--host=%{_host} \
	--target=%{target}

%{__make}

cd lib3ds
%{__cc} --shared *.o -Wl,--enable-auto-image-base -o 3ds.dll -Wl,--out-implib,lib3ds.dll.a

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/lib3ds,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

cd lib3ds

install *.h $RPM_BUILD_ROOT%{arch}/include/lib3ds
rm $RPM_BUILD_ROOT%{arch}/include/lib3ds/chunktable.h
install lib3ds{,.dll}.a $RPM_BUILD_ROOT%{arch}/lib
install 3ds.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
