#ifndef  _io_test_h
#define  _io_test_h

#define    _FILE_OFFSET_BITS    64
#define    _THREAD_SAFE
#define    _LARGEFILE_SOURCE

#if defined(linux)
    #include "linux/linuxinclude.h"
#elif defined(Windows)
    #include "windows/wininclude.h"
#elif defined(macosx)
    #include "macosx/macosxinclude.h"
#endif

#define        FAILURE          1 /* to indicate failure of an operation */
#define        SUCCESS          0 /* to indicate success of an operation */

#define        TRUE             1
#define        FALSE            0

#define        NO_TIMEOUT       -1 /* to indicate no timeout value is given */

/* Data Type Declarations */
typedef int64_t         int64;
typedef int32_t         int32;
typedef int16_t         int16;
typedef uint16_t        uint16;
typedef uint32_t        uint32;
typedef uint64_t        uint64;

/* File operations structure */
struct kqFileOperations {
    int (*openInput)            (int *fd);
    int (*openOutput)           (int *fd);
    int (*readDirectSeq)        (int fd, uint64 offset, uint64 count);
    int (*readMmapSeq)          (int fd, uint64 offset, uint64 count);
    int (*readBufferedSeq)      (int fd, uint64 offset, uint64 count);
    int (*writeDirectSeq)       (int fd, uint64 offset, uint64 count);
    int (*writeMmapSeq)         (int fd, uint64 offset, uint64 count);
    int (*writeBufferedSeq)     (int fd, uint64 offset, uint64 count);
    int (*readDirectRandom)     (int fd, uint64 startIndex, uint64 count);
    int (*readBufferedRandom)   (int fd, uint64 startIndex, uint64 count);
    int (*readMmapRandom)       (int fd, uint64 startIndex, uint64 count);
    int (*writeBufferedRandom)  (int fd, uint64 startIndex, uint64 count);
    int (*writeMmapRandom)      (int fd, uint64 startIndex, uint64 count);
    int (*writeDirectRandom)    (int fd, uint64 startIndex, uint64 count);
};


#if defined(linux) || defined(Windows) || defined (macosx)
static const char* const \
        g_short_options = "hvo:i:w:r:y:x:q:t:P:F:f:k:T:R:hu:p:Vs:S:H:n:";

static const struct option g_long_options[] = {
    { "help",       0,    NULL,    'h'},    /* display help */
    { "verbose",    0,    NULL,    'v' },   /* display verbose */
    { "output",     1,    NULL,    'o'},    /* output file */
    { "input",      1,    NULL,    'i'},    /* input file */
    { "verify",     0,    NULL,    'V'},    /* enable verify */
    { "write",      2,    NULL,    'w'},    /* specify write arguments */
    { "read",       2,    NULL,    'r'},    /* specify read arguments */
    { "wthreads",   1,    NULL,    'y'},    /* number of write threads */
    { "rthreads",   1,    NULL,    'x'},    /* number of read threads */
    { "sequence",   1,    NULL,    'q'},    /* random|non-random */
    { "type",       1,    NULL,    't'},    /* sparse|non-sparse */
    { "Pattern",    1,    NULL,    'F'},    /* pattern in file */
    { "pattern",    1,    NULL,    'P'},    /* pattern in "string" */
    { "rflags",     1,    NULL,    'f'},    /* mmap|direct|buffered */
    { "wflags",     1,    NULL,    'k'},    /* mmap|direct|buffered */
    { "timeout",    1,    NULL,    'T'},    /* seconds[.milliseconds]*/
    { "rf",         1,    NULL,    'R'},    /* replication factor*/
    { "host",       0,    NULL,    'H'},    /* host name */
    { "username",   1,    NULL,    'u'},    /* username */
    { "password",   1,    NULL,    'p'},    /* password */
    { "sparseness", 1,    NULL,    's'},    /* sparseness */
    { "seed",       1,    NULL,    'S'},    /* seed */
    { "nice",       1,    NULL,    'n'},    /* nice value */
    { NULL,         0,    NULL,    0}       /* Required at end of array. */
};
#endif

int     kqValidateFilename(char *path);
void    kqInitialiseDefaultContext(void);
void    kqReportResults();
void    kqDisplayContext();
void    createGlobalArray(uint64);
void    kqNiceness();
void    kqExecuteTc();
int64   kqTimeElapsed();
void    kqDefaultPattern();

int     kqIoMmapSeqWrite(int fd, uint64 offset, uint64 count);
int     kqIoMmapRandkqWrite(int fd, uint64 offset, uint64 count);
int     kqIoMmapSeqRead(int fd, uint64 offset, uint64 count);
int     kqIoMmapRandkqRead(int fd, uint64 offset, uint64 count);

