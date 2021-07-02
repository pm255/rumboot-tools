from rumboot.testing2 import *

@RTest()
class UBootHelloWorldTest(UBootTestBase):
    def run(self):
        super().run()

        return len(self.terminal.shell_cmd("version")) >= 1


# standard epilog
if __name__ == "__main__":
    RumbootStartTesting()
