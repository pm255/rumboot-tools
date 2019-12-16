class chipBase:
    name="name"
    part="part"
    chip_id=0
    chip_rev=0
    baudrate=115200
    warning=None

class chipMM7705:
    name="mm7705"
    part="1888ТХ018"
    chip_id=1
    chip_rev=1
    warning='''
    This chip has a RumBoot V1 bootloader. 
    RumBootV2 may be flashed onto SPI flash and executed from internal memory
    to provide additional functionality, e.g. xmodem loading
    '''
    welcome='host'
    baudrate=1000000
    memories = {
        "spi" : "rumboot-mm7705-PostProduction-updater-spiflash.bin"
    }

class chipBasis:
    name="basis"
    part="1888ВС048"
    chip_id=3
    chip_rev=1
    welcome='host'
    baudrate=115200
    memories = {
        "i2c0-0x50": "rumboot-basis-PostProduction-updater-i2c0-0x50.bin",
        "i2c0-0x51": "rumboot-basis-PostProduction-updater-i2c0-0x51.bin", 
        "i2c0-0x52": "rumboot-basis-PostProduction-updater-i2c0-0x52.bin", 
        "i2c0-0x53": "rumboot-basis-PostProduction-updater-i2c0-0x53.bin",
        "spi0-gpio0_5-cs": "rumboot-basis-PostProduction-updater-spi0-gpio0_5-cs.bin",
        "spi0-internal-cs": "rumboot-basis-PostProduction-updater-spi0-internal-cs.bin",
        "spi1-internal-cs": "rumboot-basis-PostProduction-updater-spi1-internal-cs.bin",
    }

class chipOI10:
    name="oi10"
    part="1888ВМ018(A)/1888ВМ01H4"
    chip_id=4
    chip_rev=1
    welcome='host'
    baudrate=115200
    memories = {
        "spi0-internal-cs": "rumboot-oi10-PostProduction-updater-spi-flash-0.bin",
        "nor":  "rumboot-oi10-PostProduction-updater-nor-mt150.04.bin",
        "nor-bootrom":  "rumboot-oi10-PostProduction-updater-nor-mt150.04-brom.bin"
    }

class chipBBP3:
    name="bbp3"
    part="1888ВС058"
    chip_id=5
    baudrate=115200
    chip_rev=1
    welcome='host'
    baudrate=115200
    memories = {
        "spi0-cs0": "rumboot-bbp3-PostProduction-updater-spi0-cs0.bin",
    }

class chipNM6408:
    name="nm6408"
    part="1888ВС058"
    chip_id=6
    chip_rev=1
    welcome='host'
    baudrate=115200
    warning='''
    This chip has a legacy ROM bootloader. 
    RumBoot is flashed onto SPI flash and executed from internal memory
    to provide additional functionality
    Please be careful not wipe it! Recovery will be only possible via JTAG
    '''
    memories = {
        "spi0-cs0": "rumboot-nm6408-PostProduction-updater-spi0-cs0.bin",
    }

class chipZynq:
    name="zed"
    part="Xilinx Zynq series (Zed Board, Tang Hex, ...)"
    chip_id=255
    baudrate=115200
    chip_rev=1
    welcome='Zynq> '
    baudrate=115200
    memories = {}

class chipRPI4:
    name="rpi4"
    part="BCM2711 (Raspberry Pi 4)"
    chip_id=255
    baudrate=115200
    chip_rev=2
    welcome='U-Boot> '
    baudrate=115200
    memories = {}

class chipDb:
    chips = {chipMM7705, chipBasis,chipOI10, chipBBP3, chipNM6408, chipZynq, chipRPI4}
    
    def query(self, id, rev):
        for c in self.chips:
            if c.chip_id == id and c.chip_rev == rev:
                return c
        return None
    