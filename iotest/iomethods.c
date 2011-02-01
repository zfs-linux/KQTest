#include "iotest.h"

#define _FILE_OFFSET_BITS    64
#define PAGE_SIZE           getpagesize()
#define MAX_ARRAY_SIZE      65356 /* Max size of g_iosizeArray array*/

int g_verifyInitialised     = FALSE;
pthread_mutex_t g_mutex     = PTHREAD_MUTEX_INITIALIZER;
uint64 **g_iosizeArray;       /* To store the relative offsets and iosize */
uint64 g_globalArrayIteration;/* No. of times iosizes mentioned in
                               * g_iosizeArray will be completely read/written
                               */
uint64 g_sumOfIosizeArray = 0;/* Sum of iosizes mentioned in g_iosizeArray */
uint64 g_offsetMark;          /* Offset mark, incremented by g_sumOfIosizeArray
                               * after each iteration of g_iosizeArray
                               */
int32 g_globalArrayCount;     /* No. of elements in g_iosizeArray */
uint64 **g_iosizeSubArray;    /* To store the relative offsets and iosize
                                which will used after writing
                                g_sumOfIosizeArray * g_globalArrayIteration */
uint64 g_globalSubArrayCount; /* No. of elements in g_iosizeSubArray*/
uint64 g_sumOfIosizeSubArray; /* Sum of iosizes mentioned in g_iosizeSubArray */
uint64 g_firstThreadExtraSize = 0;/* Extra size for first thread */

int g_write = 0;
int g_status                = SUCCESS;

struct kqFileOperations fops = {
    .openInput          = kqIoOpenInputFile,
    .openOutput         = kqIoOpenOutputFile,
    .readDirectSeq      = kqIoBufferedDirectSeqRead,
    .readDirectRandom   = kqIoBufferedDirectRandkqRead,
    .readBufferedSeq    = kqIoBufferedDirectSeqRead,
    .readBufferedRandom = kqIoBufferedDirectRandkqRead,
    .readMmapSeq        = kqIoMmapSeqRead,
    .readMmapRandom     = kqIoMmapRandkqRead,
    .writeDirectSeq     = kqIoBufferedDirectSeqWrite,
    .writeDirectRandom  = kqIoBufferedDirectRandkqWrite,
    .writeBufferedSeq   = kqIoBufferedDirectSeqWrite,
    .writeBufferedRandom= kqIoBufferedDirectRandkqWrite,
    .writeMmapSeq       = kqIoMmapSeqWrite,
    .writeMmapRandom    = kqIoMmapRandkqWrite,
};


/*
 * Function     : kqIoCommonAllocateBuffer
 *
 * Description  : This function allocates buffer.
 *
 * Parameters   :
 *      1. size     Size for the the buffer to be allocated.
 *
 * Return Value :
 *                 Pointer to the filled buffer.
 */
char* kqIoCommonAllocateBuffer(int size)
{
    char *buffer = NULL;

    debug("%s\n", __FUNCTION__);

    buffer = (char *) malloc(size * sizeof(char));
    if (buffer == NULL) {
        error("Failed to allocate buffer of size %"PRIu32"\n", size);
        exit(ENOMEM);
    }
    debug("Allocated buffer of size %"PRIu32" at address %x \n",
          size, buffer);
    return buffer;
}


/*
 * Function     : kqIoFillBuffer
 *
 * Description  : This function fills the buffer with pattern provided.
 *
 * Parameters   :
 *      1. buffer           Allocated buffer which is to to be filled with the
 *                          pattern.
 *      2. pattern          Pattern.
 *      3. lengthRemaining  Size of the buffer.
 *
 */
void  kqIoFillBuffer(char *buffer, char *pattern, uint64 lengthRemaining)
{

    debug("%s\n", __FUNCTION__);

    while (lengthRemaining > 0) {
        if (lengthRemaining > g_patternLen) {
            memcpy(buffer, pattern, g_patternLen);
        } else {
            memcpy(buffer, pattern, lengthRemaining);
            break;
        }
        lengthRemaining -= g_patternLen;
        buffer += g_patternLen;
    }
}


/*
 * Function    : kqCollectIoStats
 *
 * Description : This function calculates the io statistics
 *
 */
void  kqCollectIoStats()
{
    int32 numThreads           = 0;
    int32 i                    = 0;
    int64 minReadStartTime     = 0;
    int64 minWriteStartTime    = 0;
    int64 maxReadEndTime       = 0;
    int64 maxWriteEndTime      = 0;

    debug("%s\n", __FUNCTION__);

    if (kqContext.opcode == OP_READ) {
        numThreads = kqContext.numReadThreads;
    } else {
        numThreads = kqContext.numWriteThreads;
    }
    for (i = 0; i < numThreads; i++) {
        if ((kqIoStats[i].readStartTime < minReadStartTime) ||
                (minReadStartTime == 0)) {
            minReadStartTime = kqIoStats[i].readStartTime;
        }
        if (kqIoStats[i].readEndTime > maxReadEndTime) {
            maxReadEndTime = kqIoStats[i].readEndTime;
        }
        if ((kqIoStats[i].writeStartTime < minWriteStartTime) ||
                (minWriteStartTime == 0)) {
            minWriteStartTime = kqIoStats[i].writeStartTime;
        }
        if (kqIoStats[i].writeEndTime > maxWriteEndTime) {
            maxWriteEndTime = kqIoStats[i].writeEndTime;
        }
    }
    kqIoPerf.readStartTime = minReadStartTime;
    kqIoPerf.readEndTime = maxReadEndTime;
    kqIoPerf.writeStartTime = minWriteStartTime;
    kqIoPerf.writeEndTime = maxWriteEndTime;
    /* store time in milliseconds */
    kqIoPerf.readTotalTime = (kqIoPerf.readEndTime -
            kqIoPerf.readStartTime) * .001;
    kqIoPerf.writeTotalTime = (kqIoPerf.writeEndTime -
            kqIoPerf.writeStartTime) * .001;
    printf("readtotal %g writetotal %g \n", kqIoPerf.readTotalTime , kqIoPerf.writeTotalTime);
}


/*
 * Function     :   kqIoAllocReadBuffer
 *
 * Description  :   This function chooses the required size
 *                  for read buffer.
 *
 * Parameters   :
 *      1. ioSize       iosize
 *      2. patternLen   Pattern length
 *
 * Return Value :
 *                      Pointer to the buffer which is double
 *                      either iosize or pattern length.
 */
char* kqIoAllocReadBuffer(uint64 ioSize, uint32 patternLen)
{
    char *buffer;

    debug("%s\n", __FUNCTION__);

    if (ioSize <= patternLen) {
        if ((buffer = kqIoCommonAllocateBuffer(patternLen *sizeof(char) *
                        2)) == NULL) {
            return NULL;
        }
    } else {
        if ((buffer = kqIoCommonAllocateBuffer(ioSize * sizeof(char) *
                        2)) == NULL) {
            return NULL;
        }
    }
    return buffer;
}


/*
 * Function     :   kqIoFillPattern
 *
 * Description  :   This function chooses the required buffer size
 *                  and fills it with pattern.
 *
 * Parameters   :
 *      1. ioSize       iosize
 *      2. patternLen   Pattern length
 *
 * Return Value :
 *                      Pointer to the buffer which is double
 *                      either iosize or pattern length.
 */
char* kqIoFillPattern(uint64 ioSize, uint32 patternLen)
{
    char *buffer;

    debug("%s\n", __FUNCTION__);

    if (ioSize <= patternLen) {
        if ((buffer = kqIoCommonAllocateBuffer(patternLen *sizeof(char) *
                        2)) == NULL) {
            return NULL;
        }
        kqIoFillBuffer(buffer, g_pattern, patternLen * 2);
    } else {
        if ((buffer = kqIoCommonAllocateBuffer(ioSize * sizeof(char) *
                        2)) == NULL) {
            return NULL;
        }
        kqIoFillBuffer(buffer, g_pattern, ioSize * 2);
    }
    return buffer;
}


