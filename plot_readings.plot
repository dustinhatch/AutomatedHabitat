set datafile separator ','
set xdata time
set timefmt "%Y-%m-%d %H:%M"
set format x "%d-%H:%M"

set key autotitle columnhead
set ylabel "Temp (F)"
set xlabel "Date-Time"
set yrange [60:110]


set style line 1 lt 1 lc rgb '#cc00ff' lw 1.5 
set style line 2 lt 1 lc rgb '#e68a00' lw 1.5 

set object 1 rectangle from graph 0, graph 0 to graph 1, graph 1 behind fc rgb '#eeeeee' fs noborder

set style line 100 lt 1 lc rgb "grey" lw 0.5
set grid ls 100
set ytics 5
set ytics nomirror
set xtics auto
set xtics rotate

set key top horizontal center font ",12"

set terminal pngcairo size 1200,600 font 'Segoe UI,12'
set title titel

set output '/home/pi/programs/Temp_Graphs/graphs/Tempurature.png'
plot '< (head -1 && tail -120) < /home/pi/programs/sensor_readings.csv' using 1:2 with lines ls 1


set ylabel "Humidity (%)"
set yrange [0:100]
set ytics 10

set output '/home/pi/programs/Temp_Graphs/graphs/Humidity.png'
plot '< (head -1 && tail -120) < /home/pi/programs/Temp_Graphs/sensor_readings.csv' using 1:3 with lines ls 2
