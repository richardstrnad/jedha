"""This Module provides a simple parsing function of cisco cdp output.

It requires 'show cdp neighbor detail' output
"""

import re

_KEYS = {
    'device_id': 'Device ID:',
    'ip_address': r'(?:IP address|IPv4 Address):',
    'platform': r'Platform: (?:cisco)?',
    'capabilities': 'Capabilities:',
    'local_port': 'Interface:',
    'remote_port': r'Port ID \(outgoing port\):',
}

class CDPEntry(object):

    """This Class represents a CDP Entry
    """

    def __init__(self):
        self.device_id = None
        self.ip_address = None
        self.platform = None
        self.capabilities = None
        self.local_port = None
        self.remote_port = None

    @staticmethod
    def _extract_keys(pattern, string):
        res = re.search(r'{}\s?(.*)'.format(pattern), string)
        if res:
            return res.group(1).split(',')[0].strip()
        else:
            return None

    @staticmethod
    def shorten_interface(port, length=2):
        """
        Shortens the Interface Description.
        """
        prefix_re = r'^\w{%s}' % length
        prefix = re.search(prefix_re, port).group(0)
        suffix = re.search(r'\d.*$', port).group(0)
        return '{0}{1}'.format(prefix, suffix)

    def get_all_properties(self, block):
        """
        This method takes in a block and extract out of it the values
        """
        for key, val in _KEYS.items():
            self.__dict__[key] = self._extract_keys(val, block)

    def remove_domain(self):
        """
        Removes the domain portion of the device_id
        """
        return self.device_id.split('.')[0]

    def create_interface_description(self, length=2, remove_domain=True, delimiter=':'):
        """
        Creates an interface description
        """
        remote_port = self.shorten_interface(self.remote_port, length)
        if remove_domain:
            device_id = self.remove_domain()
        else:
            device_id = self.device_id
        return 'interface {}\n  description {}{}{}'.format(self.local_port,
                                                          remote_port,
                                                          delimiter,
                                                          device_id)


class Device(object):
    """
    This Class represents a Device that has one or multiple CDP Entries (Neighbors)
    """
    def __init__(self, cdp_input, hostname=None):
        self.hostname = hostname
        self.cdp_entries = []
        self.cdp_input = cdp_input
        self._split_to_blocks()
        self._get_all_entries()

    def __repr__(self):
        return 'Device: {}'.format(self.hostname)

    def _split_to_blocks(self):
        self.blocks = re.findall(r'-----+((?:.*|\n+)+?)(?:-|$)', self.cdp_input)

    def _get_all_entries(self):
        for block in self.blocks:
            cdp_entry = CDPEntry()
            cdp_entry.get_all_properties(block)
            self.cdp_entries.append(cdp_entry)


def ciscocmd_input(cdp_input):
    """
    This Function accepts an input file that includes the 'show cdp neighbor detail'
    output of multiple devices.
    Format:
    10.215.255.1:show cdp nei det

    10.215.255.1:----------------------------------------
    10.215.255.1:Device ID:sw-05-10.domain.local
    10.215.255.1:VTP Management Domain Name: NONE
    10.215.255.1:
    10.215.255.1:Interface address(es):
    10.215.255.1:    IPv4 Address: 192.168.20.20
    10.215.255.1:Platform: WS-C3850-24P, Capabilities: Switch IGMP Filtering
    10.215.255.1:Interface: mgmt0, Port ID (outgoing port): GigabitEthernet1/0/9
    10.215.255.1:Holdtime: 121 sec
    10.215.255.1:
    10.215.255.1:Version:
    10.215.255.1:Cisco IOS Software, IOS-XE Software, Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 03.03.05SE RELEASE SOFTWARE (fc1)
    10.215.255.1:Technical Support: http://www.cisco.com/techsupport
    10.215.255.1:Copyright (c) 1986-2014 by Cisco Systems, Inc.
    10.215.255.1:Compiled Thu 30-Oct-14 13:12 by prod_rel_team
    10.215.255.1:
    10.215.255.1:Advertisement Version: 2
    10.215.255.1:
    10.215.255.1:Native VLAN: 999
    10.215.255.1:Duplex: full
    10.215.255.1:Mgmt address(es):
    10.215.255.1:    IPv4 Address: 192.168.20.20
    sw-01-02.domain.local:-------------------------
    sw-01-02.domain.local:Device ID: 120-U2-Z33-01
    sw-01-02.domain.local:Entry address(es):
    sw-01-02.domain.local:  IP address: 192.168.55.50
    sw-01-02.domain.local:  IPv6 address: FE80::E25F:B9FF:FE4E:60E2  (link-local)
    sw-01-02.domain.local:Platform: cisco AIR-LAP1142N-E-K9,  Capabilities: Trans-Bridge Source-Route-Bridge IGMP
    sw-01-02.domain.local:Interface: GigabitEthernet3/0/20,  Port ID (outgoing port): GigabitEthernet0
    sw-01-02.domain.local:Holdtime : 168 sec
    sw-01-02.domain.local:
    sw-01-02.domain.local:Version :
    sw-01-02.domain.local:Cisco IOS Software, C1140 Software (C1140-K9W8-M), Version 15.3(3)JN7, RELEASE SOFTWARE (fc1)
    sw-01-02.domain.local:Technical Support: http://www.cisco.com/techsupport
    sw-01-02.domain.local:Copyright (c) 1986-2015 by Cisco Systems, Inc.
    sw-01-02.domain.local:Compiled Tue 25-Aug-15 23:34 by prod_rel_team
    sw-01-02.domain.local:
    sw-01-02.domain.local:advertisement version: 2
    sw-01-02.domain.local:Duplex: full
    sw-01-02.domain.local:Power drawn: 15.400 Watts
    sw-01-02.domain.local:Power request id: 22013, Power management id: 2
    sw-01-02.domain.local:Power request levels are:15400 14500 0 0 0
    sw-01-02.domain.local:Management address(es):
    sw-01-02.domain.local:  IP address: 192.168.55.50
    sw-01-02.domain.local:
    """
    res = {}
    cur = []
    started = False
    for line in cdp_input.split('\n'):
        if '-' * 25 in line and not started:
            started = True
            hostname = re.search(r'(.*?):', line).group(1)
            cur = []
        elif '-' * 25 in line and started:
            if hostname not in res:
                res[hostname] = []
            res[hostname].append(cur)
            hostname = re.search(r'(.*?):', line).group(1)
            cur = []
        new_line = re.sub(r'^.*?:', r'', line)
        cur.append(new_line)
    cur.append(new_line)
    if hostname not in res:
        res[hostname] = []
    res[hostname].append(cur)

    dev_res = []
    for device in res:
        tmp = '\n'.join(['\n'.join(_) for _ in res.get(device)])
        dev_res.append(Device(tmp, hostname=device))
    return dev_res
