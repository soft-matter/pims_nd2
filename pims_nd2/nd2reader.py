from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
from pims.frame import Frame
from pims.base_frames import FramesSequenceND
import os
from . import ND2SDK as h
from ctypes import c_uint8, c_uint16, c_float


class ND2_Reader(FramesSequenceND):
    """Reads multidimensional image data from the frames of a file produced by
    Nikon NIS Elements software into an iterable object that returns images as
    numpy arrays.
    The axes inside the numpy array (czyx, zyx, cyx or yx) depend on the
    value of `bundle_axes`. It defaults to zyx or yx.

    The iteration axis depends on `iter_axes`. It defaults to t.

    It is recommended to work with a context manager (see Examples)

    Parameters
    ----------
    filename: str
    series: int, optional
        Active image series index, defaults to 0. Changeable via the `series`
        property.
    channel: int, optional
        Default channel

    Attributes
    ----------
    axes : list of strings
        List of all available axes
    ndim : int
        Number of image axes
    sizes : dict of int
        Dictionary with all axis sizes
    frame_shape : tuple of int
        Shape of frames that will be returned by get_frame
    iter_axes : iterable of strings
        This determines which axes will be iterated over by the FramesSequence.
        The last element in will iterate fastest. x and y are not allowed.
    bundle_axes : iterable of strings
        This determines which axes will be bundled into one Frame. The axes in
        the ndarray that is returned by get_frame have the same order as the
        order in this list. The last two elements have to be ['y', 'x'].
        Defaults to ['z', 'y', 'x'], when 'z' is available.
    default_coords: dict of int
        When a dimension is not present in both iter_axes and bundle_axes, the
        coordinate contained in this dictionary will be used.
    metadata : dict
        Dictionary of various metadata fields
    metadata_text : string
        Raw metadata multiline string
    pixel_type : numpy.dtype
        numpy datatype of pixels
    colors : list of rgb values (floats)
        The rgb values of all channels.
    calibration : float
        The pixel size in microns per pixel, in x, y direction
    calibrationZ : float
        The pixel size in microns per pixel, in z direction

    Methods
    ----------
    close() :
        Closes the reader, necessary if context manager is not used.

    Examples
    ----------
    >>> with ND2_reader(filename) as im:
    ...     tp.locate(im[0], diameter=7)
    """
    @classmethod
    def class_exts(cls):
        return {'.nd2'}

    class_priority = 20

    def __init__(self, filename, series=0, channel=0):
        if not os.path.isfile(filename):
            raise IOError('The file "{}" does not exist.'.format(filename))
        self.filename = str(filename)
        try:
            handle = h.Lim_FileOpenForRead(os.path.abspath(self.filename))
            self._handle = handle

            # obtain image attributes
            attr = h.LIMATTRIBUTES()
            h.Lim_FileGetAttributes(handle, attr)
            self._init_axis('x', attr.uiWidth)
            self._init_axis('y', attr.uiHeight)
            if attr.uiComp > 1:
                self._init_axis('c', attr.uiComp)
                self._lim_frame_shape = (self.sizes['y'], self.sizes['x'],
                                         self.sizes['c'])
            else:
                self._lim_frame_shape = (self.sizes['y'], self.sizes['x'])
            self._pixel_size = attr.uiBpcInMemory
            self._pixel_type = {8: np.uint8,
                                16: np.uint16,
                                32: np.float32}[self._pixel_size]
            self._pixel_type_C = {8: c_uint8,
                                  16: c_uint16,
                                  32: c_float}[self._pixel_size]
            self.max_value = 2**attr.uiBpcSignificant - 1
            self._lim_attributes = attr

            # obtain extra dimension sizes
            dims = h.LIMEXPERIMENT()
            h.Lim_FileGetExperiment(handle, dims)
            self._z_home = None
            for i in range(dims.uiLevelCount):
                dim = dims.pAllocatedLevels[i]
                dimtype = h.LIMLOOP[dim.uiExpType]
                if dimtype == 'LIMLOOP_TIME':
                    self._init_axis('t', dim.uiLoopSize)
                elif dimtype == 'LIMLOOP_MULTIPOINT':
                    self._init_axis('m', dim.uiLoopSize)
                    self.default_coords['m'] = series
                elif dimtype == 'LIMLOOP_Z':
                    self._init_axis('z', dim.uiLoopSize)
                    self.calibrationZ = dim.dInterval
                    self._z_home = h.Lim_GetZStackHome(self._handle)
                elif dimtype == 'LIMLOOP_OTHER':
                    self._init_axis('o', dim.uiLoopSize)
            self._lim_experiment = dims

            # get metadata
            bufmd = h.LIMMETADATA_DESC()
            h.Lim_FileGetMetadata(self._handle, bufmd)
            if bufmd.dAspect != 1.:
                raise RuntimeError('Non-square pixels are not supported.')
            self._lim_metadata_desc = bufmd
            self.calibration = bufmd.dCalibration
            self.colors = [None] * bufmd.uiPlaneCount
            for i in range(len(self.colors)):
                plane = bufmd.pPlanes[i]
                self.colors[i] = h.rgb_int_to_float_tuple(plane.uiColorRGB)

            # initialize read buffers
            self._buf_p = h.LIMPICTURE()
            self._buf_p_size = h.Lim_InitPicture(self._buf_p,
                                                 attr.uiWidth,
                                                 attr.uiHeight,
                                                 self._pixel_size,
                                                 attr.uiComp)
            arr_size = attr.uiWidth * attr.uiHeight * attr.uiComp
            arr = self._pixel_type_C * arr_size
            self._buf_p_a = arr.from_address(self._buf_p.pImageData)
            self._buf_md = h.LIMLOCALMETADATA()

            if 'z' in self.axes:
                self.bundle_axes = 'zyx'
            if 't' in self.axes:
                self.iter_axes = 't'
            if 'c' in self.axes:
                self.default_coords['c'] = channel

        except Exception as e:
            h.Lim_FileClose(self._handle)
            self._handle = None
            raise e

    def close(self):
        if self._handle:
            h.Lim_DestroyPicture(self._buf_p)
            h.Lim_FileClose(self._handle)
            self._handle = None

    def __del__(self):
        self.close()

    def get_frame_2D(self, **coords):
        if self._handle is None:
            raise IOError('File is closed, unable to read data')

        _coords = {'t': 0, 'c': 0, 'z': 0, 'o': 0, 'm': 0}
        _coords.update(coords)
        i = h.Lim_GetSeqIndexFromCoords(self._lim_experiment,
                                        h.LIMUINT_4(int(_coords['t']),
                                                    int(_coords['m']),
                                                    int(_coords['z']),
                                                    int(_coords['o'])))

        h.Lim_FileGetImageData(self._handle, i, self._buf_p, self._buf_md)
        im = np.ndarray(self._lim_frame_shape, self.pixel_type,
                        self._buf_p_a).copy()

        if im.ndim == 3:
            im = im[:, :, _coords['c']]

        metadata = {'x_um': self._buf_md.dXPos,
                    'y_um': self._buf_md.dYPos,
                    'z_um': self._buf_md.dZPos,
                    't_ms': self._buf_md.dTimeMSec,
                    'colors': self.colors,
                    'mpp': self.calibration,
                    'max_value': self.max_value}
        if hasattr(self, 'calibrationZ'):
            metadata['mppZ'] = self.calibrationZ
        metadata.update(coords)
        return Frame(im, metadata=metadata)

    @property
    def metadata(self):
        bufmd = self._lim_metadata_desc
        attr = self._lim_attributes

        metadata = {'width': attr.uiWidth,
                    'width_bytes': attr.uiWidthBytes,
                    'height': attr.uiHeight,
                    'components': attr.uiComp,
                    'bitsize_memory': attr.uiBpcInMemory,
                    'bitsize_significant': attr.uiBpcSignificant,
                    'sequence_count': attr.uiSequenceCount,
                    'tile_width': attr.uiTileWidth,
                    'tile_height': attr.uiTileHeight,
                    'compression': h.compression_type[attr.uiCompression],
                    'compression_quality': attr.uiQuality,  # 0 (worst) - 100 (best)

                    'plane_count': bufmd.uiPlaneCount,
                    'angle': bufmd.dAngle,
                    'calibration_um': bufmd.dCalibration,
                    'time_start': h.jdn_to_datetime_local(bufmd.dTimeStart),
                    'time_start_utc': h.jdn_to_datetime_utc(bufmd.dTimeStart),
                    'objective': bufmd.wszObjectiveName,
                    'magnification': bufmd.dObjectiveMag,
                    'NA': bufmd.dObjectiveNA,
                    'refractive_index1': bufmd.dRefractIndex1,
                    'refractive_index2': bufmd.dRefractIndex2,
                    'pinhole': bufmd.dPinholeRadius,
                    'zoom': bufmd.dZoom,
                    'projective_mag': bufmd.dProjectiveMag,
                    'image_type': h.image_type[bufmd.uiImageType],

                    'z_home': self._z_home}
        for i in range(bufmd.uiPlaneCount):
            plane = bufmd.pPlanes[i]
            metadata['plane_{}'.format(i)] = {'components': plane.uiCompCount,
                                              'rgb_value': h.rgb_int_to_float_tuple(plane.uiColorRGB),
                                              'name': plane.wszName,
                                              'oc': plane.wszOCName,
                                              'emission_nm': plane.dEmissionWL}

        return metadata

    @property
    def metadata_text(self):
        if hasattr(self, '_lim_textinfo'):
            buft = self._lim_textinfo
        else:
            buft = h.LIMTEXTINFO()
            h.Lim_FileGetTextinfo(self._handle, buft)
            self._lim_textinfo = buft
        return buft.wszDescription  # wszCapturing is contained in Description

    @property
    def pixel_type(self):
        return self._pixel_type
