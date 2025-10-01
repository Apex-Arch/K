# Optimize system first
chmod +x optimize_for_high_pps.sh
sudo ./optimize_for_high_pps.sh

# Install dependencies
pip3 install aiohttp fake-useragent

# Run the high-velocity botnet
sudo python3 high_velocity_botnet.py
