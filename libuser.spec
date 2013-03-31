%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: libuser
Version: 0.56.13
Release: 4%{?dist}.1
Group: System Environment/Base
License: LGPLv2+
URL: https://fedorahosted.org/libuser/
Source: https://fedorahosted.org/releases/l/i/libuser/libuser-%{version}.tar.bz2
# Included in libuser-0.56.14.
Patch0: libuser-0.56.13-prompt-not-tty.patch
# Included in libuser-0.56.14.
Patch1: libuser-0.56.13-ldap-password.patch
# Upstream changesets 7be31ab1b558f1b506d9d00f650961c637c1ba8e and
# 072fc6a4a53a1a06281b35820fead48774fc80b2
Patch2: libuser-0.56.13-id_t.patch
# Upstream changeset 276fa0a3078b431e18289285f84a77381b89726c
Patch3: libuser-0.56.13-crypt_style.patch
# #643227, upstream libuser-0.57 fixes this differently
Patch4: libuser-0.56.13-default-pw.patch
# Upstream changesets 3b86efe54ab0f6805c3c4bccd61c1558e39d84b8 and
# f4e2b1c38d0be007bb83b6972c2ede31331c6166
Patch5: libuser-0.56.13-ldap-tests.patch
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: glib2-devel, linuxdoc-tools, pam-devel, popt-devel, python-devel
BuildRequires: cyrus-sasl-devel, libselinux-devel, openldap-devel
# To make sure the configure script can find it
BuildRequires: nscd
# For Patch4
BuildRequires: autoconf, automake, gettext-devel, gtk-doc, libtool
# For %%check
BuildRequires: openldap-clients, openldap-servers
Summary: A user and group account administration library

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.

%package devel
Group: Development/Libraries
Summary: Files needed for developing applications which use libuser
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

%description devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.

%package python
Summary: Python bindings for the libuser library
Group: Development/Libraries
Requires: libuser = %{version}-%{release}

%description python
The libuser-python package contains the Python bindings for
the libuser library, which provides a Python API for manipulating and
administering user and group accounts.

%prep
%setup -q
%patch0 -p1 -b .prompt-not-tty
%patch1 -p1 -b .ldap-password
%patch2 -p1 -b .id_t
%patch3 -p1 -b .crypt_style
%patch4 -p1 -b .default-pw
%patch5 -p1 -b .ldap-tests
chmod a+x tests/default_pw_test

# For Patch4
gtkdocize --docdir docs/reference
libtoolize --force
autopoint -f
aclocal -Wall -I m4
autoconf -Wall
autoheader -Wall
automake -Wall --add-missing

%build
%configure --with-selinux --with-ldap --with-html-dir=%{_datadir}/gtk-doc/html
make

%clean
rm -fr $RPM_BUILD_ROOT

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%find_lang %{name}

%check

make check

