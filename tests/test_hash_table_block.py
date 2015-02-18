from ..hash_table_block import HashTable
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase


class TestHashTable(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        self.notified_signals = []

    def signals_notified(self, signals, output_id='default'):
        self.notified_signals.extend(signals)

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

        # Make sure the bad one didn't make its way into the output signal
        self.assertFalse(hasattr(self.notified_signals[0], 'flavor'))
        blk.stop()

    def test_grouping(self):
        signals = [{'group': 'fruit', 'key': 'cherry', 'value': 'S'},
                   {'group': 'fruit', 'key': 'cherry', 'value': 'M'},
                   {'group': 'fruit', 'key': 'cherry', 'value': 'L'},
                   {'group': 'pie', 'key': 'banana', 'value': 'S'},
                   {'group': 'pie', 'key': 'cherry', 'value': 'M'},
                   {'group': 'pie', 'key': 'cherry', 'value': 'L'},
                   {'group': 'fruit', 'key': 'banana', 'value': 'S'}]
        blk = HashTable()
        config = {
            'group_attr': 'my_group',
            'group_by': '{{$group}}',
            'log_level': 'DEBUG'
        }
        self.configure_block(blk, config)
        blk.process_signals([Signal(s) for s in signals])
        self.assert_num_signals_notified(2, blk)
        for sig_out in self.notified_signals:
            # Make sure the group got assigned to the right attr
            self.assertIn(sig_out.my_group, ['fruit', 'pie'])

            # Assert the right values went to the right groups
            if sig_out.my_group == 'fruit':
                self.assertEqual(len(sig_out.cherry), 3)
                self.assertEqual(len(sig_out.banana), 1)
            elif sig_out.my_group == 'pie':
                self.assertEqual(len(sig_out.cherry), 2)
                self.assertEqual(len(sig_out.banana), 1)
