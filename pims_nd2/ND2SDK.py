from ctypes import (c_int, c_wchar, c_wchar_p, c_uint, c_size_t, c_void_p,
                    c_double, cdll, Structure, sizeof, POINTER)
import os
from sys import platform
from datetime import datetime

if platform == "linux" or platform == "linux2":
    nd2 = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'ND2SDK',
                                        'linux', 'libnd2ReadSDK.so'))
elif platform == "darwin":
    nd2 = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'ND2SDK',
                                        'osx', 'nd2sdk.framework', 'Versions',
                                        '1', 'nd2sdk'))
elif platform == "win32":
    bitsize = sizeof(c_void_p) * 8
    if bitsize == 32:
       dlldir = os.path.join(os.path.dirname(__file__), 'ND2SDK', 'win', 'x86')
    elif bitsize == 64:
       dlldir = os.path.join(os.path.dirname(__file__), 'ND2SDK', 'win', 'x64')
    else:
       raise OSError("The bitsize does not equal 32 or 64.")
    nd2 = cdll.LoadLibrary(os.path.join(dlldir, 'v6_w32_nd2ReadSDK.dll'))


def jdn_to_datetime_local(jdn):
    return datetime.fromtimestamp((jdn - 2440587.5) * 86400.)


def jdn_to_datetime_utc(jdn):
    return datetime.utcfromtimestamp((jdn - 2440587.5) * 86400.)


LIMFILEHANDLE = c_int
LIMWCHAR = c_wchar
LIMWSTR = c_wchar_p
LIMCWSTR = c_wchar_p  # should be constant str
LIMUINT = c_uint
LIMUINT_4 = LIMUINT * 4
LIMSIZE = c_size_t
LIMINT = c_int
LIMBOOL = c_int
LIMMAXBINARIES = 128
LIMMAXPICTUREPLANES = 256

LIMLOOP = {0: 'LIMLOOP_TIME',
           1: 'LIMLOOP_MULTIPOINT',
           2: 'LIMLOOP_Z',
           3: 'LIMLOOP_OTHER'}

LIMMAXEXPERIMENTLEVEL = 8
LIMSTRETCH_QUICK = 1
LIMSTRETCH_SPLINES = 2
LIMSTRETCH_LINEAR = 3

LIM_ERR = {0:  'LIM_OK',
           -1:  'LIM_ERR_UNEXPECTED',
           -2:  'LIM_ERR_NOTIMPL',
           -3:  'LIM_ERR_OUTOFMEMORY',
           -4:  'LIM_ERR_INVALIDARG',
           -5:  'LIM_ERR_NOINTERFACE',
           -6:  'LIM_ERR_POINTER',
           -7:  'LIM_ERR_HANDLE',
           -8:  'LIM_ERR_ABORT',
           -9:  'LIM_ERR_FAIL',
           -10: 'LIM_ERR_ACCESSDENIED',
           -11: 'LIM_ERR_OS_FAIL',
           -12: 'LIM_ERR_NOTINITIALIZED',
           -13: 'LIM_ERR_NOTFOUND',
           -14: 'LIM_ERR_IMPL_FAILED',
           -15: 'LIM_ERR_DLG_CANCELED',
           -16: 'LIM_ERR_DB_PROC_FAILED',
           -17: 'LIM_ERR_OUTOFRANGE',
           -18: 'LIM_ERR_PRIVILEGES',
           -19: 'LIM_ERR_VERSION'}

image_type = {0: 'normal', 1: 'spectral'}
compression_type = {0: 'lossless', 1: 'lossy', 2: None}


def rgb_int_to_float_tuple(rgb):
    return ((rgb & 255) / 255.,
            (rgb >> 8 & 255) / 255.,
            (rgb >> 16 & 255) / 255.)


def LIMRESULT(result):
    if result != 0:
        error = LIM_ERR[result]
        raise Exception(error)
    return True


class LIMPICTURE(Structure):
    _fields_ = [("uiWidth", LIMUINT),
                ("uiHeight", LIMUINT),
                ("uiBitsPerComp", LIMUINT),
                ("uiComponents", LIMUINT),
                ("uiWidthBytes", LIMUINT),
                ("uiSize", LIMSIZE),
                ("pImageData", c_void_p)]


class LIMBINARYDESCRIPTOR(Structure):
    _fields_ = [("wszName", LIMWCHAR*256),
                ("wszCompName", LIMWCHAR*256),
                ("uiColorRGB", LIMUINT)]


class LIMBINARIES(Structure):
    _fields_ = [("uiCount", LIMUINT),
                ("pDescriptors", LIMBINARYDESCRIPTOR*LIMMAXBINARIES)]


