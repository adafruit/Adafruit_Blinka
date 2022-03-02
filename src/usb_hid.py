from typing import Sequence
from pathlib import Path
import os
import atexit

# https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt

gadget_root = '/sys/kernel/config/usb_gadget/adafruit-blinka'


class Device():
    def __init__(self, *, descriptor: bytes, usage_page: int, usage: int, report_ids: Sequence[int],
                 in_report_lengths: Sequence[int], out_report_lengths: Sequence[int]) -> None:
        self.out_report_lengths = out_report_lengths
        self.in_report_lengths = in_report_lengths
        self.report_ids = report_ids
        self.usage = usage
        self.usage_page = usage_page
        self.descriptor = descriptor
        self._last_received_report = None

    def send_report(self, report: bytearray, report_id: int = None):
        device_path = self.gets_device_path(report_id)
        with open(device_path, 'rb+') as fd:
            fd.write(report)

    @property
    def last_received_report(self, ):
        device_path = self.gets_device_path(self.report_ids[0])
        with open(device_path, 'rb+') as fd:
            os.set_blocking(fd.fileno(), False)
            report = fd.read(self.out_report_lengths[0])
            if report is not None:
                self._last_received_report = report
        return self._last_received_report

    def gets_device_path(self, report_id):
        device = \
            Path('%s/functions/hid.usb%s/dev' % (gadget_root, report_id or self.report_ids[0])) \
                .read_text() \
                .strip() \
                .split(':')[1]
        device_path = '/dev/hidg%s' % device
        return device_path


Device.KEYBOARD = Device(
    descriptor=bytes((

        0x05, 0x01,  # usage page (generic desktop ctrls)
        0x09, 0x06,  # usage (keyboard)
        0xa1, 0x01,  # collection (application)
        0x05, 0x07,  # usage page (kbrd/keypad)
        0x19, 0xe0,  # usage minimum (0xe0)
        0x29, 0xe7,  # usage maximum (0xe7)
        0x15, 0x00,  # logical minimum (0)
        0x25, 0x01,  # logical maximum (1)
        0x75, 0x01,  # report size (1)
        0x95, 0x08,  # report count (8)
        0x81, 0x02,  # input (data,var,abs,no wrap,linear,preferred state,no null position)
        0x95, 0x01,  # report count (1)
        0x75, 0x08,  # report size (8)
        0x81, 0x01,  # input (const,array,abs,no wrap,linear,preferred state,no null position)
        0x95, 0x03,  # report count (3)
        0x75, 0x01,  # report size (1)
        0x05, 0x08,  # usage page (leds)
        0x19, 0x01,  # usage minimum (num lock)
        0x29, 0x05,  # usage maximum (kana)
        0x91, 0x02,  # output (data,var,abs,no wrap,linear,preferred state,no null position,non-volatile)
        0x95, 0x01,  # report count (1)
        0x75, 0x05,  # report size (5)
        0x91, 0x01,  # output (const,array,abs,no wrap,linear,preferred state,no null position,non-volatile)
        0x95, 0x06,  # report count (6)
        0x75, 0x08,  # report size (8)
        0x15, 0x00,  # logical minimum (0)
        0x26, 0xff, 0x00,  # logical maximum (255)
        0x05, 0x07,  # usage page (kbrd/keypad)
        0x19, 0x00,  # usage minimum (0x00)
        0x2a, 0xff, 0x00,  # usage maximum (0xff)
        0x81, 0x00,  # input (data,array,abs,no wrap,linear,preferred state,no null position)
        0xc0,  # end collection
    )),
    usage_page=0x1,
    usage=0x6,
    report_ids=[0x1],
    in_report_lengths=[8],
    out_report_lengths=[1]
)
Device.MOUSE = Device(
    descriptor=bytes((

        0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
        0x09, 0x02,  # Usage (Mouse)
        0xA1, 0x01,  # Collection (Application)
        0x09, 0x01,  # Usage (Pointer)
        0xA1, 0x00,  # Collection (Physical)
        0x05, 0x09,  # Usage Page (Button)
        0x19, 0x01,  # Usage Minimum (0x01)
        0x29, 0x05,  # Usage Maximum (0x05)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x95, 0x05,  # Report Count (5)
        0x75, 0x01,  # Report Size (1)
        0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,  # Report Count (1)
        0x75, 0x03,  # Report Size (3)
        0x81, 0x01,  # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
        0x09, 0x30,  # Usage (X)
        0x09, 0x31,  # Usage (Y)
        0x15, 0x81,  # Logical Minimum (-127)
        0x25, 0x7F,  # Logical Maximum (127)
        0x75, 0x08,  # Report Size (8)
        0x95, 0x02,  # Report Count (2)
        0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        0x09, 0x38,  # Usage (Wheel)
        0x15, 0x81,  # Logical Minimum (-127)
        0x25, 0x7F,  # Logical Maximum (127)
        0x75, 0x08,  # Report Size (8)
        0x95, 0x01,  # Report Count (1)
        0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,  # End Collection
        0xC0,  # End Collection
    )),
    # Omitted for brevity.
    usage_page=0x1,
    usage=0x02,
    report_ids=[2],
    in_report_lengths=[4],
    out_report_lengths=[0],
)

