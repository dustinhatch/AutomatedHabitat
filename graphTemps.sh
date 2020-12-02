# script to run gnuplot

#!/bin/bash
lastRead="$(tail -1 /home/crnagala/Desktop/sensor_readings.csv|cut -c1-16)"
gnuplot -p -e "titel='${lastRead}';" /home/pi/programs/Temp_Graphs/plot_readings.plot
