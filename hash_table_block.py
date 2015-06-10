from collections import defaultdict
from nio.common.block.base import Block
from nio.common.signal.base import Signal
from .mixins.group_by.group_by_block import GroupBy
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import ExpressionProperty, StringProperty, \
    BoolProperty, VersionProperty


@Discoverable(DiscoverableType.block)
class HashTable(GroupBy, Block):

    """ HashTable block.

    Group a list of signals into one hash table signal.
    The output signal will contain an attribute for each
    evaluated *key* and the value of that attribute will
    be a list with an item of *value* for each matching signal.

    If *one_value* is True, the Signal attributes will be just a
    single matching value instead of a list of all matching values.
    If multiple matches, then the last signal processed will be the
    value used.

    """
    key = ExpressionProperty(
        title='Key', default="{{ $key }}", attr_default=AttributeError)
    value = ExpressionProperty(
        title='Value', default="{{ $value }}", attr_default=AttributeError)
    group_attr = StringProperty(
        title="Group Attribute Name", default="group", visible=False)
    one_value = BoolProperty(title="One Value Per Key", default=False)
    version = VersionProperty('0.1.0')

    def process_signals(self, signals, input_id='default'):
        self.for_each_group(self._get_hash_from_group, signals)

    def notify_signal(self, signal):
        """ Notifies one signal, if it exists """
        if signal:
            self.notify_signals([signal])

    def _get_hash_from_group(self, signals, group):
        self._logger.debug("Processing group {} of {} signals".format(
            group, len(signals)))
        out_sig = self._perform_hash(signals)
        if out_sig:
            setattr(out_sig, self.group_attr, group)
            self.notify_signal(out_sig)

    def _perform_hash(self, signals):
        hash_dict = defaultdict(None) if self.one_value else defaultdict(list)

        for signal in signals:
            try:
                sig_key = self.key(signal)
                sig_value = self.value(signal)
            except AttributeError:
                # If we don't have the value on the signal, don't add it to the
                # hash table
                continue
            except Exception as e:
                self._logger.warning("Failed to evaluate props: {}".format(e))

            # Add sig_value to the proper hash key
            try:
                if sig_key is not None:
                    if self.one_value:
                        hash_dict[sig_key] = sig_value
                    else:
                        hash_dict[sig_key].append(sig_value)
                else:
                    self._logger.debug("Skipping key: {}".format(sig_key))
            except Exception as e:
                self._logger.warning(
                    "Failed to add value {} to key {}: {}".format(
                        sig_value, sig_key, e))

        if len(hash_dict):
            return Signal(hash_dict)