class LIMATTRIBUTES(Structure):
    _fields_ = [("uiWidth", LIMUINT),  # Width of images
                ("uiWidthBytes", LIMUINT),  # Line length 4-byte aligned
                ("uiHeight", LIMUINT),  # Height if images
                ("uiComp", LIMUINT),  # Number of components
                ("uiBpcInMemory", LIMUINT),  # Bits per component 8, 16 or 32 (for float image)
                ("uiBpcSignificant", LIMUINT),  # Bits per component used 8 .. 16 or 32 (for float image)
                ("uiSequenceCount", LIMUINT),  # Number of images in the sequence
                ("uiTileWidth", LIMUINT),  # If an image is tiled size of the tile/strip 
                ("uiTileHeight", LIMUINT),  # otherwise both zero 
                ("uiCompression", LIMUINT),  # 0 (lossless), 1 (lossy), 2 (None)
                ("uiQuality", LIMUINT)]  # 0 (worst) - 100 (best)

class LIMFILEUSEREVENT(Structure):
    _fields_ = [("uiID", LIMUINT),
                ("dTime", c_double),
                ("wsType", LIMWCHAR * 128),
                ("wsDescription", LIMWCHAR * 256)]


class LIMPICTUREPLANE_DESC(Structure):
    _fields_ = [("uiCompCount", LIMUINT), # Number of physical components
                ("uiColorRGB", LIMUINT), # RGB color for display
                ("wszName", LIMWCHAR * 256), # Name for display
                ("wszOCName", LIMWCHAR * 256), # Name of the Optical Configuration
                ("dEmissionWL", c_double)]


class LIMMETADATA_DESC(Structure):
    _fields_ = [("dTimeStart", c_double), # Absolute Time in JDN
                ("dAngle", c_double), # Camera Angle
                ("dCalibration", c_double), #um/px (0.0 = uncalibrated)
                ("dAspect", c_double), # pixel aspect (always 1.0)
                ("wszObjectiveName", LIMWCHAR * 256),
                ("dObjectiveMag", c_double), # Optional additional information
                ("dObjectiveNA", c_double), # dCalibration takes into accont all these
                ("dRefractIndex1", c_double),
                ("dRefractIndex2", c_double),
                ("dPinholeRadius", c_double),
                ("dZoom", c_double),
                ("dProjectiveMag", c_double),
                ("uiImageType", LIMUINT), # 0 (normal), 1 (spectral)
                ("uiPlaneCount", LIMUINT), # Number of logical planes (uiPlaneCount <= uiComponentCount)
                ("uiComponentCount", LIMUINT), # Number of physical components (same as uiComp in LIMFILEATTRIBUTES)
                ("pPlanes", LIMPICTUREPLANE_DESC * LIMMAXPICTUREPLANES)]


class LIMTEXTINFO(Structure):
    _fields_ = [("wszImageID", LIMWCHAR * 256),
                ("wszType", LIMWCHAR * 256),
                ("wszGroup", LIMWCHAR * 256),
                ("wszSampleID", LIMWCHAR * 256),
                ("wszAuthor", LIMWCHAR * 256),
                ("wszDescription", LIMWCHAR * 4096),
                ("wszCapturing", LIMWCHAR * 4096),
                ("wszSampling", LIMWCHAR * 256),
                ("wszLocation", LIMWCHAR * 256),
                ("wszDate", LIMWCHAR * 256),
                ("wszConclusion", LIMWCHAR * 256),
                ("wszInfo1", LIMWCHAR * 256),
                ("wszInfo2", LIMWCHAR * 256),
                ("wszOptics", LIMWCHAR * 256)]


class LIMEXPERIMENTLEVEL(Structure):
    _fields_ = [("uiExpType", LIMUINT),  # see LIMLOOP_TIME etc.
                ("uiLoopSize", LIMUINT),  # Number of images in the loop
                ("dInterval", c_double)]  # ms (for Time), um (for ZStack), -1.0 (for Multipoint)


class LIMEXPERIMENT(Structure):
    _fields_ = [("uiLevelCount", LIMUINT),
                ("pAllocatedLevels", LIMEXPERIMENTLEVEL*LIMMAXEXPERIMENTLEVEL)]


class LIMLOCALMETADATA(Structure):
    _fields_ = [("dTimeMSec", c_double),
                ("dXPos", c_double),
                ("dYPos", c_double),
                ("dZPos", c_double)]


Lim_FileOpenForRead = nd2.Lim_FileOpenForRead
Lim_FileOpenForRead.argtypes = [LIMCWSTR]
Lim_FileOpenForRead.restype = LIMFILEHANDLE

Lim_FileGetAttributes = nd2.Lim_FileGetAttributes
Lim_FileGetAttributes.argtypes = [LIMFILEHANDLE, POINTER(LIMATTRIBUTES)]
Lim_FileGetAttributes.restype = LIMRESULT

Lim_FileGetMetadata = nd2.Lim_FileGetMetadata
Lim_FileGetMetadata.argtypes = [LIMFILEHANDLE, POINTER(LIMMETADATA_DESC)]
Lim_FileGetMetadata.restype = LIMRESULT

Lim_FileGetTextinfo = nd2.Lim_FileGetTextinfo
Lim_FileGetTextinfo.argtypes = [LIMFILEHANDLE, POINTER(LIMTEXTINFO)]
Lim_FileGetTextinfo.restype = LIMRESULT