Device.CONSUMER_CONTROL = Device(
    descriptor=bytes((
        0x05, 0x0C,  # Usage Page (Consumer)
        0x09, 0x01,  # Usage (Consumer Control)
        0xA1, 0x01,  # Collection (Application)
        0x75, 0x10,  # Report Size (16)
        0x95, 0x01,  # Report Count (1)
        0x15, 0x01,  # Logical Minimum (1)
        0x26, 0x8C, 0x02,  # Logical Maximum (652)
        0x19, 0x01,  # Usage Minimum (Consumer Control)
        0x2A, 0x8C, 0x02,  # Usage Maximum (AC Send)
        0x81, 0x00,  # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,  # End Collection
    )),
    # Omitted for brevity.
    usage_page=0x0C,
    usage=0x01,
    report_ids=[3],
    in_report_lengths=[2],
    out_report_lengths=[0],
)
devices = [Device.KEYBOARD, Device.MOUSE, Device.CONSUMER_CONTROL]


def disable() -> None:
    try:
        Path('%s/UDC' % gadget_root).write_text('')
    except FileNotFoundError:
        pass
    for symlink in Path(gadget_root).glob('configs/**/hid.usb*'):
        symlink.unlink()

    for strings_file in Path(gadget_root).rglob('configs/*/strings/*/*'):
        if strings_file.is_dir():
            strings_file.rmdir()

    for strings_file in Path(gadget_root).rglob('configs/*/strings/*'):
        if strings_file.is_dir():
            strings_file.rmdir()
    for config_dir in Path(gadget_root).rglob('configs/*'):
        if config_dir.is_dir():
            config_dir.rmdir()
    for function_dir in Path(gadget_root).rglob('functions/*'):
        if function_dir.is_dir():
            function_dir.rmdir()
    try:
        Path(gadget_root).rmdir()
    except:
        pass


# atexit.register(disable)


