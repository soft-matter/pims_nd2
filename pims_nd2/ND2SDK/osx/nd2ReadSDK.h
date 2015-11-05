/*
  ND2ReadSDK

  If you have any question, please contact us at nd2sdk-owners@nd2sdk.com
 
  For Public Discussion with all other people registered at www.nd2sdk.com with activated Mailing list option, please use nd2sdk@nd2sdk.com
 
*/

#ifndef __ND2READSDK_H__
#define __ND2READSDK_H__

#ifdef __cplusplus
#  define EXTERN extern "C"
#else
#  define EXTERN extern
#endif

#if _WIN32
#define DLLIMPORT __declspec(dllimport)
#else
#define DLLIMPORT
#endif 

#define LIMFILEAPI EXTERN DLLIMPORT

#ifndef _G5_API_EXTERNAL_H

#include <wchar.h>

typedef wchar_t            LIMWCHAR;
typedef LIMWCHAR*          LIMWSTR;
typedef LIMWCHAR const*    LIMCWSTR;
typedef unsigned int       LIMUINT;
typedef size_t             LIMSIZE;
typedef int                LIMINT;
typedef int                LIMBOOL;
typedef int                LIMRESULT;

#define LIM_OK                    0
#define LIM_ERR_UNEXPECTED       -1
#define LIM_ERR_NOTIMPL          -2
#define LIM_ERR_OUTOFMEMORY      -3
#define LIM_ERR_INVALIDARG       -4
#define LIM_ERR_NOINTERFACE      -5
#define LIM_ERR_POINTER          -6
#define LIM_ERR_HANDLE           -7
#define LIM_ERR_ABORT            -8
#define LIM_ERR_FAIL             -9
#define LIM_ERR_ACCESSDENIED     -10
#define LIM_ERR_OS_FAIL          -11
#define LIM_ERR_NOTINITIALIZED   -12
#define LIM_ERR_NOTFOUND         -13
#define LIM_ERR_IMPL_FAILED      -14
#define LIM_ERR_DLG_CANCELED     -15
#define LIM_ERR_DB_PROC_FAILED   -16
#define LIM_ERR_OUTOFRANGE       -17
#define LIM_ERR_PRIVILEGES       -18
#define LIM_ERR_VERSION          -19
#define LIM_SUCCESS(ret)         (0 <= (res))

typedef struct _LIMPICTURE
{
   LIMUINT     uiWidth;
   LIMUINT     uiHeight;
   LIMUINT     uiBitsPerComp;       // BPC 8 .. 16 or 32
   LIMUINT     uiComponents;
   LIMUINT     uiWidthBytes;        // aligned to 4-byte
   LIMSIZE     uiSize;
   void*       pImageData;          // BYTE* for BPC=8, WORD* for BPC (8, 16>, float* for BPC=32
} LIMPICTURE;

#define LIMMAXBINARIES         128

typedef struct _LIMBINARYDESCRIPTOR
{
   LIMWCHAR wszName[256];
   LIMWCHAR wszCompName[256];       // name of component, or empty string if this binary layer is unbound
   LIMUINT uiColorRGB;
} LIMBINARYDESCRIPTOR;

typedef struct _LIMBINARIES
{
   LIMUINT     uiCount;
   LIMBINARYDESCRIPTOR pDescriptors[LIMMAXBINARIES];
} LIMBINARIES;

#define LIMMAXPICTUREPLANES    256

typedef struct _LIMPICTUREPLANE_DESC
{
   LIMUINT     uiCompCount;         // Number of physical components
   LIMUINT     uiColorRGB;          // RGB color for display
   LIMWCHAR    wszName[256];        // Name for display
   LIMWCHAR    wszOCName[256];      // Name of the Optical Configuration
   double      dEmissionWL;
} LIMPICTUREPLANE_DESC;

