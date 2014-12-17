from ..hash_table_block import HashTable
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase


class TestHashTable(NIOBlockTestCase):

    def __init__(self, methodName='runTests'):
        super().__init__(methodName)
        self.notified_signals = []

    def signals_notified(self, signals):
        print(signals)
        self.notified_signals = signals

    def test_hash(self):
        signals = [{'flavor': 'cherry'},
                   {'flavor': 'cherry', 'size': 'S'},
                   {'flavor': 'cherry', 'size': 'M'},
                   {'flavor': 'cherry', 'size': 'L'},
                   {'flavor': 'banana', 'size': 'S'},
                   {'flavor': 'apple', 'size': 'S'}]
        blk = HashTable()
        config = {
            "key": "{{$flavor}}",
            "value": "{{$size}}",
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal(s) for s in signals])
        self.assert_num_signals_notified(1, blk)
        self.assertEqual(['S', 'M', 'L'], self.notified_signals[0].cherry)
        self.assertEqual(['S'], self.notified_signals[0].banana)
        self.assertEqual(['S'], self.notified_signals[0].apple)
        blk.stop()

    def test_defaults(self):
        signals = [{'key': 'cherry', 'value': 'S'},
                   {'key': 'cherry', 'value': 'M'},
                   {'key': 'cherry', 'value': 'L'},
                   {'key': 'banana', 'value': 'S'},
                   {'key': 'apple', 'value': 'S'},
                   {'flavor': 'bad'}]
        blk = HashTable()
        config = {
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal(s) for s in signals])
        self.assert_num_signals_notified(1, blk)
        self.assertEqual(['S', 'M', 'L'], self.notified_signals[0].cherry)
        self.assertEqual(['S'], self.notified_signals[0].banana)
        self.assertEqual(['S'], self.notified_signals[0].apple)
        self.assertEqual(
            ['{{$value}}'], getattr(self.notified_signals[0], "{{$key}}"))
        blk.stop()
