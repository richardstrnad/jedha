import os
import unittest

from jedha.cdp import *
TEST_DIR = 'sample-input/'

with open('{}nxos.txt'.format(TEST_DIR)) as nxos_file:
    NXOS_TEST_FILE = nxos_file.read()

with open('{}ios.txt'.format(TEST_DIR)) as ios_file:
    IOS_TEST_FILE = ios_file.read()

with open('{}ciscocmd.txt'.format(TEST_DIR)) as ciscocmd_file:
    CISCOCMD_TEST_FILE = ciscocmd_file.read()

class TestDeviceClass(unittest.TestCase):

    def test_device_split_to_blocks_nxos(self):
        device = Device(NXOS_TEST_FILE)
        self.assertEqual(len(device.blocks), 13)

    def test_device_split_to_blocks_ios(self):
        device = Device(IOS_TEST_FILE)
        self.assertEqual(len(device.blocks), 3)

    def test_device_get_all_entries_nxos(self):
        device = Device(NXOS_TEST_FILE)
        self.assertEqual(len(device.blocks), len(device.cdp_entries))

    def test_device_get_all_entries_ios(self):
        device = Device(IOS_TEST_FILE)
        self.assertEqual(len(device.blocks), len(device.cdp_entries))


class TestCDPEntryClass(unittest.TestCase):
    def test_get_all_properties_nxos(self):
        device = Device(NXOS_TEST_FILE)
        self.assertEqual(device.cdp_entries[0].device_id, 'NETS999999.domain.local')
        self.assertEqual(device.cdp_entries[0].ip_address, '192.168.1.19')
        self.assertEqual(device.cdp_entries[0].platform, 'WS-C3560-48PS')
        self.assertEqual(device.cdp_entries[0].capabilities, 'Switch IGMP')
        self.assertEqual(device.cdp_entries[0].local_port, 'GigabitEthernet2/0/23')
        self.assertEqual(device.cdp_entries[0].remote_port, 'GigabitEthernet0/1')

    def test_get_all_properties_ios(self):
        device = Device(IOS_TEST_FILE)
        self.assertEqual(device.cdp_entries[0].device_id, 'MyAp001')
        self.assertEqual(device.cdp_entries[0].ip_address, '192.168.9.45')
        self.assertEqual(device.cdp_entries[0].platform, 'AIR-LAP1131G-E-K9')
        self.assertEqual(device.cdp_entries[0].capabilities, 'Trans-Bridge')
        self.assertEqual(device.cdp_entries[0].local_port, 'GigabitEthernet0/20')
        self.assertEqual(device.cdp_entries[0].remote_port, 'FastEthernet0')

    def test_remove_domain(self):
        device = Device(NXOS_TEST_FILE)
        self.assertEqual(device.cdp_entries[0].remove_domain(), 'NETS999999')
        self.assertNotIn(device.cdp_entries[0].remove_domain(), 'domain.local')

    def test_shorten_interface(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        self.assertEqual(cur_dev.shorten_interface(cur_dev.local_port), 'Gi2/0/23')
        self.assertEqual(cur_dev.shorten_interface(cur_dev.remote_port), 'Gi0/1')

    def test_shorten_interface_with_arguments(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        self.assertEqual(cur_dev.shorten_interface(cur_dev.local_port, length=4), 'Giga2/0/23')
        self.assertEqual(cur_dev.shorten_interface(cur_dev.remote_port, length=5), 'Gigab0/1')

    def test_create_interface_description(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        out = cur_dev.create_interface_description()
        self.assertEqual(out, 'interface GigabitEthernet2/0/23\n  description Gi0/1:NETS999999')

    def test_create_interface_description_with_length(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        out = cur_dev.create_interface_description(length=6)
        self.assertEqual(out, 'interface GigabitEthernet2/0/23\n  description Gigabi0/1:NETS999999')

    def test_create_interface_description_with_remove_domain(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        out = cur_dev.create_interface_description(remove_domain=False)
        self.assertEqual(out, 'interface GigabitEthernet2/0/23\n  description Gi0/1:NETS999999.domain.local')

    def test_create_interface_description_with_delimiter(self):
        device = Device(NXOS_TEST_FILE)
        cur_dev = device.cdp_entries[0]
        out = cur_dev.create_interface_description(delimiter=' - ')
        self.assertEqual(out, 'interface GigabitEthernet2/0/23\n  description Gi0/1 - NETS999999')


class TestCiscoCMDParser(unittest.TestCase):
    def test_ciscocmd_input_parse_devices_and_hostnames(self):
        devices = ciscocmd_input(CISCOCMD_TEST_FILE)
        hostnames = ['192.168.255.1', 'KUCA1-u1-as01.domain.local']
        for dev in devices:
            self.assertIn(dev.hostname, hostnames)

    def test_ciscocmd_input_line_split(self):
        devices = ciscocmd_input(CISCOCMD_TEST_FILE)
        for dev in devices:
            if dev.hostname == '192.168.255.1':
                self.assertEqual(len(dev.cdp_entries), 24)
                self.assertEqual(dev.cdp_entries[-1].device_id, 'KUCA1-U1-IS01.domain.local')
                self.assertEqual(dev.cdp_entries[-1].ip_address, '192.168.249.20')
                self.assertEqual(dev.cdp_entries[-1].platform, 'WS-C3850-24P')
                self.assertEqual(dev.cdp_entries[-1].capabilities, 'Switch IGMP Filtering')
                self.assertEqual(dev.cdp_entries[-1].local_port, 'Ethernet101/1/8')
                self.assertEqual(dev.cdp_entries[-1].remote_port, 'GigabitEthernet1/0/18')
            else:
                self.assertEqual(len(dev.cdp_entries), 22)
                self.assertEqual(dev.cdp_entries[-1].device_id, '899-LO-106-01')
                self.assertEqual(dev.cdp_entries[-1].ip_address, '55.50.2.149')
                self.assertEqual(dev.cdp_entries[-1].platform, 'AIR-LAP1142N-E-K9')
                self.assertEqual(dev.cdp_entries[-1].capabilities, 'Trans-Bridge Source-Route-Bridge IGMP')
                self.assertEqual(dev.cdp_entries[-1].local_port, 'GigabitEthernet3/0/18')
                self.assertEqual(dev.cdp_entries[-1].remote_port, 'GigabitEthernet0')


if __name__ == '__main__':
    unittest.main()