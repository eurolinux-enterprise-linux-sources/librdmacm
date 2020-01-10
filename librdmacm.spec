%define _hardened_build 1

Name: librdmacm
Version: 1.0.21
Release: 1%{?dist}
Summary: Userspace RDMA Connection Manager
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibverbs-devel > 1.1.5 chrpath ibacm-devel
%ifnarch ia64 %{sparc} s390 s390x
BuildRequires: valgrind-devel
%endif

%description
librdmacm provides a userspace RDMA Communication Managment API.

%package devel
Summary: Development files for the librdmacm library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release} libibverbs-devel%{?_isa}

%description devel
Development files for the librdmacm library.

%package static
Summary: Static development files for the librdmacm library
Group: System Environment/Libraries

%description static
Static libraries for the librdmacm library.

%package utils
Summary: Examples for the librdmacm library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description utils
Example test programs for the librdmacm library.

%prep
%setup -q

%build
%ifnarch ia64 %{sparc} s390 s390x
%configure --with-valgrind
%else
%configure
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} CFLAGS="$CXXFLAGS -fno-strict-aliasing" LDFLAGS="$LDFLAGS -lpthread"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/rsocket/*.la
# kill rpaths
chrpath -d %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/librdmacm*.so.*
%{_libdir}/rsocket/*.so.*
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/rsocket/lib*.so
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/rsocket/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Jun 05 2015 Doug Ledford <dledford@redhat.com> - 1.0.21-1
- Update to latest upstream release
- Build on s390
- Related: bz1186159

* Thu Oct 09 2014 Doug Ledford <dledford@redhat.com> - 1.0.19.1-1
- Update to latest upstream release
- Resolves: bz1059133

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 1.0.17.1-1
- Update to latest upstream release
- Resolves: bz978658

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.17-2
- Mass rebuild 2013-12-27

* Mon Mar 25 2013 Doug Ledford <dledford@redhat.com> - 1.0.17-1
- Grab actual upstream release 1.0.17 now that it's available

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-0.gitc6bfc1c.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Doug Ledford <dledford@redhat.com> - 1.0.17-0.gitc6bfc1c.1
- Update to upstream git repo version to pick up fix for CVE-2012-4516
- Resolves: bz865510

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.15-1
- Update to latest upstream tarball
- Add in latest git commits as patches

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-1
- Update to latest upstream release
- Rebuild against latest libibverbs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 19 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-3
- Fix up link problem caused by change to default DSO linking (bz564870)

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-2
- ExcludeArch s390(x) as the hardware doesn't exist there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 1.0.10-1
- Update to latest upstream release
- Change Requires on -devel package (bz533937)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Mar 29 2008 Roland Dreier <rolandd@cisco.com> - 1.0.7-1
- New upstream release

* Fri Feb 22 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-2
- Spec file cleanups from Fedora review: add BuildRequires for
  libibverbs, and move the static library to -static.

* Fri Feb 15 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-1
- Initial Fedora spec file

