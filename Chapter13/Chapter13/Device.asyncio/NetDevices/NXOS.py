#coding:utf-8
from NetDevices.Device import Device
from pexpect import EOF,TIMEOUT

class NXOS(Device):

    def __init__(self, device):
        super(NXOS, self).__init__(device)
        self.prompt = self.hostname + "[>|#]\s?"

    async def login(self, prompt=""):
        if not prompt:
            prompt = self.prompt
        await super(NXOS, self).login(prompt)
        await self._set_terminal_length_zero()

    async def _set_terminal_length_zero(self):
        self.c.sendline("terminal length 0")
        try:
            i = await self.c.expect(self.prompt, async_=True)
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")

    async def get_config(self):
        self.expect_list = []
        self.expect_list.append(self.prompt)
        result = []
        self.c.sendline("show running-config")
        try:
            i = await self.c.expect(self.expect_list, timeout=20, async_=True)
            if i == 0:
                result.append(i)
                result.append((self.c.before + self.c.after).decode()) 
        except EOF:
            pass
        except TIMEOUT:
            print("session timeout")
        return result
