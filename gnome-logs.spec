Summary:	Log viewer for the systemd journal
Name:		gnome-logs
Version:	3.12.1
Release:	1
License:	GPL v3
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-logs/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	3ae17008b5d25eef65cf0ef8581bff9f
URL:		https://wiki.gnome.org/Apps/Logs
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libxslt-progs
BuildRequires:	pkg-config
BuildRequires:	systemd-devel
BuildRequires:	yelp-tools
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires:	gsettings-desktop-schemas
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Logs is a viewer for the systemd journal.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e '/GNOME_COMPILE_WARNINGS.*/d'	\
    -i -e '/GNOME_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/GNOME_COMMON_INIT/d'		\
    -i -e '/GNOME_CXX_WARNINGS.*/d'		\
    -i -e '/GNOME_DEBUG_CHECK/d'		\
    -i -e '/APPDATA_XML/d' configure.ac
%{__sed} -i '/@APPDATA_XML_RULES@/d' Makefile.am

%build
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-logs
%{_desktopdir}/gnome-logs.desktop
%{_mandir}/man1/gnome-logs.1*
%{_iconsdir}/hicolor/*/*/*.png

