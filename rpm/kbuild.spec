#
# spec file for package kbuild
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.nemomobile.org/
#
Url:            http://svn.netlabs.org/kbuild

Name:           kbuild
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libacl-devel
BuildRequires:  gettext-devel
BuildRequires:  byacc
Summary:        Framework for writing simple makefiles for complex tasks
License:        GPL-2.0+
Group:          Development/Tools/Building
Version:        0.1.9998svn2543
Release:        0
%define _svnrev 2543
Source0:        %{name}-%{version}.tar.bz2
# Keep the suse changelog for history
Source99:	kbuild.changes_suse
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The goals of the kBuild framework: - Similar behavior across all
   supported platforms
- Flexibility, don't create unnecessary restrictions preventing
   ad-hoc solutions
- Makefiles can be simple to write and maintain
- One configuration file for a subtree automatically included
- Target configuration templates as the primary mechanism for
   makefile simplification
- Tools and SDKs for helping out the templates with flexibility
- Non-recursive makefile method by using sub-makefiles

Authors:
--------
    Knut St. Osmundsen <bird-kbuild-spam@anduin.net>

%prep
# version may contain a +, which breaks the build because of the
# use of ar -M scripts.
# So change the buildsubdir to be different from what's in the tarfile
%setup -q -n %{name} -c
mv %{name}-%{version}/%{name}/* .

%build
export CFLAGS="$RPM_OPT_FLAGS"
%__cat > SvnInfo.kmk << EOF
KBUILD_SVN_REV := %{_svnrev}
KBUILD_SVN_URL := http://svn.netlabs.org/repos/kbuild/trunk
EOF
kBuild/env.sh --full make -f bootstrap.gmk SRCDIR=`pwd`
kBuild/env.sh kmk rebuild PATH_INS=`pwd`
pod2man -c 'kBuild for Mer/Nemo' -r kBuild-%version kmk.pod > kmk.1

%install
kBuild/env.sh kmk NIX_INSTALL_DIR=/usr BUILD_TYPE=release PATH_INS=%{buildroot} LDFLAGS=-Wl,--as-needed install
%__install -m 644 -D kmk.1 %buildroot/%_mandir/man1/kmk.1
#remove execute flag, if occurs
%__chmod a-x %{buildroot}/%{_datadir}/kBuild/*/*kmk
%__rm -r %{buildroot}%{_datadir}/doc/kBuild-0.1.9998

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc COPYING ChangeLog
%doc kBuild/doc/COPYING-FDL-1.3
%doc kBuild/doc/QuickReference-kmk.*
%{_mandir}/man1/kmk.1.gz
%{_bindir}/*
%{_datadir}/kBuild
