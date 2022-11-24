#!/usr/bin/env python
import socket
def use_google_dns():
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.connect(('8.8.8.8', 1))
	local_ip_address = udp_socket.getsockname()[0]
	return local_ip_address


def use_socket_func():
	all_local_ip = [
		item for item in socket.gethostbyname_ex(socket.gethostname())[-1] if not item.startswith('127')
	]
	return all_local_ip


if __name__ == '__main__':
	try:
		local_ip_address = use_google_dns()
	except OSError:
		local_ip_address = use_socket_func()
	finally:
		print(local_ip_address)
