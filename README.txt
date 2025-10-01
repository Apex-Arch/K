# Install dependencies (if needed)
pip3 install requests

# First, scan for open ports
python3 scan_all_ports.py

# Launch the main Slowloris attack
python3 slowloris_port_saturation.py

# In separate terminal, monitor the attack progress
python3 monitor_attack.py
