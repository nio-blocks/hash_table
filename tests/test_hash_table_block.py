from unittest.mock import patch
from ..hash_table_block import HashTable
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.common.signal.base import Signal


class FlavorSignal(Signal):
    def __init__(self, flavor, size=None):
        self.flavor = flavor
        self.size = size

class KeyValueSignal(Signal):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class TestHashTable(NIOBlockTestCase):

    def __init__(self, methodName='runTests'):
        super().__init__(methodName)
        self.notified_signals = []

    def signals_notified(self, signals):
        self.notified_signals = signals

    def test_hash(self):
        signals = [FlavorSignal('cherry'),
                   FlavorSignal('cherry', 'S'),
                   FlavorSignal('cherry', 'M'),
                   FlavorSignal('cherry', 'L'),
                   FlavorSignal('banana', 'S'),
                   FlavorSignal('apple', 'S')]
        blk = HashTable()
        config = {
            "key": "{{$flavor}}",
            "value": "{{$size}}",
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(1, blk)
        self.assertEqual(['S','M','L'], self.notified_signals[0].cherry)
        self.assertEqual(['S'], self.notified_signals[0].banana)
        self.assertEqual(['S'], self.notified_signals[0].apple)
        blk.stop()

    def test_defaults(self):
        signals = [KeyValueSignal('cherry', 'S'),
                   KeyValueSignal('cherry', 'M'),
                   KeyValueSignal('cherry', 'L'),
                   KeyValueSignal('banana', 'S'),
                   KeyValueSignal('apple', 'S'),
                   FlavorSignal('bad')]
        blk = HashTable()
        config = {
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(1, blk)
        self.assertEqual(['S','M','L'], self.notified_signals[0].cherry)
        self.assertEqual(['S'], self.notified_signals[0].banana)
        self.assertEqual(['S'], self.notified_signals[0].apple)
        self.assertEqual(['{{$value}}'], getattr(self.notified_signals[0], "{{$key}}"))
        blk.stop()
