import sys, logging, re, threading, requests, concurrent.futures

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == '__main__':
	x = input('Masukkan umur (Tahun): ')
	y = raw_input('Nama: ')

	if x == 22:
		yes = False
	else:
		yes = True

if not yes:
	print "Halo, ", y
else:
	print "Go noww!"
