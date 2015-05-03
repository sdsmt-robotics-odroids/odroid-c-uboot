%global commit 9c256c87b5ba97a626138d60f5af1ad5c235d55a

Name:           odroid-c-uboot
Version:        2015.01.03
Release:        1%{?dist}
Summary:        U-boot for ODROID-C

Group:          System Environment/Base
License:        GPLv2
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-c1
Source0:        https://github.com/hardkernel/u-boot/archive/%{commit}/u-boot-%{commit}.tar.gz
Source1:        boot.ini
Source2:        grubby
Source3:        hardkernel-1080.bmp
Source4:        hardkernel-720.bmp

# We always need to use a cross compiler because we can't use hardfloat static
# libraries. This means that we'll always produce an ARM package, even when
# built on x86 machines. The code compiled here is also indifferent of the
# architecture used on the ODROID's OS.
BuildArch:      noarch

BuildRequires:  arm-none-eabi-gcc-cs
Requires:       grubby

%description
U-boot for Hardkernel's ODROID-C. This package installs u-boot.bin and a
default boot.ini, and also configures grubby.

%prep
%setup -qn u-boot-%{commit}

%build
make %{?_smp_mflags} odroidc_config
make %{?_smp_mflags} CROSS_COMPILE=arm-none-eabi-

%install
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_datadir}/%{name}/grubby-%{version}-%{release}
install -p -m0644 -D %{SOURCE1} %{buildroot}/boot/uboot/boot.ini
install -p -m0755 -D sd_fuse/u-boot.bin %{buildroot}/boot/uboot/u-boot.bin

ln -s grubby-%{version}-%{release} %{buildroot}%{_datadir}/%{name}/grubby

install -p -m0644 -D %{SOURCE3} %{buildroot}/boot/uboot/hardkernel-1080.bmp
install -p -m0644 -D %{SOURCE4} %{buildroot}/boot/uboot/hardkernel-720.bmp

%post
cat %{_datadir}/%{name}/grubby-%{version}-%{release} >> %{_sysconfdir}/sysconfig/uboot

%preun
while read l; do
  sed -i "0,/^`echo "$l" | sed 's/\//\\\\\//g'`/{//d}" %{_sysconfdir}/sysconfig/uboot
done < %{_datadir}/%{name}/grubby-%{version}-%{release}

%files
%doc COPYING CREDITS MAINTAINERS README
%{_datadir}/%{name}/grubby
%{_datadir}/%{name}/grubby-%{version}-%{release}
%config(noreplace) /boot/uboot/boot.ini
/boot/uboot/u-boot.bin
/boot/uboot/hardkernel-1080.bmp
/boot/uboot/hardkernel-720.bmp

%changelog
* Sat May 02 2015 Scott K Logan <logans@cottsay.net> - 2015.01.03-1
- Initial package
