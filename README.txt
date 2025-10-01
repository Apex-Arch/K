# Optimize system first
chmod +x Optimization.sh
./Optimization.sh

# Install dependencies
pip3 install aiohttp cryptography fake-useragent psutil schedule

# Start 48-hour assessment
python3 Absolute-Bomber.py

# In separate terminal, start monitoring
python3 Monitor.py