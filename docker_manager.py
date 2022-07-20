import subprocess
import time

# close all running container 
def stop_all_containers():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_car.sh")
    time.sleep(1)
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_bike.sh")
    time.sleep(1)
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_foot.sh")
    time.sleep(1)
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_nominatim.sh")
    time.sleep(3)

# run nominatim docker container
def run_nominatim_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_run_nominatim.sh")
    time.sleep(2)

def stop_nominatim_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_nominatim.sh")
    time.sleep(2)

# run car docker container
def run_car_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_run_car.sh")
    time.sleep(2)

def stop_car_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_car.sh")
    time.sleep(2)

def run_foot_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_run_foot.sh")
    time.sleep(2)

def stop_foot_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_foot.sh")
    time.sleep(2)
    
def run_bike_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_run_bike.sh")
    time.sleep(2)

def stop_bike_container():
    subprocess.call("/home/bdroix/bdroix/express_cv_tools/docker_exec/docker_stop_bike.sh")
    time.sleep(2)