import matplotlib.pyplot as plt
from time import sleep
from app import app, database

plt.figure()

try:
    app.run(host='0.0.0.0', port=3001)
    while True:
        sleep(1)

except KeyboardInterrupt:
    database.dump_to_pkl()