/*
 * Function     :   getArrayCount
 *
 * Description  :   This function calculates the number elements for global
 *                  array which contains offser and iosize.
 *
 * Parameters   :
 *
 * Return Value :
 *                  Returns the number elements for global array .
 */
uint64 getArrayCount(uint64 size)
{
    uint64 iosize;
    uint64 count = 0;

    debug("%s\n", __FUNCTION__);

    srand48(kqContext.seed);
    while (size > 0) {
        if (g_randomIosize) {
            if (kqContext.opcode == OP_READ) {
                iosize = (lrand48() % (kqContext.rarguments.maxBlockSize +
                            1 - kqContext.rarguments.minBlockSize) +
                        kqContext.rarguments.minBlockSize);
            } else {
                iosize = (lrand48() % (kqContext.warguments.maxBlockSize +
                            1 - kqContext.warguments.minBlockSize) +
                        kqContext.warguments.minBlockSize);
            }
        } else {
            if (kqContext.opcode == OP_READ) {
                iosize = kqContext.rarguments.blockSize;
            } else {
                iosize = kqContext.warguments.blockSize;
            }
        }
        count++;
        if (size <= iosize) {
            break;
        } else {
            size -= iosize;
        }
    }
    return count;
}


/*
 * Function     :   createGlobalSubArray
 *
 * Description  :   This function created the global random array which
 *                  contains offser and iosize.This fuction is called
 *                  only when total size is greater than
 *                  (g_globalArrayIteration * g_sumOfIosizeArray * noOfThreads)
 *
 * Parameters   :
 *          size    Remaining size in bytes.
 *                  total size - (g_globalArrayIteration * g_sumOfIosizeArray *
 *                  noOfThreads)
 *
 * Return Value :
 */
void createGlobalSubArray(uint64 size)
{
    uint64 i      = 0;
    uint64 offset;
    uint64 iosize;
    uint64 sizeRemaining;
    uint64 sizePerThread;
    uint64 bigRand;
    uint64 subArrayCount;
    uint32 noOfThreads;
    uint64 *tmp;
    uint64 directIoOps      = 0;
    uint64 directIoOpsPerThread;

    debug("%s\n", __FUNCTION__);

    offset =  g_globalArrayIteration * g_offsetMark;
    if (kqContext.opcode == OP_READ) {
        noOfThreads = kqContext.numReadThreads;
        directIoOps = size / g_sectorSize;
        directIoOpsPerThread = directIoOps / noOfThreads;
    } else {
        noOfThreads = kqContext.numWriteThreads;
        directIoOps = size / g_sectorSize;
        directIoOpsPerThread = directIoOps / noOfThreads;
    }
    if (kqContext.warguments.rwflag == IO_DIRECT ||
                kqContext.rarguments.rwflag == IO_DIRECT) {
             sizePerThread = directIoOpsPerThread *  g_sectorSize;
    } else {
        sizePerThread = (size / noOfThreads);
    }
    subArrayCount = getArrayCount(sizePerThread);
    g_globalSubArrayCount = subArrayCount;
    g_iosizeSubArray = (uint64 **)malloc(sizeof(uint64 *) * subArrayCount);
    if (g_iosizeSubArray == NULL) {
        error("malloc failed \n");
        exit(ENOMEM);
    }
    for (i = 0; i < subArrayCount; i++) {
        g_iosizeSubArray[i] = malloc(2 * sizeof(uint64));
        if (g_iosizeSubArray[i] == NULL) {
            error("malloc failed \n");
            exit(ENOMEM);
        }
    }
    srand48(kqContext.seed);
    sizeRemaining = sizePerThread;
    for (i = 0; i < subArrayCount; i++) {
        if (g_randomIosize) {
            if (kqContext.opcode == OP_READ) {
                iosize = (lrand48() % (kqContext.rarguments.maxBlockSize +
                            1 - kqContext.rarguments.minBlockSize) +
                        kqContext.rarguments.minBlockSize);
            } else {
                iosize = (lrand48() % (kqContext.warguments.maxBlockSize +
                            1 - kqContext.warguments.minBlockSize) +
                        kqContext.warguments.minBlockSize);
            }
        } else {
            if (kqContext.opcode == OP_READ) {
                iosize = kqContext.rarguments.blockSize;
            } else {
                iosize = kqContext.warguments.blockSize;
            }
        }
        if (sizeRemaining < iosize) {
            g_iosizeSubArray[i][1]  = sizeRemaining;
        } else {
            g_iosizeSubArray[i][1] = iosize;
        }
        g_iosizeSubArray[i][0] = offset;
        offset += g_iosizeSubArray[i][1] * kqContext.sparseFactor;
        g_sumOfIosizeSubArray += g_iosizeSubArray[i][1];
        sizeRemaining -= iosize;
    }
    /* Randomizing g_ig_iosizeSubArray */
    srand48(kqContext.seed);
    for (i = 0; i < subArrayCount; i++) {
        bigRand = lrand48();
        bigRand = bigRand % subArrayCount;
        tmp = g_iosizeSubArray[i];
        g_iosizeSubArray[i] = g_iosizeSubArray[bigRand];
        g_iosizeSubArray[bigRand] = tmp;
    }
    /* Calculate the extra size which will be given for first thread.*/
    if (kqContext.opcode == OP_READ) {
        g_firstThreadExtraSize  = kqContext.rarguments.size -
                                  (kqContext.numReadThreads *
                                  ((g_sumOfIosizeArray *
                                  g_globalArrayIteration)  +
                                  (g_sumOfIosizeSubArray *
                                  g_globalSubArrayCount)));
    } else {
        g_firstThreadExtraSize = kqContext.warguments.size -
                                (kqContext.numWriteThreads *
                                ((g_sumOfIosizeArray *
                                g_globalArrayIteration)  +
                                (g_sumOfIosizeSubArray)));
    }
}


/*
 * Function     :   createGlobalArray
 *
 * Description  :   This function created the global  random array which
 *                  contains offser and iosize.
 *
 * Parameters   :
 *      size       Total read/write size in bytes.
 *
 * Return Value :
 */
void createGlobalArray(uint64 size)
{
    uint64 i      = 0;
    uint64 offset = 0;
    uint64 iosize;
    uint64 sizeRemaining;
    uint64 sizePerThread;
    uint64 bigRand;
    uint64 arrayCount;
    uint32 noOfThreads;
    uint64 *tmp;
    uint64 subSize;
    uint64 directIoOps      = 0;
    uint64 directIoOpsPerThread;

    debug("%s\n", __FUNCTION__);

    if (kqContext.opcode == OP_READ) {
        noOfThreads = kqContext.numReadThreads;
        directIoOps = kqContext.rarguments.size / g_sectorSize;
        directIoOpsPerThread = directIoOps / noOfThreads;
    } else {
        noOfThreads = kqContext.numWriteThreads;
        directIoOps = kqContext.warguments.size / g_sectorSize;
        directIoOpsPerThread = directIoOps / noOfThreads;
    }
    if (kqContext.warguments.rwflag == IO_DIRECT ||
                kqContext.rarguments.rwflag == IO_DIRECT) {
             sizePerThread = directIoOpsPerThread *  g_sectorSize;
    } else {
            sizePerThread = (size / noOfThreads);
    }
    arrayCount = getArrayCount(sizePerThread);
    if (MAX_ARRAY_SIZE < arrayCount) {
        arrayCount =  MAX_ARRAY_SIZE;
    }
    g_globalArrayCount = arrayCount;
    g_iosizeArray = (uint64 **)malloc(sizeof(uint64 *) * arrayCount);
    if (g_iosizeArray == NULL) {
        error("malloc failed \n");
        exit(ENOMEM);
    }
    for (i = 0; i < arrayCount; i++) {
        g_iosizeArray[i] = malloc(2 * sizeof(uint64));
        if (g_iosizeArray[i] == NULL) {
            error("malloc failed \n");
            exit(ENOMEM);
        }
    }
    srand48(kqContext.seed);
    sizeRemaining = sizePerThread;
    for (i = 0; i < arrayCount; i++) {
        if (g_randomIosize) {
            if (kqContext.opcode == OP_READ) {
                iosize = (lrand48() % (kqContext.rarguments.maxBlockSize +
                            1 - kqContext.rarguments.minBlockSize) +
                        kqContext.rarguments.minBlockSize);
            } else {
                iosize = (lrand48() % (kqContext.warguments.maxBlockSize +
                            1 - kqContext.warguments.minBlockSize) +
                        kqContext.warguments.minBlockSize);
            }
        } else {
            if (kqContext.opcode == OP_READ) {
                iosize = kqContext.rarguments.blockSize;
            } else {
                iosize = kqContext.warguments.blockSize;
            }
        }
        if (sizeRemaining < iosize) {
            g_iosizeArray[i][1] = sizeRemaining;
        } else {
            g_iosizeArray[i][1] = iosize;
        }
        g_iosizeArray[i][0] = offset;
        sizeRemaining -= iosize;
        offset += g_iosizeArray[i][1] * kqContext.sparseFactor;
        g_sumOfIosizeArray += g_iosizeArray[i][1];
    }
    /* Setting g_offsetMark to the last offset of g_iosizeArray*/
    g_offsetMark = offset;
    /* Calculation for g_globalArrayIteration */
    g_globalArrayIteration = sizePerThread / g_sumOfIosizeArray;
    subSize = size - (g_globalArrayIteration * g_sumOfIosizeArray *
                        noOfThreads);
    if (subSize != 0) {
    createGlobalSubArray(subSize);
    }
    /* Randomizing g_iosizeArray */
    srand48(kqContext.seed);
    for (i = 0; i < arrayCount; i++) {
        bigRand = lrand48();
        bigRand = bigRand % arrayCount;
        tmp = g_iosizeArray[i];
        g_iosizeArray[i] = g_iosizeArray[bigRand];
        g_iosizeArray[bigRand] = tmp;
    }
}


