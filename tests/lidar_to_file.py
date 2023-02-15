import sys
from lidar_lib import RPLidar
import time
PORT_NAME = '/dev/ttyUSB0'

max_time = 5

def run(path):

    lidar = RPLidar(PORT_NAME, baudrate=256000)
    outfile = open(path, 'w')
    try:
        print('Recording measurements... Press Crl+C to stop.')
        start_time = time.time()

        for measurement in lidar.iter_scans():
            line = '\t'.join(str(v) for v in measurement)
            outfile.write(line + '\n')
            if time.time() - start_time > max_time:
                raise KeyboardInterrupt('Max time record reached')
    except KeyboardInterrupt:
        print('Stopping.')
        lidar.stop_motor()
        lidar.disconnect()
        outfile.close()


if __name__ == '__main__':
    run('lidar_out.txt')
