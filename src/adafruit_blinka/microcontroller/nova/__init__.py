class Connection:
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Connection.__instance is not None:
            raise Exception("This class is a singleton!")

        from binhoHostAdapter import binhoHostAdapter
        from binhoHostAdapter import binhoUtilities

        utilities = binhoUtilities.binhoUtilities()
        devices = utilities.listAvailableDevices()

        if len(devices) > 0:
            Connection.__instance = binhoHostAdapter.binhoHostAdapter(devices[0])
        else:
            raise RuntimeError('No Binho Nova found!')
