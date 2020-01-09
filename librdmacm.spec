Name: librdmacm
Version: 1.0.19.1
Release: 1.1%{?dist}
Summary: Userspace RDMA Connection Manager
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
Patch0:	cma.c.nofprintf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x
BuildRequires: libibverbs-devel >= 1.1, chrpath, ibacm-devel >= 1.0.8

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
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --with-ib_acm
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} CFLAGS="$CXXFLAGS -fno-strict-aliasing" LDFLAGS="-lpthread"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/rsocket/*.la
# kill rpaths
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/rsocket/*.so
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
* Thu Jan 07 2016 Donald Dutile <ddutile@redhat.com> - 1.0.19.1-1.1
- Silence warning/errors messages to stderr when RDMA hw not installed
- Resolves: bz1296408

* Wed Mar 11 2015 Doug Ledford <dledford@redhat.com> - 1.0.19.1-1
- Update to latest upstream release
- Drop patches that upstream has folded in
- Resolves: bz1119108

* Tue Jun 17 2014 Doug Ledford <dledford@redhat.com> - 1.0.18.1-1
- Update to latest upstream release
- Related: bz1056662

* Wed Aug 07 2013 Doug Ledford <dledford@redhat.com> - 1.0.17-1
- Official 1.0.17 release
- The fix to bug 866221 got kicked back as incomplete last time, fix
  it for real this time.
- Intel adapters that use the qib driver don't like using inline data,
  so use a memory region that is registered instead
- Resolves: bz866221, bz828071

* Sun Oct 14 2012 Doug Ledford <dledford@redhat.com> - 1.0.17-0.git4b5c1aa
- Pre-release version of 1.0.17
- Resolves a CVE vulnerability between librdmacm and ibacm
- Fixes various minor bugs in sample programs
- Resolves: bz866221, bz816074

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0.15-2
- Build against new ib_acm service
- Related: bz700285

* Fri Jan 20 2012 Doug Ledford <dledford@redhat.com> - 1.0.15-1
- Update to latest upstream release (adds FDR support and fixes 696019 the
  upstream way)
- Include fixes in git not yet in a release
- Related: bz750609
- Resolves: bz700289

* Tue Sep 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-4
- Fix for the fix to bug 696019

* Mon Aug 01 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-3
- Oops, change how we set -fno-strict-aliasing to get FORTIFY_SOURCE back
- Related: bz725016

* Mon Aug 01 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-2
- Add -fno-strict-aliasing to CFLAGS due to rpmdiff failure
- Related: bz725016

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-1
- Update to latest upstream version
- Fix segfault in rping usage
- Related: bz725016, bz696019

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
