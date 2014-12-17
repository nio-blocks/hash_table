from collections import defaultdict
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
    key = ExpressionProperty(
        title='Key', default="{{$key}}", attr_default=AttributeError)
    value = ExpressionProperty(
        title='Value', default="{{$value}}", attr_default=AttributeError)

    def process_signals(self, signals):
        hash_dict = defaultdict(list)

        for signal in signals:
            try:
                sig_key = self.key(signal)
                sig_value = self.value(signal)
            except AttributeError:
                # If we don't have the value on the signal, don't add it to the
                # hash table
                continue

            # Append sig_value to the proper hash key
            hash_dict[sig_key].append(sig_value)

        if len(hash_dict):
            self.notify_signals([Signal(hash_dict)])
