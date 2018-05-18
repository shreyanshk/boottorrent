port={{ port }}
interface={{ interface }}
{% if bind_interfaces %}bind-interfaces{% endif %}
dhcp-range={{ dhcp_range }}
{% if enable_tftp %}enable-tftp{% endif %}
