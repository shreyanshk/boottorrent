bt-enable-lpd={% if bt_enable_lpd %}true{% else %}false{% endif %}
check-integrity
console-log-level={{ console_log_level }}
disable-ipv6=true
dir={{ dir }}
enable-dht=false
enable-dht6=false
enable-peer-exchange={% if enable_peer_exchange %}true{% else %}false{% endif %}
input-file={{ input_file }}
log=-
log-level={{ console_log_level }}
seed-ratio=0.0
quiet=true