typedef struct _LIMMETADATA_DESC
{
   double      dTimeStart;          // Absolute Time in JDN
   double      dAngle;              // Camera Angle
   double      dCalibration;        // um/px (0.0 = uncalibrated)
   double      dAspect;             // pixel aspect (always 1.0)
   LIMWCHAR    wszObjectiveName[256];
   double      dObjectiveMag;       // Optional additional information
   double      dObjectiveNA;        // dCalibration takes into accont all these
   double      dRefractIndex1;
   double      dRefractIndex2;
   double      dPinholeRadius;
   double      dZoom;
   double      dProjectiveMag;
   LIMUINT     uiImageType;         // 0 (normal), 1 (spectral)
   LIMUINT     uiPlaneCount;        // Number of logical planes (uiPlaneCount <= uiComponentCount)
   LIMUINT     uiComponentCount;    // Number of physical components (same as uiComp in LIMFILEATTRIBUTES)
   LIMPICTUREPLANE_DESC pPlanes[LIMMAXPICTUREPLANES];
} LIMMETADATA_DESC;

typedef struct _LIMTEXTINFO
{
   LIMWCHAR wszImageID[256];
   LIMWCHAR wszType[256];
   LIMWCHAR wszGroup[256];
   LIMWCHAR wszSampleID[256];
   LIMWCHAR wszAuthor[256];
   LIMWCHAR wszDescription[4096];
   LIMWCHAR wszCapturing[4096];
   LIMWCHAR wszSampling[256];
   LIMWCHAR wszLocation[256];
   LIMWCHAR wszDate[256];
   LIMWCHAR wszConclusion[256];
   LIMWCHAR wszInfo1[256];
   LIMWCHAR wszInfo2[256];
   LIMWCHAR wszOptics[256];
   LIMWCHAR wszAppVersion[256];
} LIMTEXTINFO;


#define LIMLOOP_TIME             0
#define LIMLOOP_MULTIPOINT       1
#define LIMLOOP_Z                2
#define LIMLOOP_OTHER            3

#define LIMMAXEXPERIMENTLEVEL    8

typedef struct _LIMEXPERIMENTLEVEL
{
   LIMUINT uiExpType;            // see LIMLOOP_TIME etc.
   LIMUINT  uiLoopSize;          // Number of images in the loop
   double   dInterval;           // ms (for Time), um (for ZStack), -1.0 (for Multipoint)
} LIMEXPERIMENTLEVEL;

typedef struct _LIMEXPERIMENT
{
   LIMUINT  uiLevelCount;
   LIMEXPERIMENTLEVEL pAllocatedLevels[LIMMAXEXPERIMENTLEVEL];
} LIMEXPERIMENT;

typedef struct _LIMLOCALMETADATA
{
   double   dTimeMSec;           // Relative time msec from the first
   double   dXPos;               // Stage XPos
   double   dYPos;               // Stage YPos
   double   dZPos;               // Stage ZPos

} LIMLOCALMETADATA;

//_G5_API_EXTERNAL_H
#endif


typedef int LIMFILEHANDLE;

typedef struct _LIMATTRIBUTES
{
   LIMUINT  uiWidth;             // Width of images
	LIMUINT  uiWidthBytes;        // Line length 4-byte aligned
   LIMUINT  uiHeight;            // Height if images
   LIMUINT  uiComp;              // Number of components
   LIMUINT  uiBpcInMemory;       // Bits per component 8, 16 or 32 (for float image)
   LIMUINT  uiBpcSignificant;    // Bits per component used 8 .. 16 or 32 (for float image)
   LIMUINT  uiSequenceCount;     // Number of images in the sequence
   LIMUINT  uiTileWidth;         // If an image is tiled size of the tile/strip 
   LIMUINT  uiTileHeight;        // otherwise both zero 
   LIMUINT  uiCompression;       // 0 (lossless), 1 (lossy), 2 (None)
   LIMUINT  uiQuality;           // 0 (worst) - 100 (best)

} LIMATTRIBUTES;

typedef struct _LIMFILEUSEREVENT
{
   LIMUINT    uiID;
   double     dTime;       
   LIMWCHAR   wsType[128]; 
   LIMWCHAR   wsDescription[256];
   
} LIMFILEUSEREVENT;

#define LIMSTRETCH_QUICK    1
#define LIMSTRETCH_SPLINES  2
#define LIMSTRETCH_LINEAR   3

