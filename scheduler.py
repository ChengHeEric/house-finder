import schedule
import time
import subprocess

# Function to run a python file
def run_script(script_name):
    subprocess.run(['python', script_name])

# Schedule your Python script to run at 9 AM every day
schedule.every().day.at("09:00").do(run_script, 'house_finder.py')
schedule.every().day.at("09:01").do(run_script, 'add_extra_info.py')
schedule.every().day.at("09:02").do(run_script, 'analysis_and_rank.py')

# Keep the script running to check the schedule
while True:
    schedule.run_pending()
    time.sleep(1)