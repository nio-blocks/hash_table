from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.expression import ExpressionProperty


@Discoverable(DiscoverableType.block)
class HashTable(Block):
    """ HashTable block.

    Group a list of signals into one hash table signal.
    The output signal will contain an attribute for each
    evaluated *key* and the value of that attribute will
    be a list with an item of *value* for each matching signal.

    """
    key = ExpressionProperty(title='Key', default="{{$key}}")
    value = ExpressionProperty(title='Value', default="{{$value}}")

    def process_signals(self, signals):
        hash_dict = {}
        for signal in signals:
            sig_key = self.key(signal)
            sig_value = self.value(signal)
            if not sig_value:
                continue
            list = hash_dict.get(sig_key, [])
            list.append(sig_value)
            hash_dict[sig_key] = list
        if hash_dict:
            self.notify_signals([Signal(hash_dict)])

