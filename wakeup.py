import socket
import binascii
import logging

class RemoteWakeOnLan:
    def __init__(self, log_file='wol.log'):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def wake_on_lan(self, mac_address):
        try:
            # 格式化MAC地址
            mac_bytes = mac_address.split(':')
            mac = b''
            for byte in mac_bytes:
                mac += binascii.unhexlify(byte)
            
            # 创建魔术数据包
            magic_packet = b'\xff'*6 + mac*16
            
            # 发送UDP数据包
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            udp_socket.sendto(magic_packet, ('<broadcast>', 9))
            udp_socket.close()
            
            logging.info(f'成功发送唤醒信号至MAC地址: {mac_address}')
        except Exception as e:
            logging.error(f'发送唤醒信号时出现异常: {str(e)}')

# 创建RemoteWakeOnLan实例
wol = RemoteWakeOnLan()

# 目标计算机的MAC地址
target_mac_address = 'AA:BB:CC:DD:EE:FF'

# 唤醒目标计算机
wol.wake_on_lan(target_mac_address)