int     kqIoBufferedDirectSeqRead(int fd, uint64 offset, uint64 count);
int     kqIoBufferedDirectRandkqRead(int fd, uint64 offset, uint64 count);
int     kqIoBufferedDirectSeqWrite(int fd, uint64 offset, uint64 count);
int     kqIoBufferedDirectRandkqWrite(int fd, uint64 offset, uint64 count);

int     kqIoVerifyBlock(uint64 off, char *buffer, uint64 iosize);

int     kqIoOpenInputFile();
int     kqIoOpenOutputFile();

int     kqIoMmapRead(int fd, uint64 offset, uint64 count);
int     kqIoMmapWrite(int fd, uint64 offset, uint64 count);

int     kqIoBufferedRead();
int     kqIoBufferedWrite();

int     kqIoDirectRead();
int     kqIoDirectWrite();

char*   kqIoCommonAllocateBuffer(int size);
char*   kqIoFillPattern(uint64 ioSize, uint32 patternLe);
char*   kqIoAllocReadBuffer(uint64, uint32);

int     kqIoCommonRead(int fd, uint64 offset, uint64  size, char *buffer);
int     kqIoCommonWrite(int fd, uint64 offset, uint64 size, char *pattern);
int     kqIoGetSectorSize(char *);


int     kqCommonAddTimeout();
void    debug(const char *format, ...);
void    error(const char *format, ...);


char    *g_pattern;                 /* pattern to be written in file */
uint32  g_patternLen;               /* pattern length */
char    *g_patternBuffer;           /* pattern buffer of block size*/
int     g_verbose_level;            /* level of verbosity */
int     g_sectorSize;
bool    g_randomIosize;   
bool    g_randomSleep;   

typedef enum kqIoMethod {
    IO_MMAP,
    IO_DIRECT,
    IO_BUFFERED,
} kqIoMethod;

typedef enum kqIoType {
    IO_SPARSE,
    IO_NOSPARSE,
} kqIoType;

typedef enum kqIoSequence {
    IO_SEQUENCE,
    IO_RANDOM,
} kqIoSequence;

/* Global Arguments */
typedef struct kqRwargs {
    uint64      offset;             /* offset to start io from */
    int64       size;               /* size of total io */
    uint64      count;              /* no of iops */
    kqIoMethod  rwflag;             /* direct|mmap|buffered */
    uint64      blockSize;          /* io block size */
    uint64      minBlockSize;       /* lower limit for io block size */
    uint64      maxBlockSize;       /* upper limit for io block size */
    int64       sleep;              /* sleep between io ops */
    int64       minSleep;           /* lower limit for sleep between io ops */
    int64       maxSleep;           /* Upper limit for sleep between io ops */
} kqRwargs;

typedef struct    domainAuthenticationToken {
    char *host;
    char *username;
    char *password;
    char *domain;
} auth_token;

typedef enum kqOperation {
    OP_READ  = 0x01,
    OP_WRITE = 0x02,
} kqOperation;

#define        MAX_THREADS    16

struct kqExecutionContext {
    char            inputFile [256];
    char            outputFile[256];
    char            corruptionFile[256];
    uint16          verify;
    kqRwargs        rarguments;
    kqRwargs        warguments;
    uint16          numWriteThreads;
    uint16          numReadThreads;
    kqIoSequence    sequence;
    kqIoType        type;
    double          timeout;
    int16           verbose;
    uint16          replicationFactor;
    auth_token      token;
    int16           opcode;
    int16           sparseFactor;
    uint64          seed;
    int32           nice;
} kqContext;

struct kqIoStat {
    union start {
        uint64    index;
        uint64    offset;
        uint64    baseOffset;
    } start;
    uint64      size;
    uint64      count;
    int         inpFileDesc;
    int         outFileDesc;
    int64       readStartTime;
    int64       readEndTime;
    int64       writeStartTime;
    int64       writeEndTime;
} kqIoStats[MAX_THREADS];

struct kqIoPerf {
    int64       readStartTime;
    int64       readEndTime;
    int64       writeStartTime;
    int64       writeEndTime;
    double      readSpeed;
    double      writeSpeed;
    double      readTotalTime;
    double      writeTotalTime;
    uint64      readOps;
    uint64      writeOps;
    uint64      verifyOps;
    uint64      failedVerifyOps;
} kqIoPerf;

#define BYTES_IN_KB    (1024)
#define BYTES_IN_MB    (1024 * 1024)

#endif /* _io_test_h */
