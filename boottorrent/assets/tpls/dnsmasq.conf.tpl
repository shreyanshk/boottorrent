{% if bind_interfaces %}
	bind-interfaces
{% endif %}
interface={{ interface }}

# Do not fork and go background
# because we want to capture output and
# terminate the process programmatically.
keep-in-foreground

# Redirect logs so that Python
# script can capture it.
log-facility=/dev/stdout

# This disables Dnsmasq's DNS function.
port=0

user={{ user }}

{% if enable_dhcp %}
	dhcp-boot=pxelinux.0
	dhcp-leasefile={{ dhcp_leasefile }}
	dhcp-option-force=209,pxelinux.cfg
	dhcp-range={{ dhcp_range }}
{% endif %}

{% if enable_tftp %}
	enable-tftp
	tftp-root={{ ph1 }}
{% endif %}