/*
 * Function     :   kqIoBufferedDirectSeqRead
 *
 * Description  :   This function performs sequential read for buffered and
 *                  direct I/O.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which read needs to be started.
 *      3. count    No. of I/O operations.
 * Return Value :
 *                  Returns SUCCESS if read was successful.
 *                  Returns FAILURE if read failed.
 */
int kqIoBufferedDirectSeqRead(int fd, uint64 offset, uint64 size)
{
    uint64 sizeRemaining    = size;
    char *buffer            = NULL;
    bool finalRead          = false;
    uint64 i                = 0;
    uint64 iosize;
    uint64 randomSleep;

    debug("%s\n", __FUNCTION__);

    if (g_randomIosize) {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    while (sizeRemaining != 0) {
        if (g_randomIosize) {
            iosize = g_iosizeArray[i][1];
            i++;
            if (i == g_globalArrayCount) {
                i = 0;
            }
        } else {
            iosize = kqContext.rarguments.blockSize;
        }
        if ((iosize) <= sizeRemaining) {
            if (kqIoCommonRead(fd, offset, iosize,
                        buffer) == FAILURE) {
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
        } else {
            if (kqIoCommonRead(fd, offset, sizeRemaining, buffer) ==
                    FAILURE) {
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            finalRead = true;
        }
        if (!g_randomSleep) {
            if (kqContext.rarguments.sleep != 0) {
                usleep(kqContext.rarguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.rarguments.maxSleep
                        + 1 - kqContext.rarguments.minSleep)) +
                kqContext.rarguments.minSleep;
            usleep(randomSleep);
        }
        if (kqContext.verify == TRUE) {
            if (!finalRead) {
                if (kqIoVerifyBlock(offset, buffer, iosize) == SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                }
            } else {
                if (kqIoVerifyBlock(offset, buffer, sizeRemaining) ==
                        SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, sizeRemaining);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, sizeRemaining);
                }
            }
        }
        if (kqContext.sparseFactor > 1) {
            offset +=  (kqContext.sparseFactor * iosize);
        } else {
            offset += iosize;
        }
        if (!finalRead) {
            sizeRemaining -= (iosize);
        } else {
            sizeRemaining = 0;
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     :   kqIoBufferedDirectRandkqRead
 *
 * Description  :   This function performs random read for buffered and
 *                  direct I/O.
 *
 * Parameters   :
 *      1. fd           File descriptor.
 *      2. baseOffset   Base Offset from where next I/O operation will start.
 *      3. size         Total size of the I/O operation.
 * Return Value :
 *                      Returns SUCCESS if read was successful.
 *                      Returns FAILURE if read failed.
 */
int kqIoBufferedDirectRandkqRead(int fd, uint64 baseOffset, uint64 size)
{
    uint64 i                = 0;
    char *buffer            = NULL;
    uint64 count            = 0;
    uint64 offset;
    uint32 randomSleep;
    uint64 iosize;
    uint64 offsetMark;
    uint64 sizeRemaining;

    debug("%s : Baseoffset  %"PRIu64" size %"PRIu64"\n", __FUNCTION__,
            baseOffset, size);

    if (g_randomIosize) {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    /* Do the I/O for (g_globalArrayIteration * g_sumOfIosizeArray) */
    offsetMark = baseOffset;
    for (count = 0; count < g_globalArrayIteration; count++) {
        for (i = 0; i != g_globalArrayCount; i++) {
            offset = g_iosizeArray[i][0] + offsetMark;
            iosize = g_iosizeArray[i][1];
            if (kqIoCommonRead(fd, offset, iosize,
                                 buffer) == FAILURE) {
                free(buffer);
                return FAILURE;
            }
            if (!g_randomSleep) {
                if (kqContext.rarguments.sleep != 0) {
                    usleep(kqContext.rarguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.rarguments.maxSleep
                            + 1 - kqContext.rarguments.minSleep)) +
                    kqContext.rarguments.minSleep;
                usleep(randomSleep);
            }
            if (kqContext.verify == TRUE) {
                if (kqIoVerifyBlock(offset, buffer, iosize) ==
                        SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                }
            }
        }
        offsetMark += g_offsetMark;
    }
    sizeRemaining = (size - (g_globalArrayIteration * g_sumOfIosizeArray));
    if (sizeRemaining != 0) {
        for (i = 0; i < g_globalSubArrayCount; i++) {
            offset =  g_iosizeSubArray[i][0] + baseOffset;
            iosize =  g_iosizeSubArray[i][1];
            if (kqIoCommonRead(fd, offset, iosize,
                        buffer) == FAILURE) {
                free(buffer);
                return FAILURE;
            }
            if (!g_randomSleep) {
                if (kqContext.rarguments.sleep != 0) {
                    usleep(kqContext.rarguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.rarguments.maxSleep
                            + 1 - kqContext.rarguments.minSleep)) +
                    kqContext.rarguments.minSleep;
                usleep(randomSleep);
            }
            if (kqContext.verify == TRUE) {
                if (kqIoVerifyBlock(offset, buffer, iosize) ==
                        SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                }
                sizeRemaining -= g_iosizeSubArray[i][1];
            }
        }
    }
    if (g_firstThreadExtraSize != 0) {
        offset = g_sumOfIosizeSubArray + (g_globalArrayIteration *
                    g_sumOfIosizeArray);
        if (kqIoCommonRead(fd, offset, g_firstThreadExtraSize,
                    buffer) == FAILURE) {
            free(buffer);
            return FAILURE;
        }
        if (!g_randomSleep) {
            if (kqContext.rarguments.sleep != 0) {
                usleep(kqContext.rarguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.rarguments.maxSleep
                        + 1 - kqContext.rarguments.minSleep)) +
                kqContext.rarguments.minSleep;
            usleep(randomSleep);
        }
        if (kqContext.verify == TRUE) {
            if (kqIoVerifyBlock(offset, buffer, g_firstThreadExtraSize) ==
                    SUCCESS) {
                debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                        "\n", offset, g_firstThreadExtraSize);
            } else {
                error("Verification  offset %10"PRIu64" length %10"PRIu64""
                        "\n", offset, g_firstThreadExtraSize);
            }
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     :   kqIoMmapSeqRead
 *
 * Description  :   This function performs mmap sequentitial read.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which read needs to be started.
 *      3. count    No. of I/O operations.
 * Return Value :
 *                  Returns SUCCESS if read was successful.
 *                  Returns FAILURE if read failied.
 */
int kqIoMmapSeqRead(int fd, uint64 offset, uint64 size)
{
    uint64 fileOffset       = 0;
    uint64 sizeRemaining    = size;
    void   *file_memory     = NULL;
    char   *buffer          = NULL;
    uint64 pageStart        = 0;
    bool finalRead          = false;
    uint64 i                = 0;
    uint64 iosize;
    uint64 pageEnd;
    uint64 inpageOffset;
    uint32 randomSleep;

    debug("%s\n", __FUNCTION__);

    if (g_randomIosize) {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    /* start from the block boundary before the offset */
    fileOffset = offset;
    while (sizeRemaining != 0) {
        if (g_randomIosize) {
            iosize = g_iosizeArray[i][1];
            i++;
            if (i == g_globalArrayCount) {
                i = 0;
            }
        } else {
            iosize = kqContext.rarguments.blockSize;
        }
        pageStart = fileOffset / PAGE_SIZE;
        if  ((iosize) <= sizeRemaining) {
            pageEnd = (fileOffset + iosize + PAGE_SIZE -1) /
                PAGE_SIZE;
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64"" \
                    "size %10" PRIu64"\n", fileOffset, pageStart, iosize);
        } else {
            pageEnd = (fileOffset + sizeRemaining  + PAGE_SIZE -1) /
                PAGE_SIZE;
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64"" \
                  "size %10" PRIu64"\n", fileOffset, pageStart, sizeRemaining);
            finalRead = true;
        }
        inpageOffset = fileOffset % PAGE_SIZE;
        file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ,
                MAP_SHARED, fd, (pageStart * PAGE_SIZE));
        if (file_memory == MAP_FAILED) {
            error("mmap failed ! %s\n", strerror(errno));
            if (buffer != NULL) {
                free(buffer);
            }
            return FAILURE;
        }
        if (!finalRead) {
            memcpy(buffer, (char *)(file_memory + inpageOffset),
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
        } else {
            memcpy(buffer, (char *)(file_memory + inpageOffset),
                    sizeRemaining);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
        }
        if (!g_randomSleep) {
            if (kqContext.rarguments.sleep != 0) {
                usleep(kqContext.rarguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.rarguments.maxSleep
                        + 1 - kqContext.rarguments.minSleep)) +
                kqContext.rarguments.minSleep;
            usleep(randomSleep);
        }
        if (kqContext.verify == TRUE) {
            if (!finalRead) {
                if (kqIoVerifyBlock(fileOffset, buffer, iosize) == SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", fileOffset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", fileOffset, iosize);
                }
            } else {
                if (kqIoVerifyBlock(fileOffset, buffer, sizeRemaining) ==
                        SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", fileOffset, sizeRemaining);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", fileOffset, sizeRemaining);
                }
            }
        }
        if (kqContext.sparseFactor > 1) {
            fileOffset +=  (kqContext.sparseFactor * iosize);
        } else {
            fileOffset += iosize;
        }
        sizeRemaining -= iosize;
        if (finalRead) {
            sizeRemaining = 0;
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     : kqIoMmapRandkqRead
 *
 * Description  : This function performs mmap random read.
 *
 * Parameters   :
 *      1. fd           File descriptor.
 *      2. baseOffset   Base Offset from where next I/O operation will start.
 *      3. size         Total size of the I/O operation.
 * Return Value :
 *                      Returns SUCCESS if read was successful.
 *                      Returns FAILURE if read failed.
 */
int kqIoMmapRandkqRead(int fd, uint64 baseOffset, uint64 size)
{
    uint64 offset;
    void   *file_memory     = NULL;
    char   *buffer          = NULL;
    uint64 inpageOffset     = 0;
    uint64 pageStart        = 0;
    uint64 pageEnd          = 0;
    uint64 count            = 0;
    uint64 i                = 0;
    uint64  randomSleep;
    uint64 offsetMark;
    uint64 iosize;
    uint64 sizeRemaining;

    debug("%s : Baseoffset  %"PRIu64" size %"PRIu64"\n", __FUNCTION__,
            baseOffset, size);

    if (g_randomIosize) {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoAllocReadBuffer(kqContext.rarguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    /* Do the I/O for (g_globalArrayIteration * g_sumOfIosizeArray) */
    offsetMark = baseOffset;
    for (count = 0; count < g_globalArrayIteration; count++) {
        for (i = 0; i != g_globalArrayCount; i++) {
            offset = g_iosizeArray[i][0] + offsetMark;
            iosize = g_iosizeArray[i][1];
            pageStart = offset / PAGE_SIZE;
            pageEnd = (offset + iosize + PAGE_SIZE -1) /
                PAGE_SIZE;
            inpageOffset = offset % PAGE_SIZE;
            file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ,
                    MAP_SHARED, fd, (pageStart * PAGE_SIZE));
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", offset, pageStart, iosize);
            if (file_memory == MAP_FAILED) {
                error("mmap failed ! %s\n", strerror(errno));
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            memcpy(buffer, (char *)(file_memory + inpageOffset),
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE );
            if (!g_randomSleep) {
                if (kqContext.rarguments.sleep != 0) {
                    usleep(kqContext.rarguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.rarguments.maxSleep
                            + 1 - kqContext.rarguments.minSleep)) +
                    kqContext.rarguments.minSleep;
                usleep(randomSleep);
            }
            if (kqContext.verify == TRUE) {
                if (kqIoVerifyBlock(offset, buffer, iosize) ==
                        SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                }
            }
        }
        offsetMark += g_offsetMark;
    }
    sizeRemaining = (size - (g_globalArrayIteration * g_sumOfIosizeArray));
    if (sizeRemaining != 0) {
        for (i = 0; i < g_globalSubArrayCount; i++) {
            offset =  g_iosizeSubArray[i][0] + baseOffset;
            iosize =  g_iosizeSubArray[i][1];
            pageStart = offset / PAGE_SIZE;
            pageEnd = (offset + iosize + PAGE_SIZE -1) /
                PAGE_SIZE;
            inpageOffset = offset % PAGE_SIZE;
            file_memory = mmap(0, (pageEnd - pageStart + 1) * PAGE_SIZE, PROT_READ,
                    MAP_SHARED, fd, (pageStart * PAGE_SIZE));
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", offset, pageStart, iosize);
            if (file_memory == MAP_FAILED) {
                error("mmap failed ! %s\n", strerror(errno));
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            memcpy(buffer, (char *)(file_memory + inpageOffset),
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            if (!g_randomSleep) {
                if (kqContext.rarguments.sleep != 0) {
                    usleep(kqContext.rarguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.rarguments.maxSleep
                            + 1 - kqContext.rarguments.minSleep)) +
                    kqContext.rarguments.minSleep;
                usleep(randomSleep);
            }
            if (kqContext.verify == TRUE) {
                if (kqIoVerifyBlock(offset,
                            buffer,iosize) == SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, iosize);
                }
            }
            sizeRemaining -= iosize;
        }
    }
        if (g_firstThreadExtraSize != 0) {
            offset = g_sumOfIosizeSubArray + (g_globalArrayIteration *
                         g_sumOfIosizeArray);
            pageStart = offset / PAGE_SIZE;
            pageEnd = (offset + g_firstThreadExtraSize + PAGE_SIZE -1) /
                PAGE_SIZE;
            inpageOffset = offset % PAGE_SIZE;
            file_memory = mmap(0, (pageEnd - pageStart + 1) * PAGE_SIZE, PROT_READ,
                    MAP_SHARED, fd, (pageStart * PAGE_SIZE));
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", offset, pageStart, g_firstThreadExtraSize);
            if (file_memory == MAP_FAILED) {
                error("mmap failed ! %s\n", strerror(errno));
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            memcpy(buffer, (char *)(file_memory + inpageOffset),
                    g_firstThreadExtraSize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            if (!g_randomSleep) {
                if (kqContext.rarguments.sleep != 0) {
                    usleep(kqContext.rarguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.rarguments.maxSleep
                            + 1 - kqContext.rarguments.minSleep)) +
                    kqContext.rarguments.minSleep;
                usleep(randomSleep);
            }
            if (kqContext.verify == TRUE) {
                if (kqIoVerifyBlock(offset,
                            buffer,g_firstThreadExtraSize) == SUCCESS) {
                    debug("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, g_firstThreadExtraSize);
                } else {
                    error("Verification  offset %10"PRIu64" length %10"PRIu64""
                            "\n", offset, g_firstThreadExtraSize);
                }
            }
    }
    free(buffer);
    return SUCCESS;
}

/*
 * Function     :   kqIoBufferedDirectSeqWrite
 *
 * Description  :   This function performs seq write for buffered and
 *                  direct I/O.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which  write needs to be started.
 *      3. count    No. of I/O operations.
 * Return Value :
 *                  Returns SUCCESS if write was successful.
 *                  Returns FAILURE if write failed.
 */
int kqIoBufferedDirectSeqWrite(int fd, uint64 offset, uint64 size)
{
    uint64 sizeRemaining    = size;
    char   *buffer          = NULL;
    uint64 skip             = 0;
    bool finalWrite         = false;
    uint64 i                = 0;
    uint64 iosize;
    uint32 randomSleep;

    debug("%s\n", __FUNCTION__);

    if (g_randomIosize) {
        if ((buffer = kqIoFillPattern(kqContext.warguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoFillPattern(kqContext.warguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    while (sizeRemaining != 0) {
        if (g_randomIosize) {
            iosize = g_iosizeArray[i][1];
            i++;
            if (i == g_globalArrayCount) {
                i = 0;
            }
        } else {
            iosize = kqContext.warguments.blockSize;
        }
        skip = (offset % g_patternLen);
        if  ((iosize) <= sizeRemaining) {
            if (kqIoCommonWrite(fd, offset, iosize,
                        buffer + skip) == FAILURE) {
                if (buffer != NULL && (buffer != g_pattern)) {
                    free(buffer);
                }
                return FAILURE;
            }
        } else {
            if (kqIoCommonWrite(fd, offset, sizeRemaining, buffer + skip) ==
                    FAILURE) {
                if ((buffer != NULL) && (buffer != g_pattern))
                    free(buffer);
                return FAILURE;
            }
            finalWrite = true;
        }
        if (!g_randomSleep) {
            if (kqContext.warguments.sleep != 0) {
                usleep(kqContext.warguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.warguments.maxSleep
                        + 1 - kqContext.warguments.minSleep)) +
                kqContext.warguments.minSleep;
            usleep(randomSleep);
        }
        if (kqContext.sparseFactor > 1) {
            offset +=  (kqContext.sparseFactor * iosize);
        } else {
            offset += iosize;
        }
        if (!finalWrite) {
            sizeRemaining -= (iosize);
        } else {
            sizeRemaining = 0;
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     :   kqIoBufferedDirectRandkqWrite
 *
 * Description  :   This function performs random write for buffered and
 *                  direct I/O.
 *
 * Parameters   :
 *      1. fd           File descriptor.
 *      2. baseOffset   Base Offset from where next I/O operation will start.
 *      3. size         Total size of the I/O operation.
 * Return Value :
 *                      Returns SUCCESS if write was successful.
 *                      Returns FAILURE if write failed.
 */
int kqIoBufferedDirectRandkqWrite(int fd, uint64 baseOffset, uint64 size)
{
    uint64  i           = 0;
    uint64 skip         = 0;
    uint64 count        = 0;
    uint64  offset;
    char   *buffer;
    uint32 randomSleep;
    uint64 iosize;
    uint64 offsetMark;
    uint64 sizeRemaining;

    debug("%s : Baseoffset  %"PRIu64" size %"PRIu64"\n", __FUNCTION__,
            baseOffset, size);


    if (g_randomIosize) {
        if ((buffer = kqIoFillPattern(kqContext.warguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoFillPattern(kqContext.warguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    /* Do the I/O for (g_globalArrayIteration * g_sumOfIosizeArray) */
    offsetMark = baseOffset;
    for (count = 0; count < g_globalArrayIteration; count++) {
        for (i = 0; i != g_globalArrayCount; i++) {
            offset = g_iosizeArray[i][0] + offsetMark;
            skip = offset % g_patternLen;
            iosize = g_iosizeArray[i][1];
            if (kqIoCommonWrite(fd, offset, iosize,
                        buffer + skip) == FAILURE) {
                if (buffer != NULL)
                    free(buffer);
                return FAILURE;
            }
            if (!g_randomSleep) {
                if (kqContext.warguments.sleep != 0) {
                    usleep(kqContext.warguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.warguments.maxSleep
                            + 1 - kqContext.warguments.minSleep)) +
                    kqContext.warguments.minSleep;
                usleep(randomSleep);
            }
        }
        offsetMark += g_offsetMark;
    }
    sizeRemaining = (size - (g_globalArrayIteration * g_sumOfIosizeArray));
    if (sizeRemaining != 0) {
        for (i = 0; i < g_globalSubArrayCount; i++) {
            offset =  g_iosizeSubArray[i][0] + baseOffset;
            skip = offset % g_patternLen;
            iosize =  g_iosizeSubArray[i][1];
            if (kqIoCommonWrite(fd, offset, iosize,
                        buffer + skip) == FAILURE) {
                if (buffer != NULL)
                    free(buffer);
                return FAILURE;
            }
            if (!g_randomSleep) {
                if (kqContext.warguments.sleep != 0) {
                    usleep(kqContext.warguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.warguments.maxSleep
                            + 1 - kqContext.warguments.minSleep)) +
                    kqContext.warguments.minSleep;
                usleep(randomSleep);
            }
            sizeRemaining -= g_iosizeSubArray[i][1];
        }
    }
    if (g_firstThreadExtraSize != 0) {
        offset = g_sumOfIosizeSubArray + (g_globalArrayIteration *
                    g_sumOfIosizeArray);
        skip = offset % g_patternLen;
        if (kqIoCommonWrite(fd, offset, g_firstThreadExtraSize,
                    buffer + skip) == FAILURE) {
            if (buffer != NULL)
                free(buffer);
            return FAILURE;
        }
        if (!g_randomSleep) {
            if (kqContext.warguments.sleep != 0) {
                usleep(kqContext.warguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.warguments.maxSleep
                        + 1 - kqContext.warguments.minSleep)) +
                kqContext.warguments.minSleep;
            usleep(randomSleep);
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     : kqIoMmapSeqWrite
 *
 * Description  : This function performs mmap sequential write.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. count    No. of I/O operations.
 * Return Value :
 *                  Returns SUCCESS if write was successful.
 *                  Returns FAILURE if write failed.
 */
int kqIoMmapSeqWrite(int fd, uint64 fileOffset, uint64 size)
{
    uint64 sizeRemaining    = size;
    void *file_memory       = NULL;
    char *buffer            = NULL;
    uint64 skip             = 0;
    uint64 pageEnd          = 0;
    uint64 pageStart        = 0;
    bool finalWrite         = false;
    uint64  i               = 0;
    uint64 iosize;
    uint64 inpageOffset;
    uint32 randomSleep;

    debug("%s\n", __FUNCTION__);

    if (g_randomIosize) {
        if ((buffer = kqIoFillPattern(kqContext.warguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoFillPattern(kqContext.warguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    while (sizeRemaining != 0) {
        if (g_randomIosize) {
            iosize = g_iosizeArray[i][1];
            i++;
            if (i == g_globalArrayCount) {
                i = 0;
            }
        } else {
            iosize = kqContext.warguments.blockSize;
        }
        pageStart = fileOffset / PAGE_SIZE;
        if ((iosize) <= sizeRemaining) {
            pageEnd = (fileOffset + iosize + PAGE_SIZE - 1) /
                        PAGE_SIZE;
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", fileOffset, pageStart, iosize);
        } else {
            pageEnd = (fileOffset + sizeRemaining + PAGE_SIZE - 1) /
                        PAGE_SIZE;
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                        PRIu64"\n", fileOffset, pageStart, sizeRemaining);
            finalWrite = true;
        }
        inpageOffset = fileOffset % PAGE_SIZE;
        file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ |
                PROT_WRITE, MAP_SHARED, fd,
                (pageStart * PAGE_SIZE));
        if (file_memory == MAP_FAILED) {
            error("mmap failed ! %s\n", strerror(errno));
            if (buffer != NULL) {
                free(buffer);
            }
            return FAILURE;
        }
        skip = fileOffset % g_patternLen;
        if (kqContext.sparseFactor > 1) {
            fileOffset +=  (kqContext.sparseFactor * iosize);
        } else {
            fileOffset += iosize;
        }
        if (!finalWrite) {
            memcpy((char *)(file_memory + inpageOffset), buffer + skip,
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            sizeRemaining -= iosize;
        }  else {
            memcpy((char *)(file_memory + inpageOffset), buffer + skip,
                    sizeRemaining);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            sizeRemaining = 0;
        }
        if (!g_randomSleep) {
            if (kqContext.warguments.sleep != 0) {
                usleep(kqContext.warguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.warguments.maxSleep
                        + 1 - kqContext.warguments.minSleep)) +
                kqContext.warguments.minSleep;
            usleep(randomSleep);
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     : kqIoMmapRandkqWrite
 *
 * Description  : This function performs mmap random write.
 *
 * Parameters   :
 *      1. fd           File descriptor.
 *      2. baseOffset   Base Offset from where next I/O operation will start.
 *      3. size         Total size of the I/O operation.
 * Return Value :
 *                      Returns SUCCESS if write was successful.
 *                      Returns FAILURE if write failed.
 */
int kqIoMmapRandkqWrite(int fd, uint64 baseOffset, uint64 size)
{
    uint64  offset;
    void    *file_memory    = NULL;
    char    *buffer         = NULL;
    uint64  skip            = 0;
    uint64  inpageOffset    = 0;
    uint64  pageStart       = 0;
    uint64  pageEnd         = 0;
    uint32 randomSleep;
    uint64 count = 0;
    uint64 i = 0;
    uint64 offsetMark;
    uint64 iosize;
    uint64 sizeRemaining;

    debug("%s : Baseoffset  %"PRIu64" size %"PRIu64"\n", __FUNCTION__,
            baseOffset, size);

    if (g_randomIosize) {
        if ((buffer = kqIoFillPattern(kqContext.warguments.maxBlockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    } else {
        if ((buffer = kqIoFillPattern(kqContext.warguments.blockSize,
                        g_patternLen)) == NULL) {
            return FAILURE;
        }
    }
    /* Do the I/O for (g_globalArrayIteration * g_sumOfIosizeArray) */
    offsetMark = baseOffset;
    for (count = 0; count < g_globalArrayIteration; count++) {
        for (i = 0; i != g_globalArrayCount; i++) {
            offset = g_iosizeArray[i][0] + offsetMark;
            skip = offset % g_patternLen;
            iosize = g_iosizeArray[i][1];
            pageStart = offset / PAGE_SIZE;
            pageEnd = (offset + iosize + PAGE_SIZE -1) /
                PAGE_SIZE;
            inpageOffset = offset % PAGE_SIZE;
            file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ |
                    PROT_WRITE, MAP_SHARED, fd,
                    (pageStart * PAGE_SIZE));
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", offset, pageStart, iosize);
            if (file_memory == MAP_FAILED) {
                error("mmap failed ! %s\n", strerror(errno));
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            memcpy((char *)(file_memory + inpageOffset), buffer + skip,
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            if (!g_randomSleep) {
                if (kqContext.warguments.sleep != 0) {
                    usleep(kqContext.warguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.warguments.maxSleep
                            + 1 - kqContext.warguments.minSleep)) +
                    kqContext.warguments.minSleep;
                usleep(randomSleep);
            }
        }
        offsetMark += g_offsetMark;
    }
    sizeRemaining = (size - (g_globalArrayIteration * g_sumOfIosizeArray));
    if (sizeRemaining != 0) {
        for (i = 0; i < g_globalSubArrayCount; i++) {
            offset =  g_iosizeSubArray[i][0] + baseOffset;
            iosize =  g_iosizeSubArray[i][1];
            skip = offset % g_patternLen;
            pageStart = offset / PAGE_SIZE;
            pageEnd = (offset + iosize + PAGE_SIZE -1) /
                        PAGE_SIZE;
            inpageOffset = offset % PAGE_SIZE;
            file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ |
                             PROT_WRITE, MAP_SHARED, fd,(pageStart * PAGE_SIZE));
            debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                    PRIu64"\n", offset, pageStart, iosize);
            if (file_memory == MAP_FAILED) {
                error("mmap failed ! %s\n", strerror(errno));
                if (buffer != NULL) {
                    free(buffer);
                }
                return FAILURE;
            }
            memcpy((char *)(file_memory + inpageOffset), buffer + skip,
                    iosize);
            munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
            if (!g_randomSleep) {
                if (kqContext.warguments.sleep != 0) {
                    usleep(kqContext.warguments.sleep);
                }
            } else {
                randomSleep = (rand() % (kqContext.warguments.maxSleep
                            + 1 - kqContext.warguments.minSleep)) +
                    kqContext.warguments.minSleep;
                usleep(randomSleep);
            }
            sizeRemaining -= iosize;
        }
    }
    if (g_firstThreadExtraSize != 0) {
        offset = g_sumOfIosizeSubArray + (g_globalArrayIteration *
                    g_sumOfIosizeArray);
        skip = offset % g_patternLen;
        pageStart = offset / PAGE_SIZE;
        pageEnd = (offset + g_firstThreadExtraSize + PAGE_SIZE -1) /
            PAGE_SIZE;
        inpageOffset = offset % PAGE_SIZE;
        file_memory = mmap(0, (pageEnd - pageStart) * PAGE_SIZE, PROT_READ |
                PROT_WRITE, MAP_SHARED, fd,
                (pageStart * PAGE_SIZE));
        debug("mmap          offset %10"PRIu64" page   %10"PRIu64" size %10"
                PRIu64"\n", offset, pageStart, iosize);
        if (file_memory == MAP_FAILED) {
            error("mmap failed ! %s\n", strerror(errno));
            if (buffer != NULL) {
                free(buffer);
            }
            return FAILURE;
        }
        memcpy((char *)(file_memory + inpageOffset), buffer + skip,
                g_firstThreadExtraSize);
        munmap(file_memory, (pageEnd - pageStart) * PAGE_SIZE);
        if (!g_randomSleep) {
            if (kqContext.warguments.sleep != 0) {
                usleep(kqContext.warguments.sleep);
            }
        } else {
            randomSleep = (rand() % (kqContext.warguments.maxSleep
                        + 1 - kqContext.warguments.minSleep)) +
                kqContext.warguments.minSleep;
            usleep(randomSleep);
        }
    }
    free(buffer);
    return SUCCESS;
}


/*
 * Function     : kqIoMmapRead
 *
 * Description  : This function performs mmap read.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which reads needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls Mmap read function according to the sequence.
 *                  Returns FAILURE otherwise.
 */
int kqIoMmapRead(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.readMmapSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.readMmapRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoBufferedRead
 *
 * Description  : This function performs buffered read.
 *
 * Parameters   :
 *      1. fd      File descriptor.
 *      2. offse   Offset from which read needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                 Calls Buffered I/O read function according to the sequence.
 *                 Returns FAILURE otherwise.
 */
int kqIoBufferedRead(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.readBufferedSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.readBufferedRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoDirectRead
 *
 * Description  : This function performs direct read.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which read needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls Direct I/O read function according to the sequence.
 *                  Returns FAILURE otherwise.
 */
int kqIoDirectRead(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.readDirectSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.readDirectRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoMmapWrite
 *
 * Description  : This function performs mmap write.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls Mmap write function according to the sequence.
 *                  Returns FAILURE otherwise.
 */
int kqIoMmapWrite(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.writeMmapSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.writeMmapRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoDirectWrite
 *
 * Description  : This function performs direct write.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls Direct I/O write function according to the
 *                  sequence.
 *                  Returns FAILURE otherwise.
 */
int kqIoDirectWrite(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.writeDirectSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.writeDirectRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoBufferedWrite
 *
 * Description  : This function performs buffered write.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls Buffered I/O write function according to the sequence.
 *                  Returns FAILURE otherwise.
 */
int kqIoBufferedWrite(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.sequence == IO_SEQUENCE) {
        return fops.writeBufferedSeq(fd, offset, size);
    } else if (kqContext.sequence == IO_RANDOM) {
        return fops.writeBufferedRandom(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoWrite
 *
 * Description  : This function performs write.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls write function according to the I/O method .
 *                  Returns FAILURE otherwise.
 */
int kqIoWrite(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.warguments.rwflag == IO_MMAP) {
        return kqIoMmapWrite(fd, offset,size);
    } else if (kqContext.warguments.rwflag == IO_DIRECT) {
        return kqIoDirectWrite(fd, offset, size);
    } else if (kqContext.warguments.rwflag == IO_BUFFERED) {
        return kqIoBufferedWrite(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function     : kqIoRead
 *
 * Description  : This function performs read.
 *
 * Parameters   :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which write needs to be started.
 *      3. size     Total size for the I/O operations.
 * Return Value :
 *                  Calls read function according to the I/O method .
 *                  Returns FAILURE otherwise.
 */
int kqIoRead(int fd, uint64 offset, uint64 size)
{

    debug("%s\n", __FUNCTION__);

    if (kqContext.rarguments.rwflag == IO_MMAP) {
        return kqIoMmapRead(fd, offset, size);
    } else if (kqContext.rarguments.rwflag == IO_DIRECT) {
        return kqIoDirectRead(fd, offset, size);
    } else if (kqContext.rarguments.rwflag == IO_BUFFERED) {
        return kqIoBufferedRead(fd, offset, size);
    }
    return FAILURE;
}


/*
 * Function    : kqIoReportCorruption
 *
 * Description : This function reports corruption.
 */
void kqIoReportCorruption(uint64 offset, int size, char *buffer,
        char *pattern, uint64 skip)
{
    FILE *fp;

    debug("%s\n", __FUNCTION__);

    fp = fopen(kqContext.corruptionFile, "a");
    fprintf(fp,"%.8s..%.8s (%.10"PRIu64", %.10"PRIu64")\n",buffer,
            (buffer + size - 8), offset, offset + size);
    fclose(fp);
}


/*
 * Function     :    kqIoVerifyBlock
 *
 * Description  :    This function verifies block read
 *
 * Parameters   :
 *      1. offset   Offset with file.
 *      2. buffer   Read buffer
 * Return Value :
 *                  Returns SUCCESS if the block is verified.
 *                  Returns FAILURE if the verification failed.
 *
 */
int kqIoVerifyBlock(uint64 offset, char *buffer, uint64 iosize)
{
    uint64 skip =0;

    debug("%s\n", __FUNCTION__);

    skip = offset % g_patternLen;
    if (memcmp(buffer, g_patternBuffer + skip, iosize)
            == 0) {
        return SUCCESS;
    } else {
        pthread_mutex_lock(&g_mutex);
        kqIoPerf.failedVerifyOps++;
        kqIoReportCorruption(offset, iosize , buffer,
                g_patternBuffer, skip);
        pthread_mutex_unlock(&g_mutex);
        return FAILURE;
    }
}


/*
 * Function     : kqIoVerifyInit
 *
 * Description  : This function intializes verification structures.
 *
 * Parameters   :
 * Return Value :
 *                  Returns SUCCESS if the verification structures
 *                  intilizes successfully.
 *                  Returns FAILURE  if the verification structure
 *                  intilaization fails.
 */
int kqIoVerifyInit()
{

    debug("%s\n", __FUNCTION__);

    if (g_randomIosize) {
        if (kqContext.rarguments.maxBlockSize <= g_patternLen) {
            if ((g_patternBuffer = kqIoCommonAllocateBuffer(g_patternLen *
                            sizeof(char) * 2))
                    == NULL) {
                return FAILURE;
            }
            kqIoFillBuffer(g_patternBuffer, g_pattern, g_patternLen * 2);
        } else {
            if ((g_patternBuffer = kqIoCommonAllocateBuffer(
                            kqContext.rarguments.maxBlockSize *
                            sizeof(char) * 2)) == NULL) {
                return FAILURE;
            }
            kqIoFillBuffer(g_patternBuffer, g_pattern,
                    kqContext.rarguments.maxBlockSize * 2);
        }
    } else {
        if (kqContext.rarguments.blockSize <= g_patternLen) {
            if ((g_patternBuffer = kqIoCommonAllocateBuffer(g_patternLen *
                            sizeof(char) * 2))
                    == NULL) {
                return FAILURE;
            }
            kqIoFillBuffer(g_patternBuffer, g_pattern, g_patternLen * 2);
        } else {
            if ((g_patternBuffer = kqIoCommonAllocateBuffer(
                            kqContext.rarguments.blockSize *
                            sizeof(char) * 2)) == NULL) {
                return FAILURE;
            }
            kqIoFillBuffer(g_patternBuffer, g_pattern,
                    kqContext.rarguments.blockSize * 2);

        }
    }
    kqIoPerf.failedVerifyOps = 0;
    sprintf(kqContext.corruptionFile,"corruption_log_%d", getpid());
    debug("using corruption log file %s\n", kqContext.corruptionFile);
    g_verifyInitialised = TRUE;
    return SUCCESS;
}


/*
 * Function    : kqExecuteTcThread
 *
 * Description : This function executes the thead.
 */
void *kqExecuteTcThread(void *argument)
{
    struct kqIoStat *kqIoStat = argument;
    int16 opcode;
    int ret;

    debug("%s\n", __FUNCTION__);

    opcode = kqContext.opcode;
    if (opcode == OP_WRITE) {
        if (fops.openOutput(&(kqIoStat->outFileDesc)) == FAILURE) {
            exit(-1);
        }
        kqIoStat->writeStartTime = kqTimeElapsed();
        if (kqContext.sequence == IO_RANDOM) {
            ret = kqIoWrite(kqIoStat->outFileDesc,
                    kqIoStat->start.baseOffset, kqIoStat->size);
        } else {
            ret = kqIoWrite(kqIoStat->outFileDesc, kqIoStat->start.offset,
                    kqIoStat->size);
        }
        if (ret == FAILURE) {
            g_status = FAILURE;
            error("Write failed\n");
            exit(FAILURE);
        }
        kqIoStat->writeEndTime = kqTimeElapsed();
        close(kqIoStat->outFileDesc);
        if (kqContext.verify == TRUE) {
            kqContext.rarguments.offset =  kqContext.warguments.offset;
            kqContext.rarguments.count  =  kqContext.warguments.count;
            kqContext.rarguments.size   =  kqContext.warguments.size;
            kqContext.rarguments.blockSize = kqContext.warguments.blockSize;
            kqContext.rarguments.minBlockSize =
                kqContext.warguments.minBlockSize;
            kqContext.rarguments.maxBlockSize =
                kqContext.warguments.maxBlockSize;
            kqContext.rarguments.minSleep = kqContext.warguments.minSleep;
            kqContext.rarguments.maxSleep = kqContext.warguments.maxSleep;
            if (g_verifyInitialised == FALSE) {
                debug("Initialising the verification structures\n");
                pthread_mutex_lock(&g_mutex);
                kqIoVerifyInit();
                pthread_mutex_unlock(&g_mutex);
            }
            strcpy(kqContext.inputFile, kqContext.outputFile);
            if (fops.openInput(&(kqIoStat->inpFileDesc)) == FAILURE) {
                exit(-1);
            }
            kqIoStat->readStartTime = kqTimeElapsed();
            if (kqContext.sequence == IO_RANDOM) {
                kqIoRead(kqIoStat->inpFileDesc,
                        kqIoStat->start.baseOffset, kqIoStat->size);
            } else {
                kqIoRead(kqIoStat->inpFileDesc, kqIoStat->start.offset,
                        kqIoStat->size);
            }
            kqIoStat->readEndTime = kqTimeElapsed();
            close(kqIoStat->inpFileDesc);
        }
    } else {
        if (fops.openInput(&(kqIoStat->inpFileDesc)) == FAILURE) {
            exit(-1);
        }
        if (g_verifyInitialised == FALSE) {
            debug("Initialising the verification structures\n");
            pthread_mutex_lock(&g_mutex);
            kqIoVerifyInit();
            pthread_mutex_unlock(&g_mutex);
        }
        kqIoStat->readStartTime = kqTimeElapsed();
        if (kqContext.sequence == IO_RANDOM) {
            ret = kqIoRead(kqIoStat->inpFileDesc,
                    kqIoStat->start.baseOffset, kqIoStat->size);
        } else {
            ret = kqIoRead(kqIoStat->inpFileDesc, kqIoStat->start.offset,
                    kqIoStat->size);
        }
        if (ret == FAILURE) {
            g_status = FAILURE;
            error("Read failed\n");
            exit(FAILURE);
        }
        kqIoStat->readEndTime = kqTimeElapsed();
        close(kqIoStat->inpFileDesc);
    }
    return NULL; /* to avoid warning */
}


/*
 * Function    : kqExecuteTc
 *
 * Description : This function sets up the enviroment for threads.
 */
void kqExecuteTc(void)
{
    pthread_t threads[16];
    int threadCntr          = 0;
    uint64 offset           = 0;
    int noOfThreads         = 0;
    int blocksPerThread     = 0;
    uint64 blocksExtra      = 0;
    uint64 fileSize         = 0;
    uint64 sizePerThread    = 0;
    uint64 sizeExtra        = 0;
    uint64 directIoOps      = 0;
    uint64 i                = 0;
    int fd;
    uint64 directIoOpsPerThread;
    uint64 directIoOpsExtra;

    debug("%s\n", __FUNCTION__);

    if (kqContext.opcode == OP_WRITE) {
        fd = open(kqContext.outputFile, O_RDWR | O_CREAT, S_IRWXU | S_IRWXG |
                S_IRWXO);
        if (fd == -1) {
            error("Could not open the output file. %s\n", strerror(errno));
            exit(-1);
        }
        debug("Marking the end of the file at %"PRIu64"\n", (
                    (kqContext.warguments.size * kqContext.sparseFactor) +
                    kqContext.warguments.offset) - 1);
        if (lseek(fd, ((kqContext.warguments.size * kqContext.sparseFactor) +
                        kqContext.warguments.offset) - 1, SEEK_SET) == -1) {
            error("lseek failed \n", strerror(errno));
            exit(ESPIPE);
        }
        if (write(fd, "", 1) == -1) {
            error("write failed %s exiting...\n", strerror(errno));
            exit(-1);
        }
        close(fd);
        /* Get the sector size for directio. */
        g_sectorSize = kqIoGetSectorSize(kqContext.outputFile);
        /* Calculate the size for each thread for writing. */
        noOfThreads = kqContext.numWriteThreads;
        offset = kqContext.warguments.offset;
        if (g_randomIosize) {
            sizePerThread = kqContext.warguments.size / noOfThreads;
            sizeExtra = kqContext.warguments.size % noOfThreads;
        } else {
            if (kqContext.warguments.rwflag == IO_DIRECT) {
                directIoOps = kqContext.warguments.size / g_sectorSize;
                directIoOpsPerThread = directIoOps / noOfThreads;
                directIoOpsExtra = directIoOps % noOfThreads;
                sizePerThread = directIoOpsPerThread *
                                kqContext.warguments.blockSize;
                sizeExtra = directIoOpsExtra * kqContext.warguments.blockSize;
            } else {
                blocksPerThread = (kqContext.warguments.count / noOfThreads);
                blocksExtra = (kqContext.warguments.count % noOfThreads);
                sizePerThread = blocksPerThread *
                                 kqContext.warguments.blockSize;
                sizeExtra = blocksExtra * kqContext.warguments.blockSize;
            }
        }
        createGlobalArray(kqContext.warguments.size);
    } else {
        /* Get the sector size for directio. */
        g_sectorSize = kqIoGetSectorSize(kqContext.inputFile);
        /* Calculate the size for each thread for reading. */
        noOfThreads = kqContext.numReadThreads;
        offset = kqContext.rarguments.offset;
        if (g_randomIosize) {
            sizePerThread = kqContext.rarguments.size / noOfThreads;
            sizeExtra = kqContext.rarguments.size % noOfThreads;
        } else {
            if (kqContext.rarguments.rwflag == IO_DIRECT) {
                directIoOps = kqContext.rarguments.size / g_sectorSize;
                directIoOpsPerThread = directIoOps / noOfThreads;
                directIoOpsExtra = directIoOps % noOfThreads;
                sizePerThread = directIoOpsPerThread *
                                kqContext.rarguments.blockSize;
                sizeExtra = directIoOpsExtra * kqContext.rarguments.blockSize;
            }
            blocksPerThread = (kqContext.rarguments.count / noOfThreads);
            blocksExtra = (kqContext.rarguments.count % noOfThreads);
            sizePerThread = blocksPerThread * kqContext.rarguments.blockSize;
            sizeExtra = blocksExtra * kqContext.rarguments.blockSize;
        }
        createGlobalArray(kqContext.rarguments.size);
        if (fops.openInput(&fd) == FAILURE) {
            exit(-1);
        }
        if ((fileSize = lseek(fd, 0, SEEK_END)) == -1) {
            error("lseek failed \n", strerror(errno));
            exit(ESPIPE);
        }
        if (((kqContext.rarguments.size * kqContext.sparseFactor) +
                    kqContext.rarguments.offset) != fileSize) {
            error("The given size[%"PRIu64"] do not match the original file"
                    "size[%"PRIu64"]\n",((kqContext.rarguments.size *
                            kqContext.sparseFactor) +
                        kqContext.rarguments.offset),
                    fileSize);
            exit(EINVAL);
        }
    }
    while (noOfThreads > threadCntr) {
        if (sizeExtra != 0) {
            kqIoStats[threadCntr].size = sizePerThread + sizeExtra;
        } else {
            kqIoStats[threadCntr].size = sizePerThread;
        }
        if (kqContext.sequence == IO_RANDOM) {
            kqIoStats[threadCntr].start.baseOffset = offset;
            debug("Thread %2d offset  %10"PRIu64" size %10"PRIu64"\n",
                    threadCntr, kqIoStats[threadCntr].start.baseOffset,
                    kqIoStats[threadCntr].size);
        } else {
            kqIoStats[threadCntr].start.offset = offset;
            debug("Thread %2d offset %10"PRIu64" size %10"PRIu64"\n",
                    threadCntr, kqIoStats[threadCntr].start.offset,
                    kqIoStats[threadCntr].size);
        }
        offset += kqIoStats[threadCntr].size * kqContext.sparseFactor;
        if ((pthread_create(&threads[threadCntr], NULL, kqExecuteTcThread,
                        (void *)&kqIoStats[threadCntr])) != 0) {
            error("Thread creation failed %s \n", strerror(errno));
            exit(EINVAL);
        }
        threadCntr++;
        sizeExtra = 0;
    }
    while (threadCntr) {
        pthread_join(threads[threadCntr -1], NULL);
        threadCntr--;
    }
    if (kqIoPerf.failedVerifyOps != 0) {
        error("Varification of one or more block failed failed \n");
        exit(-1);
    }
    if (g_status == SUCCESS) {
        kqCollectIoStats();
        kqReportResults();
    }
    if (g_patternBuffer != NULL) {
        free(g_patternBuffer);
    }
    for (i = 0; i < g_globalArrayCount; i++) {
        free(g_iosizeArray[i]);
    }
    for (i = 0; i < g_globalSubArrayCount; i++) {
        free(g_iosizeSubArray[i]);
    }
    if (g_iosizeSubArray != NULL) {
        free(g_iosizeSubArray);
    }
    if (g_iosizeArray != NULL) {
        free(g_iosizeArray);
    }
    debug("Processing Finished!!!!!!!!!!!!\n");
    exit(SUCCESS);
}