Lim_FileGetExperiment = nd2.Lim_FileGetExperiment
Lim_FileGetExperiment.argtypes = [LIMFILEHANDLE, POINTER(LIMEXPERIMENT)]
Lim_FileGetExperiment.restype = LIMRESULT

Lim_FileGetImageData = nd2.Lim_FileGetImageData
Lim_FileGetImageData.argtypes = [LIMFILEHANDLE, LIMUINT, POINTER(LIMPICTURE),
                                 POINTER(LIMLOCALMETADATA)]
Lim_FileGetImageData.restype = LIMRESULT

Lim_FileGetImageRectData = nd2.Lim_FileGetImageRectData
Lim_FileGetImageRectData.argtypes = [LIMFILEHANDLE, LIMUINT, LIMUINT,
                                     LIMUINT, LIMUINT, LIMUINT, LIMUINT,
                                     LIMUINT, c_void_p, LIMUINT, LIMINT,
                                     POINTER(LIMLOCALMETADATA)]
Lim_FileGetImageRectData.restype = LIMRESULT

Lim_FileGetBinaryDescriptors = nd2.Lim_FileGetBinaryDescriptors
Lim_FileGetBinaryDescriptors.argtypes = [LIMFILEHANDLE, POINTER(LIMBINARIES)]
Lim_FileGetBinaryDescriptors.restype = LIMRESULT

Lim_FileGetBinary = nd2.Lim_FileGetBinary
Lim_FileGetBinary.argtypes = [LIMFILEHANDLE, LIMUINT, LIMUINT,
                              POINTER(LIMPICTURE)]
Lim_FileGetBinary.restype = LIMRESULT

Lim_FileClose = nd2.Lim_FileClose
Lim_FileClose.argtypes = [LIMFILEHANDLE]
Lim_FileClose.restype = LIMRESULT


Lim_InitPicture = nd2.Lim_InitPicture
Lim_InitPicture.argtypes = [POINTER(LIMPICTURE),
                            LIMUINT, LIMUINT, LIMUINT, LIMUINT]
Lim_InitPicture.restype = LIMSIZE

Lim_DestroyPicture = nd2.Lim_DestroyPicture
Lim_DestroyPicture.argtypes = [POINTER(LIMPICTURE)]

Lim_GetSeqIndexFromCoords = nd2.Lim_GetSeqIndexFromCoords
Lim_GetSeqIndexFromCoords.argtypes = [POINTER(LIMEXPERIMENT),
                                      POINTER(LIMUINT * 4)]
Lim_GetSeqIndexFromCoords.restype = LIMUINT

Lim_GetCoordsFromSeqIndex = nd2.Lim_GetCoordsFromSeqIndex
Lim_GetCoordsFromSeqIndex.argtypes = [POINTER(LIMEXPERIMENT), LIMUINT,
                                      POINTER(LIMUINT)]

Lim_GetMultipointName = nd2.Lim_GetMultipointName
Lim_GetMultipointName.argtypes = [LIMFILEHANDLE, LIMUINT, LIMWSTR]
Lim_GetMultipointName.restype = LIMRESULT

Lim_GetLargeImageDimensions = nd2.Lim_GetLargeImageDimensions
Lim_GetLargeImageDimensions.argtypes = [LIMFILEHANDLE, POINTER(LIMUINT),
                                        POINTER(LIMUINT), POINTER(c_double)]
Lim_GetLargeImageDimensions.restype = LIMRESULT

Lim_GetRecordedDataInt = nd2.Lim_GetRecordedDataInt
Lim_GetRecordedDataInt.argtypes = [LIMFILEHANDLE, LIMCWSTR,
                                   LIMINT, POINTER(LIMINT)]
Lim_GetRecordedDataInt.restype = LIMRESULT

Lim_GetRecordedDataDouble = nd2.Lim_GetRecordedDataDouble
Lim_GetRecordedDataDouble.argtypes = [LIMFILEHANDLE, LIMCWSTR,
                                      LIMINT, POINTER(c_double)]
Lim_GetRecordedDataDouble.restype = LIMRESULT

Lim_GetRecordedDataString = nd2.Lim_GetRecordedDataString
Lim_GetRecordedDataString.argtypes = [LIMFILEHANDLE, LIMCWSTR,
                                      LIMINT, LIMWSTR]
Lim_GetRecordedDataString.restype = LIMRESULT

Lim_GetNextUserEvent = nd2.Lim_GetNextUserEvent
Lim_GetNextUserEvent.argtypes = [LIMFILEHANDLE, POINTER(LIMUINT),
                                 POINTER(LIMFILEUSEREVENT)]
Lim_GetNextUserEvent.restype = LIMRESULT

Lim_GetZStackHome = nd2.Lim_GetZStackHome
Lim_GetZStackHome.argtypes = [LIMFILEHANDLE]
Lim_GetZStackHome.restype = LIMINT
