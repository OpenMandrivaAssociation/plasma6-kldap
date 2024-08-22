#define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
%define major 6
%define libname %mklibname KPim6LdapCore
%define devname %mklibname KPim6LdapCore -d
%define wlibname %mklibname KPim6LdapWidgets
%define wdevname %mklibname KPim6LdapWidgets -d

Name: plasma6-kldap
Version:	24.08.0
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Release:	%{?git:0.%{git}.}1
%if 0%{?git:1}
Source0:	https://invent.kde.org/pim/kldap/-/archive/%{gitbranch}/kldap-%{gitbranchd}.tar.bz2#/kldap-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{ftpdir}/release-service/%{version}/src/kldap-%{version}.tar.xz
%endif
Summary: KDE library for accessing LDAP directories
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: pkgconfig(ldap)
BuildRequires: sasl-devel
BuildRequires: cmake(KF6Completion)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KPim6Mbox)
BuildRequires: cmake(KF6Wallet)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6DocTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Keychain)
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt6-qttools-assistant
Requires: plasma6-akonadi-contacts

%description
KDE library for accessing LDAP directories.

%package -n %{libname}
Summary: KDE library for accessing LDAP directories
Group: System/Libraries

%description -n %{libname}
KDE library for accessing LDAP directories.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{wlibname}
Summary: KDE library for accessing LDAP directories (Widgets)
Group: System/Libraries

%description -n %{wlibname}
KDE library for accessing LDAP directories (Widgets).

%package -n %{wdevname}
Summary: Development files for %{name} Widgets
Group: Development/C
Requires: %{wlibname} = %{EVRD}
Requires: %{devname} = %{EVRD}

%description -n %{wdevname}
Development files (Headers etc.) for %{name} Widgets.

%prep
%autosetup -p1 -n kldap-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang %{name} --all-name --with-html

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/kldap.categories
%{_datadir}/qlogging-categories6/kldap.renamecategories
%{_libdir}/qt6/plugins/kf6/kio/ldap.so

%files -n %{libname}
%{_libdir}/libKPim6LdapCore.so*

%files -n %{wlibname}
%{_libdir}/libKPim6LdapWidgets.so*

%files -n %{devname}
%{_includedir}/KPim6/KLDAPCore
%{_libdir}/cmake/KPim6LdapCore

%files -n %{wdevname}
%{_includedir}/KPim6/KLDAPWidgets
%{_libdir}/cmake/KPim6LdapWidgets