def enable(devices: Sequence[Device], boot_device: int = 0) -> None:
    if len(devices) == 0:
        disable()
        return
    """
    1. Creating the gadgets
    -----------------------

    For each gadget to be created its corresponding directory must be created::

        $ mkdir $CONFIGFS_HOME/usb_gadget/<gadget name>

    e.g.::

        $ mkdir $CONFIGFS_HOME/usb_gadget/g1

        ...
        ...
        ...

        $ cd $CONFIGFS_HOME/usb_gadget/g1

    Each gadget needs to have its vendor id <VID> and product id <PID> specified::

        $ echo <VID> > idVendor
        $ echo <PID> > idProduct

    A gadget also needs its serial number, manufacturer and product strings.
    In order to have a place to store them, a strings subdirectory must be created
    for each language, e.g.::

        $ mkdir strings/0x409

    Then the strings can be specified::

        $ echo <serial number> > strings/0x409/serialnumber
        $ echo <manufacturer> > strings/0x409/manufacturer
        $ echo <product> > strings/0x409/product
    """
    Path('%s/functions' % gadget_root).mkdir(parents=True, exist_ok=True)
    Path('%s/configs' % gadget_root).mkdir(parents=True, exist_ok=True)
    Path('%s/bcdDevice' % gadget_root).write_text('%s' % 1)  # Version 1.0.0
    Path('%s/bcdUSB' % gadget_root).write_text('%s' % 0x0200)  # USB 2.0
    Path('%s/bDeviceClass' % gadget_root).write_text('%s' % 0x00)  # multipurpose i guess?
    Path('%s/bDeviceProtocol' % gadget_root).write_text('%s' % 0x00)
    Path('%s/bDeviceSubClass' % gadget_root).write_text('%s' % 0x00)
    Path('%s/bMaxPacketSize0' % gadget_root).write_text('%s' % 0x08)
    Path('%s/idProduct' % gadget_root).write_text('%s' % 0x0104)  # Multifunction Composite Gadget
    Path('%s/idVendor' % gadget_root).write_text('%s' % 0x1d6b)  # Linux Foundation
    """
    2. Creating the configurations
    ------------------------------

    Each gadget will consist of a number of configurations, their corresponding
    directories must be created:

    $ mkdir configs/<name>.<number>

    where <name> can be any string which is legal in a filesystem and the
    <number> is the configuration's number, e.g.::

        $ mkdir configs/c.1

        ...
        ...
        ...

    Each configuration also needs its strings, so a subdirectory must be created
    for each language, e.g.::

        $ mkdir configs/c.1/strings/0x409

    Then the configuration string can be specified::

        $ echo <configuration> > configs/c.1/strings/0x409/configuration

    Some attributes can also be set for a configuration, e.g.::

        $ echo 120 > configs/c.1/MaxPower
        """

    for i, device in enumerate(devices):

        config_root = '%s/configs/device.%s' % (gadget_root, 1)
        Path('%s/' % config_root).mkdir(parents=True, exist_ok=True)
        Path('%s/strings/0x409' % config_root).mkdir(parents=True, exist_ok=True)
        Path('%s/strings/0x409/configuration' % config_root).write_text('my configuration')
        Path('%s/MaxPower' % config_root).write_text('150')
        Path('%s/bmAttributes' % config_root).write_text('%s' % 0x080)
        """
        3. Creating the functions
        -------------------------

        The gadget will provide some functions, for each function its corresponding
        directory must be created::

            $ mkdir functions/<name>.<instance name>

        where <name> corresponds to one of allowed function names and instance name
        is an arbitrary string allowed in a filesystem, e.g.::

          $ mkdir functions/ncm.usb0 # usb_f_ncm.ko gets loaded with request_module()

          ...
          ...
          ...

        Each function provides its specific set of attributes, with either read-only
        or read-write access. Where applicable they need to be written to as
        appropriate.
        Please refer to Documentation/ABI/*/configfs-usb-gadget* for more information.

        """

        # create functions
        for report_index, report_id in enumerate(device.report_ids):
            function_root = '%s/functions/hid.usb%s' % (gadget_root, report_id)
            try:
                Path('%s/' % function_root).mkdir(parents=True)
            except FileExistsError:
                continue
            Path('%s/protocol' % function_root).write_text('%s' % report_id)
            Path('%s/report_length' % function_root).write_text('%s' % device.in_report_lengths[report_index])
            Path('%s/subclass' % function_root).write_text('%s' % 1)
            Path('%s/report_desc' % function_root).write_bytes(device.descriptor)
            """
            4. Associating the functions with their configurations
            ------------------------------------------------------

            At this moment a number of gadgets is created, each of which has a number of
            configurations specified and a number of functions available. What remains
            is specifying which function is available in which configuration (the same
            function can be used in multiple configurations). This is achieved with
            creating symbolic links::

                $ ln -s functions/<name>.<instance name> configs/<name>.<number>

            e.g.::

                $ ln -s functions/ncm.usb0 configs/c.1
            """

            Path('%s/hid.usb%s' % (config_root, report_id)).symlink_to(function_root)
    """
    5. Enabling the gadget
    ----------------------
    Such a gadget must be finally enabled so that the USB host can enumerate it.

    In order to enable the gadget it must be bound to a UDC (USB Device
    Controller)::

        $ echo <udc name> > UDC

    where <udc name> is one of those found in /sys/class/udc/*
    e.g.::

    $ echo s3c-hsotg > UDC

    """
    udc = next(Path('/sys/class/udc/').glob('*'))
    Path('%s/UDC' % gadget_root).write_text('%s' % udc.name)
