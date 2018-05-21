{% if bind_interfaces %}bind-interfaces{% endif %}
dhcp-boot=pxelinux.0
dhcp-leasefile={{ dhcp_leasefile }}
#path of config file for the pxe bootloader (relative to root of assets)
dhcp-option-force=209,isolinux.cfg
dhcp-range={{ dhcp_range }}
enable-tftp
interface={{ interface }}
keep-in-foreground
log-facility=/dev/stdout
port={{ port }}
#PXE bootloader to run
tftp-root={{ ph1 }}
user={{ user }}