# Verify that all python modules load, just in case.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd $RPM_BUILD_ROOT/%{python_sitearch}
python -c "import libuser"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO docs/*.txt
%config(noreplace) %{_sysconfdir}/libuser.conf

%attr(0755,root,root) %{_bindir}/*
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%exclude %{_libdir}/*.la
%exclude %{_libdir}/%{name}/*.la

%files python
%defattr(-,root,root)
%doc python/modules.txt
%{python_sitearch}/*.so
%exclude %{python_sitearch}/*.la

%files devel
%defattr(-,root,root)
%{_includedir}/libuser
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*

%changelog
* Mon Jan 10 2011 Miloslav Trmač <mitr@redhat.com> - 0.56.13-4
- Correctly mark the LDAP default password value as encrypted (CVE-2011-0002)
  Resolves: #668020

* Wed Sep  1 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.13-4
- Change default crypt_style to sha512
  Resolves: #629001

* Wed Jul  7 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.13-3
- Provide LU_VALUE_INVALID_ID and id_t validation in the Python module
  Resolves: #610838

* Mon Feb  8 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.13-2
- Allow supplying passwords from scripts
- Allow specifying a LDAP simple bind password in libuser.conf
  Resolves: #562832

* Fri Dec 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.13-1
- Update to libuser-0.56.13.
  Resolves: #251951
  Resolves: #454079
  Resolves: #456373
  Resolves: #456382
  Resolves: #530513

* Fri Oct  2 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.12-1
- Update to libuser-0.56.12.

* Mon Sep 14 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.11-1
- Update to libuser-0.56.11.
  Resolves: #454091
  Resolves: #456267
  Resolves: #456270
  Resolves: #487129

* Thu Jul 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.10-3
- Fix nscd cache invalidation
  Resolves: #506628
- Preserve timestamps during (make install)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.10-1
- Update to libuser-0.56.10.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.56.9-2
- Rebuild for Python 2.6

* Wed Apr  9 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.9-1
- Update to libuser-0.56.9.

* Sat Feb 23 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.8-1
- New home page at https://fedorahosted.org/libuser/ .

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.56.7-2
- Autorebuild for GCC 4.3

* Wed Jan  9 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.7-1
- Add support for SHA256 and SHA512 in password hashes
  Related: #173583
- Fix file locking on some architectures
- Rename sr@Latn.po to sr@latin.po
  Resolves: #426584
- Address issues from a review by Jason Tibbitts:
  - Remove default.-c, moving the provided functions to libuser proper
  - Remove the WITH_SELINUX build option
  - Move Python library test to %%check
  Resolves: #226054

* Mon Jan 07 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.56.6-4
- Add the usual "there is no upstream" notice.

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.56.6-4
 - Rebuild for openldap bump

* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-3
- Rebuild with openldap-2.4.

* Wed Oct 31 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-2
- Fix uninitialized memory usage when SELinux is disabled

* Thu Oct 25 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-1
- Set SELinux file contexts when creating home directories, preserve them when
  moving home directories
  Resolves: #351201

* Thu Oct 11 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.5-1
- Work around spurious error messages when run against the Fedora Directory
  server
- Fix error reporting when creating home directories and creating/removing mail
  spool files
  Resolves: #318121

* Wed Sep  5 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-3
- s/popt/popt-devel/ in BuildRequires
  Resolves: #277541

* Wed Aug  8 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-2
- Split the Python module to a separate subpackage (original patch by Yanko
  Kaneti)
- Update the License: tag

* Fri Jun 15 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-1
- Update the last password change date field when changing passwords
  Resolves: #243854

* Sat Jun  9 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.3-1
- Allow specifying a SASL mechanism (original patch by Simo Sorce)
  Resolves: #240904

* Thu Apr 19 2007 Miloslav Trmac <mitr@redhat.com> - 0.56.2-1
- New release with updated translations

* Fri Feb 23 2007 Miloslav Trmac <mitr@redhat.com> - 0.56.1-1
- When changing passwords, only silently ignore know shadow markers, not all
  invalid hashes
  Resolves: #225495

* Sat Feb 17 2007 Miloslav Trmac <mitr@redhat.com> - 0.56-1
- Tighten the API and implementation to avoid corrupting number-like strings;
  the module interface ABI has changed
  Resolves: #226976

* Sat Jan  6 2007 Jeremy Katz <katzj@redhat.com> - 0.55-2
- Fix inconsistent PyObject/PyMem usage (#220679)

* Sun Dec 10 2006 Miloslav Trmac <mitr@redhat.com> - 0.55-1
- Update to support the 64-bit API of Python 2.5
- Drop the quota library and Python module

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.54.8-2
- rebuild against python2.5
- follow python packaging guidelines

* Thu Nov  2 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.8-1
- Add importing of HOME from default/useradd
  Related: #204707

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.54.7-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.7-1
- New release with updated translations

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.54.6-2.1
- rebuild

* Wed Jun  7 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.6-2
- Configure without --enable-gtk-doc to fix multilib conflict (#192715)

* Mon May  1 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.6-1
- Fix bugs in handling of invalid lines in the files and shadow modules
- Fix pattern matching in lu_*_enumerate_full in the files and shadow modules
- Add more error reporting, return non-zero exit status on error from utils
- Use the skeleton directory specified in libuser.conf by Python
  admin.createHome and admin.addUser, add parameter skeleton= to admin.addUser
  (#189984)

* Tue Feb 21 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.5-1
- Fix multilib conflict on libuser.conf.5

* Mon Feb 13 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.4-1
- New release with updated translations

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.54.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.54.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.3-1
- Fix crash in lpasswd when user is not specified (#174801)

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.2-1
- Avoid using deprecated openldap functions

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.1-2
- Rebuild with newer openldap

* Tue Oct 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.1-1
- Support importing of configuration from shadow-utils (/etc/login.defs and
  /etc/default/useradd)
- Add libuser.conf(5) man page

* Wed Oct  5 2005 Matthias Clasen <mclasen@redhat.com> - 0.54-2
- Use gmodule-no-export in the .pc file

* Tue Sep 13 2005 Miloslav Trmac <mitr@redhat.com> - 0.54-1
- Make sure attributes with no values can never appear
- Fix crash in the "files" module when an attribute is missing
- Use hidden visibility for internal functions, remove them from
  libuser/user_private.h; this changes module interface ABI

* Wed Jun  8 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.8-1
- Permit "portable" user and group names as defined by SUSv3, plus trailing $
  (#159452)
- Don't build static libraries

* Sat Apr 30 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.7-1
- Rebuild with updated translations, add missing translations.

* Sun Apr 24 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.6-1
- Allow empty configuration values (#155402)

* Fri Apr 15 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.5-1
- Ignore nss_compat lines in the "files" module (#154651)
- Autodetect Python version (#154096)
- Add BuildRequires: libselinux-devel, s/BuildPrereq/BuildRequires/

* Wed Apr  6 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.4-1
- Fix adding objectclasses to existing LDAP entries (#152960)

* Wed Mar 30 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.3-2
- Add Requires: glib2-devel to libuser-devel (#152501)
- Run ldconfig using %%post{,un} -p to let RPM play tricks

* Sat Mar  5 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.3-1
- Don't silently ignore some I/O errors
- Don't include a Cyrus SASL v1 header file when libldap links to v2 (#150046)
- Rebuild with gcc 4

* Mon Jan 17 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.2-1
- Important bug fixes in lchage, lgroupmod, lnewusers and lusermod
- Minor bug fixes in lpasswd and luseradd
- Add man pages for the utilities (#61673)

* Mon Dec 13 2004 Miloslav Trmac <mitr@redhat.com> - 0.53.1-1
- Export UT_NAMESIZE from <utmp.h> to Python (#141273)

* Sun Nov 14 2004 Miloslav Trmac <mitr@redhat.com> - 0.53-1
- Support UID and GID values larger than LONG_MAX (#124967)
- Fix updating of groups after user renaming in lusermod
- Allow setting a shadow password even if the current shadow password is
  invalid (#131180)
- Add lu_{user,group}_unlock_nonempty (#86414); module interface ABI has 
  changed
- Miscellaneous bug and memory leak fixes

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 0.52.6-2
- rebuild against python 2.4

* Tue Nov  2 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.6-1
- Make error reporting more consistent, more verbose and always on stderr
  (partly #133861, original patch by Pawel Salek)
- Mark strings previously blocked by string freeze for translation

* Tue Oct 12 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.5-1
- Fix home directory renaming in ADMIN.modifyUser (#135280)
- Further Python reference counting fixes

* Sun Oct 10 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.4-1
- Fix memory leaks (#113730)
- Build with updated translations

* Wed Sep 29 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.3-1
- Fix compilation without libuser headers already installed (#134085)

* Tue Sep 28 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.2-1
- Allow LDAP connection using ldaps, custom ports or without TLS (original
  patch from Pawel Salek).

* Mon Sep 27 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.1-1
- Fix freecon() of uninitialized value in files/shadow module

* Mon Sep 27 2004 Miloslav Trmac <mitr@redhat.com> - 0.52-1
- Usable LDAP backend (#68052, #99435, #130404)
- Miscellaneous bug fixes

* Fri Sep 24 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.12-1
- Don't claim success and exception at the same time (#133479)
- LDAP fixes, second round
- Various other bugfixes

* Thu Sep 23 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.11-1
- Allow documented optional arguments in Python
  ADMIN.{addUser,modifyUser,deleteUser} (#119812)
- Add man pages for lchfn and lchsh
- LDAP fixes, first round
- Avoid file conflict on multilib systems
- Call ldconfig correctly

* Fri Sep  3 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.10-1
- Don't attempt to lookup using original entity name after entity
  modification (rename in particular) (#78376, #121252)
- Fix copying of symlinks from /etc/skel (#87572, original patch from gLaNDix)
- Make --enable-quota work, and fix the quota code to at least compile (#89114)
- Fix several bugs (#120168, original patch from Steve Grubb)
- Don't hardcode python version in spec file (#130952, from Robert Scheck)
- Properly integrate the SELinux patch, it should actually be used now, even
  though it was "enabled" since 0.51.7-6

* Tue Aug 31 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.9-1
- Fix various typos
- Document library interfaces
- Build all shared libraries with -fPIC (#72536)

* Wed Aug 25 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.8-1
- Update to build with latest autotools and gtk-doc
- Update ALL_LINGUAS and POTFILES.in
- Rebuild to depend on newer openldap

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 0.51.7-7
- fix is_selinux_enabled call

* Sun Dec 14 2003 Jeremy Katz <katzj@redhat.com> 0.51.7-6
- rebuild against python 2.3
- enable SELinux

* Mon Sep 08 2003 Dan Walsh <dwalsh@redhat.com> 0.51.7-5
- Turn off SELinux 

* Wed Aug 06 2003 Dan Walsh <dwalsh@redhat.com> 0.51.7-3
- Add SELinux support

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.7-1
- ldap: set error codes correctly when we encounter failures initializing
- don't double-close modules which fail initialization
- ldap: don't set an error in cases where one is already set

* Tue Feb 18 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.6-1
- use a crypt salt consistent with the defaults/crypt_style setting when
  setting new passwords (#79337)

* Thu Feb  6 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.5-2
- rebuild

* Wed Feb  5 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.5-1
- expose lu_get_first_unused_id() as a package-private function
- provide libuser.ADMIN.getFirstUnusedUid and libuser.ADMIN.getFirstUnusedGid
  in python

* Thu Dec 19 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.4-1
- fix not freeing resources properly in files.c(generic_is_locked), spotted by
  Zou Pengcheng

* Wed Dec 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.2-1
- degrade gracefully
- build with --with-pic and -fPIC
- remove unpackaged man page

* Tue Aug 27 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.1-2
- translation updates

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.1-1
- doc updates -- cvs tree moved
- language updates
- disallow weird characters in account names

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51-1
- files: ignore blank lines in files
- libuser: disallow creation of accounts with names containing whitespace,
  control characters, or non-ASCII characters

* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50.2-1
- refresh translations
- fix a heap-corruption bug in the python bindings

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50-1
- bump version
- refresh translations

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.102-1
- ldap: cache an entity's dn in the entity structure to try to speed things up

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-3
- rebuild in new environment

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-2
- add missing buildreqs on cyrus-sasl-devel and openldap-devel (#59456)
- translation refresh

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-1
- fix python bindings of enumerateFull functions
- adjust prompter wrapping to not error out on successful returns

* Thu Feb 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.100-1
- be more careful about printing error messages
- fix refreshing after adding of accounts
- ldap: try to use a search to convert names to DNs, and only fall back to
  guessing if it turns up nothing
- files: fix an off-by-one in removal of entries

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.99-1
- refresh translations
- fix admin() constructor comments in the python module

* Thu Feb 21 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.98-1
- automatically refresh entities after add, modify, setpass, removepass,
  lock, and unlock operations
- remove debug spewage when creating and removing mail spools
- files: fix saving of multi-valued attributes
- rename MEMBERUID attribute for groups to MEMBERNAME

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.97-1
- files: fix bug in removals
- ldap: revert attempts at being smart at startup time, because it makes UIs
  very messy (up the three whole dialogs just to start the ldap stuff!)

* Sun Feb 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.96-1
- fix thinko in dispatch routines

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.95-1
- lgroupmod: fix thinko

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.94-2
- rebuild in new environment

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.93-1
- move shadow initialization for groups to the proper callback
- rework locking in the files module to not require that files be writable

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com>
- expose lu_strerror()
- add various typedefs for types used by the library

* Mon Jan 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.92-1
- add removepass() functions

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com>
- lchfn,lchsh,lpasswd - reorder PAM authentication calls
- include API docs in the package

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.91-1
- ldap: finish port to new API
- sasl: finish port to new API (needs test)
- libuser: don't commit object changes before passing data to service
  functions which might need differing data sets to figure out what to
  change (for example, ldap)

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.90-1
- bind the internal mail spool creation/removal functions for python

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com>
- renamed the python module
- revamped internals to use gobject's gvalues and gvaluearrays instead of
  glists of cached strings
- add enumeration-with-data functions to the C library

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- require linuxdoc-tools instead of sgml-tools for rawhide

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- fixup build files to allow building for arbitrary versions of python

* Wed Aug 29 2001 Nalin Dahyabhai <nalin@redhat.com> 0.32-1
- link the python module against libpam
- attempt to import the python modules at build-time to verify dependencies

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 0.31-1
- fix a file-parsing bug that popped up in 0.29's mmap modifications

* Mon Aug 27 2001 Nalin Dahyabhai <nalin@redhat.com> 0.30-1
- quotaq: fix argument order when reading quota information
- user_quota: set quota grace periods correctly
- luseradd: never create home directories for system accounts

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add da translation files
- update translations

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 0.29-1
- add an explicit build dependency on jade (for the docs)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- HUP nscd on modifications
- userutil.c: mmap files we're reading for probable speed gain
- userutil.c: be conservative with the amount of random data we read
- docs fixes

* Wed Aug 15 2001 Nalin Dahyabhai <nalin@redhat.com> 0.28-1
- apps: print usage on errors
- lnewusers.c: initialize groups as groups, not users
- lnewusers.c: set passwords for new accounts
- luseradd.c: accept group names in addition to IDs for the -g flag
- luseradd.c: allow the primary GID to be a preexisting group

* Tue Aug 14 2001 Nalin Dahyabhai <nalin@redhat.com> 0.27-1
- add ko translation files
- files.c: fix a heap corruption bug in lock/unlock (#51750)
- files.c: close a memory leak in reading of files

* Mon Aug 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- files.c: remove implementation limits on lengths of lines

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.26-1
- lusermod: change user name in groups the user is a member of during renames
- lgroupmod: change primary GID for users who are in the group during renumbers
- ldap.c: handle new attributes more gracefully if possible
- add ru translation files

* Tue Aug  7 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25.1-1
- rename the quota source files to match the library, which clears up a
  file conflict with older quota packages
- add ja translation files

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- add lu_ent_clear_all() function

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25-1
- close up some memory leaks
- add the ability to include resident versions of modules in the library

* Wed Aug  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-4
- fix incorrect Py_BuildValue invocation in python module

* Tue Jul 31 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-3
- stop leaking descriptors in the files module
- speed up user creation by reordering some checks for IDs being in use
- update the shadowLastChanged attribute when we set a password
- adjust usage of getXXXXX_r where needed
- fix assorted bugs in python binding which break prompting

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.23-1
- install sv translation
- make lpasswd prompt for passwords when none are given on the command line
- make sure all user-visible strings are marked for translation
- clean up some user-visible strings
- require PAM authentication in lchsh, lchfn, and lpasswd for non-networked modules

* Fri Jul 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- print uids and gids of users and names in lid app
- fix tree traversal in users_enumerate_by_group and groups_enumerate_by_users
- implement enumerate_by_group and enumerate_by_user in ldap module
- fix id-based lookups in the ldap module
- implement islocked() method in ldap module
- implement setpass() method in ldap module
- add lchfn and lchsh apps
- add %%d substitution to libuser.conf

* Thu Jul 26 2001 Nalin Dahyabhai <nalin@redhat.com> 0.21-1
- finish adding a sasldb module which manipulates a sasldb file
- add users_enumerate_by_group and groups_enumerate_by_users

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com> 
- luserdel: remove the user's primary group if it has the same name as
  the user and has no members configured (-G disables)
- fixup some configure stuff to make libuser.conf get generated correctly
  even when execprefix isn't specified

* Tue Jul 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.20-1
- only call the auth module when setting passwords (oops)
- use GTrees instead of GHashTables for most internal tables
- files: complain properly about unset attributes
- files: group passwords are single-valued, not multiple-valued
- add lpasswd app, make sure all apps start up popt with the right names

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.18-1
- actually make the new optional arguments optional
- fix lu_error_new() to actually report errors right
- fix part of the python bindings
- include tools in the binary package again
- fixup modules so that password-changing works right again
- add a "key" field to prompt structures for use by apps which like to
  cache these things
- add an optional "mvhomedir" argument to userModify (python)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.16.1-1
- finish home directory population
- implement home directory moving
- change entity get semantics in the python bindings to allow default values for .get()
- add lu_ent_has(), and a python has_key() method to Entity types
- don't include tools in the binary package
- add translated strings

* Thu Jul 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- lib/user.c: catch and ignore errors when running stacks
- lusermod: fix slightly bogus help messages
- luseradd: when adding a user and group, use the gid of the group
  instead of the user's uid as the primary group
- properly set the password field in user accounts created using
  auth-only auth modules (shadow needs "x" instead of "!!")
- implement home directory removal, start on population

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix group password setting in the files module
- setpass affects both auth and info, so run both stacks

* Tue Jul 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- make the testbed apps noinst

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix errors due to uninitialized fields in the python bindings
- add kwargs support to all python wrappers
- add a mechanism for passing arguments to python callbacks

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- stub out the krb5 and ldap modules so that they'll at least compile again
 
* Tue Jul 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't bail when writing empty fields to colon-delimited files
- use permissions of the original file when making backup files instead of 0600

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish implementing is_locked methods in files/shadow module
- finish cleanup of the python bindings
- allow conditional builds of modules so that we can build without
  all of the prereqs for all of the modules

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add error reporting facilities
- split public header into pieces by function
- backend cleanups

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- make %%{name}-devel require %%{name} and not %%{name}-devel

* Fri Jun 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up quota bindings some more
- finish most of the ldap bindings
- fix a subtle bug in the files module that would show up when renaming accounts
- fix mapping methods for entity structures in python

* Thu Jun 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- get bindings for prompts to work correctly
- clean up some of the add/remove semantics (set source on add)
- ldap: implement enumeration
- samples/enum: fix the argument order

* Wed Jun 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up python bindings for quota

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com> 0.11
- finish up python bindings for quota support

* Sun Jun 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish up quota support libs

* Fri Jun  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- start quota support library to get some type safety

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- start looking at quota manipulation

* Wed Jun  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add functions for enumerating users and groups, optionally per-module
- lusermod.c: -s should specify the shell, not the home directory

* Fri Jun  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.10
- finish the python bindings and verify that the file backend works again

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove a redundant check which was breaking modifications

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish adding setpass methods

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9
- get a start on some Python bindings

* Tue May  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.2
- make binary-incompatible change in headers

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.1
- add doxygen docs and a "doc" target for them

* Sat Jan 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8
- add a "quiet" prompter
- add --interactive flag to sample apps and default to using quiet prompter
- ldap: attempt a "self" bind if other attempts fail
- krb5: connect to the password-changing service if the user principal has
  the NULL instance

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- the great adding-of-the-copyright-statements
- take more care when creating backup files in the files module

* Wed Jan  3 2001 Nalin Dahyabhai <nalin@redhat.com> 0.7
- add openldap-devel as a buildprereq
- krb5: use a continuous connection
- krb5: add "realm" config directive
- ldap: use a continuous connection
- ldap: add "server", "basedn", "binddn", "user", "authuser" config directives
- ldap: actually finish the account deletion function
- ldap: don't send cleartext passwords to the directory
- fix naming attribute for users (should be uid, not gid)
- refine the search-by-id,convert-to-name,search-by-name logic
- fix handling of defaults when the config file is read in but contains no value
- implement an LDAP information store
- try to clean up module naming with libtool
- luseradd: pass plaintext passwords along
- luseradd: use symbolic attribute names instead of hard-coded
- lusermod: pass plaintext passwords along
- lgroupadd: pass plaintext passwords along
- lgroupmod: pass plaintext passwords along
- add libuser as a dependency of libuser-devel

* Tue Jan  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.6
- initial packaging
