from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import os
import unittest
import nose
import numpy as np
from numpy.testing import (assert_equal, assert_almost_equal, assert_allclose)

from pims_nd2 import ND2_Reader

path, _ = os.path.split(os.path.abspath(__file__))


def assert_image_equal(actual, expected):
    if np.issubdtype(actual.dtype, np.integer):
        assert_equal(actual, expected)
    else:
        if np.issubdtype(expected.dtype, np.integer):
            expected = expected/float(np.iinfo(expected.dtype).max)
        assert_allclose(actual, expected, atol=1/256.)


class _image_single(object):
    def check_skip(self):
        pass

    def test_bool(self):
        self.check_skip()
        pass

    def test_integer_attributes(self):
        self.check_skip()
        assert_equal(len(self.v.frame_shape), len(self.expected_shape))
        self.assertTrue(isinstance(self.v.frame_shape[0], six.integer_types))
        self.assertTrue(isinstance(self.v.frame_shape[1], six.integer_types))
        self.assertTrue(isinstance(len(self.v), six.integer_types))

    def test_shape(self):
        self.check_skip()
        assert_equal(self.v.frame_shape, self.expected_shape)

    def test_count(self):
        self.check_skip()
        assert_equal(len(self.v), self.expected_len)

    def test_repr(self):
        self.check_skip()
        # simple smoke test, values not checked
        repr(self.v)


class _image_series(_image_single):
    def test_iterator(self):
        self.check_skip()
        iter(self.v)

    def test_getting_slice(self):
        self.check_skip()
        tmp = list(self.v[0:2])
        frame0, frame1 = tmp

    def test_getting_single_frame(self):
        self.v[0]
        self.v[0]
        self.v[1]
        self.v[1]

    def test_getting_list(self):
        self.check_skip()
        list(self.v[[1, 0, 0, 1, 1]])

    def test_frame_number_present(self):
        self.check_skip()
        for frame_no in [0, 1, 2, 1]:
            self.assertTrue(hasattr(self.v[frame_no], 'frame_no'))
            not_none = self.v[frame_no].frame_no is not None
            self.assertTrue(not_none)

    def test_frame_number_accurate(self):
        self.check_skip()
        for frame_no in [0, 1, 2, 1]:
            self.assertEqual(self.v[frame_no].frame_no, frame_no)

    def test_simple_negative_index(self):
        self.check_skip()
        self.v[-1]
        list(self.v[[0, -1]])


class _image_stack(object):
    def check_skip(self):
        pass

    def test_getting_stack(self):
        self.check_skip()
        assert_equal(self.v[0].shape[-3], self.expected_Z)

    def test_sizeZ(self):
        self.check_skip()
        assert_equal(self.v.sizes['z'], self.expected_Z)


class _image_multichannel(object):
    def check_skip(self):
        pass

    def test_change_channel(self):
        self.check_skip()
        self.v.bundle_axes = 'cyx'
        channel0, channel1 = self.v[0][0], self.v[0][1]
        self.v.bundle_axes = 'yx'
        self.v.default_coords['c'] = 0
        assert_image_equal(self.v[0], channel0)
        self.v.default_coords['c'] = 1
        assert_image_equal(self.v[0], channel1)

    def test_sizeC(self):
        self.check_skip()
        assert_equal(self.v.sizes['c'], self.expected_C)


class TestND2(_image_series, _image_stack, _image_multichannel,
              unittest.TestCase):
    # Nikon NIS-Elements ND2
    # 38 x 31 pixels, 16 bits, 2 channels, 3 time points, 10 focal planes
    def setUp(self):
        self.filename = os.path.join(path, 'cluster.nd2')
        self.klass = ND2_Reader
        self.kwargs = {}
        self.v = self.klass(self.filename, **self.kwargs)
        self.expected_shape = (10, 31, 38)
        self.expected_len = 3
        self.expected_Z = 10
        self.expected_C = 2

    def test_metadata(self):
        assert_equal(self.v.metadata['plane_count'], 2)
        assert_equal(self.v.metadata['plane_0']['name'], '5-FAM/pH 9.0')
        assert_almost_equal(self.v.calibration, 0.167808983)
        assert_allclose(self.v.colors[0], [0.47, 0.91, 0.06], atol=0.01)

    def test_metadata_framewise(self):
        self.v.bundle_axes = 'yx'
        frame = self.v[0]
        assert_almost_equal(frame.metadata['t_ms'], 445.08349828)
        assert_equal(frame.metadata['t'], 0)

    def tearDown(self):
        self.v.close()

if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs'],
                   exit=False)
