Name:           vlmcsd
Version:        svn1113
Release:        1%{?dist}
Summary:        KMS Emulator

License:        Unlicense
URL:            https://github.com/simaek/vlmcsd
Source0:        vlmcsd-%{version}.tar.gz

Group:          Networking/Utilities
Packager:       Yaser Hsueh <master@simaek.com>

#BuildRequires:  
#Requires:       

%description
A fully Microsoft compatible KMS server


%prep
%autosetup


%build
%make_build
gzip man/vlmcs.1
gzip man/vlmcsd-floppy.7
gzip man/vlmcsd.7
gzip man/vlmcsd.8
gzip man/vlmcsd.ini.5
gzip man/vlmcsdmulti.1


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
install -D $RPM_BUILD_DIR/%{name}-%{version}/bin/vlmcsd $RPM_BUILD_ROOT/usr/sbin/vlmcsd
install -D $RPM_BUILD_DIR/%{name}-%{version}/bin/vlmcs $RPM_BUILD_ROOT/usr/sbin/vlmcs

install -d $RPM_BUILD_ROOT/etc/vlmcsd
install -d $RPM_BUILD_ROOT/usr/lib/systemd/system

cp etc/vlmcsd.ini $RPM_BUILD_ROOT/etc/vlmcsd/vlmcsd.ini
cp etc/vlmcsd.kmd $RPM_BUILD_ROOT/etc/vlmcsd/vlmcsd.kmd
cp systemd/vlmcsd.service $RPM_BUILD_ROOT/usr/lib/systemd/system

install -d $RPM_BUILD_ROOT/usr/share/man/man1
install -d $RPM_BUILD_ROOT/usr/share/man/man5
install -d $RPM_BUILD_ROOT/usr/share/man/man7
install -d $RPM_BUILD_ROOT/usr/share/man/man8

cp man/vlmcs.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
cp man/vlmcsd-floppy.7.gz $RPM_BUILD_ROOT/usr/share/man/man7
cp man/vlmcsd.7.gz $RPM_BUILD_ROOT/usr/share/man/man7
cp man/vlmcsd.8.gz $RPM_BUILD_ROOT/usr/share/man/man8
cp man/vlmcsd.ini.5.gz $RPM_BUILD_ROOT/usr/share/man/man5
cp man/vlmcsdmulti.1.gz $RPM_BUILD_ROOT/usr/share/man/man1

%files
%defattr(-,root,root)
%attr(755,root,root) /usr/sbin/vlmcsd
%attr(755,root,root) /usr/sbin/vlmcs
%attr(644,root,root) /etc/vlmcsd/vlmcsd.ini
%attr(644,root,root) /etc/vlmcsd/vlmcsd.kmd
%attr(644,root,root) /usr/lib/systemd/system/vlmcsd.service
%attr(644,root,root) /usr/share/man/man1/vlmcs.1.gz
%attr(644,root,root) /usr/share/man/man1/vlmcsdmulti.1.gz
%attr(644,root,root) /usr/share/man/man5/vlmcsd.ini.5.gz
%attr(644,root,root) /usr/share/man/man7/vlmcsd.7.gz
%attr(644,root,root) /usr/share/man/man7/vlmcsd-floppy.7.gz
%attr(644,root,root) /usr/share/man/man8/vlmcsd.8.gz
%doc

%changelog

%pre
if ! grep -q vlmcs /etc/group; then
  echo 'Creating vlmcs group'
  /usr/sbin/groupadd -r vlmcsd
fi

if ! /usr/bin/id -u vlmcs > /dev/null 2>&1; then
  echo 'Creating vlmcs user'
  /usr/sbin/useradd -M -N -g vlmcsd -r -s /bin/false vlmcsd
fi

%post 
if [ -f /bin/systemctl ]; then
  if [ ! -f /.dockerenv ]; then
      /bin/systemctl daemon-reload
      # NOTE: do not enable any services during first installation
  fi
fi

%preun
if [ -f /bin/systemctl ]; then
  if [ ! -f /.dockerenv ]; then
      # possibly remove the installed services
      %systemd_preun vlmcsd.service
  fi
fi

%postun
if [ -f /bin/systemctl ]; then
  if [ ! -f /.dockerenv ]; then
      # possibly restart the running services
      %systemd_postun_with_restart vlmcsd.service
  fi
fi

