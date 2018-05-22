{% if bind_interfaces %}
	bind-interfaces
{% endif %}
interface={{ interface }}
keep-in-foreground
log-facility=/dev/stdout
port={{ port }}
user={{ user }}

dhcp-boot=pxelinux.0
dhcp-leasefile={{ dhcp_leasefile }}
dhcp-option-force=209,pxelinux.cfg
dhcp-range={{ dhcp_range }}

{% if enable_tftp %}
	enable-tftp
	tftp-root={{ ph1 }}
{% endif %}