LIMFILEAPI LIMFILEHANDLE   Lim_FileOpenForRead(LIMCWSTR wszFileName);
LIMFILEAPI LIMRESULT       Lim_FileGetAttributes(LIMFILEHANDLE hFile, LIMATTRIBUTES* pFileAttributes);
LIMFILEAPI LIMRESULT       Lim_FileGetMetadata(LIMFILEHANDLE hFile, LIMMETADATA_DESC* pFileMetadata);
LIMFILEAPI LIMRESULT       Lim_FileGetTextinfo(LIMFILEHANDLE hFile, LIMTEXTINFO* pFileTextinfo);
LIMFILEAPI LIMRESULT       Lim_FileGetExperiment(LIMFILEHANDLE hFile, LIMEXPERIMENT* pFileExperiment);
LIMFILEAPI LIMRESULT       Lim_FileGetImageData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMPICTURE* pPicture, LIMLOCALMETADATA* pImgInfo);
LIMFILEAPI LIMRESULT       Lim_FileGetImageRectData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMUINT uiDstTotalW, LIMUINT uiDstTotalH, LIMUINT uiDstX, LIMUINT uiDstY, LIMUINT uiDstW, LIMUINT uiDstH, void* pBuffer, LIMUINT uiDstLineSize, LIMINT iStretchMode, LIMLOCALMETADATA* pImgInfo);
LIMFILEAPI LIMRESULT       Lim_FileGetBinaryDescriptors(LIMFILEHANDLE hFile, LIMBINARIES* pBinaries);
LIMFILEAPI LIMRESULT       Lim_FileGetBinary(LIMFILEHANDLE hFile, LIMUINT uiSequenceIndex, LIMUINT uiBinaryIndex, LIMPICTURE* pPicture);
LIMFILEAPI LIMRESULT       Lim_FileClose(LIMFILEHANDLE hFile);

LIMFILEAPI LIMSIZE         Lim_InitPicture(LIMPICTURE* pPicture, LIMUINT width, LIMUINT height, LIMUINT bpc, LIMUINT components);
LIMFILEAPI void            Lim_DestroyPicture(LIMPICTURE* pPicture);

LIMFILEAPI LIMUINT         Lim_GetSeqIndexFromCoords(LIMEXPERIMENT* pExperiment, LIMUINT* pExpCoords);
LIMFILEAPI void            Lim_GetCoordsFromSeqIndex(LIMEXPERIMENT* pExperiment, LIMUINT uiSeqIdx, LIMUINT* pExpCoords);
LIMFILEAPI LIMRESULT       Lim_GetMultipointName(LIMFILEHANDLE hFile, LIMUINT uiPointIdx, LIMWSTR wstrPointName);
LIMFILEAPI LIMINT          Lim_GetZStackHome(LIMFILEHANDLE hFile);
LIMFILEAPI LIMRESULT       Lim_GetLargeImageDimensions(LIMFILEHANDLE hFile, LIMUINT* puiXFields, LIMUINT* puiYFields, double* pdOverlap);

LIMFILEAPI LIMRESULT       Lim_GetRecordedDataInt(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMINT *piData);
LIMFILEAPI LIMRESULT       Lim_GetRecordedDataDouble(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, double* pdData);
LIMFILEAPI LIMRESULT       Lim_GetRecordedDataString(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMWSTR wszData);
LIMFILEAPI LIMRESULT       Lim_GetNextUserEvent(LIMFILEHANDLE hFile, LIMUINT *puiNextID, LIMFILEUSEREVENT* pEventInfo);

LIMFILEAPI LIMINT          Lim_GetCustomDataCount(LIMFILEHANDLE hFile);
LIMFILEAPI LIMRESULT       Lim_GetCustomDataInfo(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszName, LIMWSTR wszDescription, LIMINT *piType, LIMINT *piFlags);
LIMFILEAPI LIMRESULT       Lim_GetCustomDataDouble(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, double* pdData);
LIMFILEAPI LIMRESULT       Lim_GetCustomDataString(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszData, LIMINT *piLength);

LIMFILEAPI LIMRESULT       Lim_GetStageCoordinates(LIMFILEHANDLE hFile, LIMUINT uiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double* pdXPos, double *pdYPos, double *pdZPos, LIMINT iUseAlignment);
LIMFILEAPI LIMRESULT       Lim_SetStageAlignment(LIMFILEHANDLE hFile, LIMUINT uiPosCount, double* pdXSrc, double* pdYSrc, double* pdXDst, double *pdYDst);
LIMFILEAPI LIMRESULT       Lim_GetAlignmentPoints(LIMFILEHANDLE hFile, LIMUINT* puiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double *pdXPos, double *pdYPos);

#endif // __ND2READSDK_H__
