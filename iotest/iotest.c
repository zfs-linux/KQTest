#include "iotest.h"

#define PAGE_SIZE   getpagesize()

/* Help message for the tool */

char help[] = {
    "Usage: iotest <options>\n"
    "-o|--output  [/path/to/filename|-]     Destination for writing data\n"
    "                                       If specified as '-', the \n"
    "                                       the file is stdout\n"
    "-i|--input   [/path/to/filename|-]     Source for reading data\n"
    "                                       If specified as '-', the \n"
    "                                       the file is stdin\n"
    "-V|--verify                            Enable or disable the algorithmic\n"
    "                                       verification of data\n"
    "-w|--write offset=[],count=[],iosize=[],miniosize=[],maxiosize=[] \n"
    "                                       size=[],sleep=[],minsleep=[]\n"
    "                                       maxsleep=[] \n"
    "-r|--read  offset=[],count=[],iosize=[],miniosize=[],maxiosize=[] \n"
    "                                       size=[],sleep=[],minsleep=[]\n"
    "                                       maxsleep=[]\n"
    "-y|--writethreads [count]              Number of threads to write\n"
    "                                       data. default 1\n"
    "-x|--readthreads [count]               Number of threads to read\n"
    "                                       data. default 1\n"
    "-q|--sequence [random|seq]             Random/sequential\n"
    "                                       reading/writing\n"
    "-t|--type [sparse|non-sparse]          Sparse-ness of a file to be\n"
    "                                       written/read\n"
    "-P|--pattern [string]                  Data-pattern to use in the\n"
    "                                       read/write and verification\n"
    "-F|--Pattern [filename]                Data-pattern to use in the \n"\
    "                                       read/write and verification\n"
    "-f|--rflags  [mmap|directio|bufferedio]\n"
    "-k|--wflags  [mmap|directio|bufferedio]\n"
    "-T|--timeout [seconds]                 Timeout for the operation\n"
    "-v|-vv|--verbose                       verbose flag for more information\n"
    "-s|--sparseness [factor]               Define the sparseness factor\n"
    "-S|--seed [value]                      Define the seed value to be used\n"
    "-n|--nice [value]                      Specify the nice value to be used\n"
    "-h|--help                              Help\n"
};

#define USAGE_MSG  "\tUsage: For usage information type iotest -h\n\n"


/*
 * Function     :   kqGetPattern
 *
 * Description  :   Function to retrieve pattern.
 *
 * Parameters   :
 *      1. pattern  Contains the pattern passed at command line.
 */
static inline void kqGetPattern(char *pattern)
{
    g_pattern = (char *) malloc(sizeof(char) * strlen(pattern));
    if (g_pattern == NULL) {
        error("Memory allocation for pattern failed! %s\n", strerror(errno));
        exit(ENOMEM);
    }
    g_patternLen = strlen(pattern);
    strncpy(g_pattern, pattern, g_patternLen);
    debug("The pattern length is %"PRIu32"\n", g_patternLen);
}


/*
 * Function     : kqGetPatternFromFile
 *
 * Description  : Function to retrieve pattern from file.
 *
 * Parameters   :
 *      1. pattern  File name which contains the pattern.
 */
static inline void kqGetPatternFromFile(char *pattern)
{
    int fd;
    uint64 filesize;

    if ((fd = open(pattern, O_RDONLY)) != -1) {
        filesize = lseek(fd, 0, SEEK_END);
        g_patternLen = filesize;
        g_pattern = mmap(0, g_patternLen, PROT_READ, MAP_SHARED, fd, 0);
        if (g_pattern == MAP_FAILED) {
            error("Pattern could not be read from file! %s\n", strerror(errno));
            exit(EACCES);
        }
        close(fd);
    } else {
        error("Could not be open the pattern file! %s\n", strerror(errno));
        exit(EACCES);
    }
    debug("The pattern length is %"PRIu32"\n", g_patternLen);
}


/*
 * Function     : kqParseRwOptions
 *
 * Description  : Function to parse the read/write arguments supplied
 *
 * Parameters   :
 *      1. options  Contains the read/write option passed at command line.
 *      2. opcode   Value of opcode.
 * Return Value :
 *                  Returns SUCCESS if all the options are parsed
 *                  Exit otherwise.
 */
int kqParseRwOptions(char *options, int16 opcode)
{
    char *str1      = NULL;
    char *str2      = NULL;
    char *token     = NULL;
    char *subtoken  = NULL;
    char *saveptr1  = NULL;
    char *saveptr2  = NULL;
    char *arg       = NULL;
    char *val       = NULL;
    int j;
    int k;

    for (j = 1, str1 = options; ;j++, str1 = NULL) {
        token = strtok_r(str1, ",", &saveptr1);
        if (token == NULL) {
            break;
        }
        for (str2 = token, k = 0; ; str2 = NULL, k++) {
            subtoken = strtok_r(str2, "=", &saveptr2);
            if (subtoken == NULL) {
                break;
            }
            if (arg == NULL) {
                arg = subtoken;
            } else {
                val = subtoken;
            }
            if (k == 2) { /* we need only one parameter to one option*/
                error("Invalid option passed\n");
                printf("%s\n", help);
                exit(EINVAL);
                break;
            }
        }
        if (arg != NULL && val == NULL) {
                error("Invalid read/write option passed \n");
                printf("%s\n", help);
                exit(EINVAL);
        }
        if (strcmp(arg, "offset") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.offset = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.offset = atoll(val);
            }
        } else if (strcmp(arg, "size") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.size = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.size = atoll(val);
            }
        } else if (strcmp(arg, "iosize") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.blockSize = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.blockSize = atoll(val);
            }
        } else if (strcmp(arg, "miniosize") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.minBlockSize = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.minBlockSize = atoll(val);
            }
        } else if (strcmp(arg, "maxiosize") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.maxBlockSize = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.maxBlockSize = atoll(val);
            }
        } else if (strcmp(arg, "count") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.count = atoll(val);
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.count = atoll(val);
            }
        } else if (strcmp(arg, "sleep") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.sleep = atof(val) * 1000000;
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.sleep = atof(val) * 1000000;
            }
        } else if (strcmp(arg, "minsleep") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.minSleep = atof(val) * 1000000;
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.minSleep = atof(val) * 1000000;
            }
        } else if (strcmp(arg, "maxsleep") == 0) {
            if (opcode == OP_READ) {
                kqContext.rarguments.maxSleep = atof(val) * 1000000;
            } else if (opcode == OP_WRITE) {
                kqContext.warguments.maxSleep =  atof(val) * 1000000;
            }
        } else {
            error("Invalid option passed\n");
            exit(EINVAL);
        }
        arg = NULL;
        val = NULL;
    }
    return SUCCESS;
}


/*
 * Function     : kqParseArguments
 *
 * Description  : Function to parse the arguments
 *
 * Parameters   :
 *      1. argc :  Count as passed to the main() function on program invocation.
 *      2. argv :  Array  as passed to the main() function on program
 *      invocation.
 *
 */
void kqParseArguments(int argc, char **argv)
{
    int next_option;

    debug("%s\n", __FUNCTION__);
    do {
        next_option = getopt_long(argc, argv, g_short_options,
                                  g_long_options, NULL);
        switch (next_option) {
        case 'h':    /* -h or --help */
            printf("%s\n", help);
            exit(0);
            break;

        case 'v':    /* -v or  --verbose */
            kqContext.verbose = TRUE;
            g_verbose_level += 1;
            break;

        case 'o':    /* -o or  --output */
            if (!(kqContext.opcode & OP_WRITE)) {
                kqContext.opcode = kqContext.opcode | OP_WRITE;
            }
            if (strncmp(optarg, "-", 1) == 0) {
                strcpy(kqContext.outputFile, optarg);
                debug("Sending o/p to stdout\n");
            } else if (kqValidateFilename(optarg) == SUCCESS) {
                strcpy(kqContext.outputFile, optarg);
            } else {
                error("Error : Invalid O/P filename %s !!\n", optarg);
                exit(EINVAL);
            }
            break;

        case 'i':    /* -i or  --input */
            if (!(kqContext.opcode & OP_READ)) {
                kqContext.opcode = kqContext.opcode | OP_READ;
            }
            debug("I/P filename %s\n", (char *)optarg);
            if (strncmp(optarg, "-", 1) == 0) {
                debug("Taking input from stdin\n");
                strcpy(kqContext.inputFile, optarg);
                } else if (kqValidateFilename(optarg) == SUCCESS) {
                strcpy(kqContext.inputFile, optarg);
            } else {
                error("Error : Invalid I/P filename %s !!\n", optarg);
                exit(EINVAL);
            }
            break;

        case 'V':    /* -V or  --verify */
            kqContext.verify = TRUE;
            break;

        case 's':    /* -s or  --sparseness */
            kqContext.sparseFactor = atoi(optarg);
            if ( kqContext.sparseFactor == 0) {
                error("The sparse factor is incorrect !!\n");
                exit(EINVAL);
            }
            break;

        case 'S':    /* -S or  --seed */
            kqContext.seed = atoll(optarg);
            if (kqContext.seed < 0) {
                error("The seed can not be -ve!!\n");
                exit(EINVAL);
            }
            break;

        case 'n':    /* -n or  --nice */
            kqContext.nice = atoi(optarg);
            if (kqContext.nice == 0) {
                exit(EINVAL);
            }
            break;

        case 'w':    /* -w or  --write */
            kqParseRwOptions(optarg, OP_WRITE);
            if ((kqContext.warguments.blockSize != 0) ||
                    (kqContext.warguments.count != 0)) {
                g_randomIosize = false;
            } else {
                g_randomIosize = true;
            }
            if(!g_randomIosize) {
                if (kqContext.warguments.size == 0) {
                    if ((kqContext.warguments.blockSize == 0 ) &&
                            (kqContext.warguments.count == 0)) {
                        error("Please specify count and block size !!\n");
                        exit(EINVAL);
                    }
                    if (kqContext.warguments.count == 0) {
                        error("Please specify either count or size !!\n");
                        exit(EINVAL);
                    }
                    if (kqContext.warguments.blockSize == 0) {
                        error("Please specify either iosize or size!!\n");
                        exit(EINVAL);
                    }
                    kqContext.warguments.size = kqContext.warguments.count *
                        kqContext.warguments.blockSize;
                }
                if (kqContext.warguments.size != 0) {
                    if ((kqContext.warguments.blockSize == 0) &&
                            (kqContext.warguments.count == 0)) {
                        kqContext.warguments.blockSize = PAGE_SIZE;
                        if ((kqContext.warguments.size % PAGE_SIZE) == 0) {
                            kqContext.warguments.count =
                                kqContext.warguments.size / PAGE_SIZE;
                        } else {
                            error("Please specify size, which is multiple \
                                    of PAGE_SIZE!!\n");
                            exit(EINVAL);
                        }
                    }
                    if ((kqContext.warguments.blockSize != 0) &&
                            (kqContext.warguments.count == 0)) {
                        if ((kqContext.warguments.size %
                                    kqContext.warguments.blockSize) == 0) {
                            kqContext.warguments.count =
                                kqContext.warguments.size /
                                kqContext.warguments.blockSize;
                        } else {
                            error("Please specify valid iosize and size!!\n");
                            exit(EINVAL);
                        }
                    }
                    if ((kqContext.warguments.blockSize == 0) &&
                            (kqContext.warguments.count != 0)) {
                        if ((kqContext.warguments.size %
                                    kqContext.warguments.count) == 0) {
                            kqContext.warguments.blockSize =
                                kqContext.warguments.size /
                                kqContext.warguments.count;
                        } else {
                            error("Please specify valid count and size!!\n");
                            exit(EINVAL);
                        }
                    }
                }
            } else {
                if (kqContext.warguments.count != 0) {
                    error("count is not a valid option with random iosize!!\n");
                    exit(EINVAL);
                }
                if (kqContext.warguments.maxBlockSize <= 0) {
                    error("Please specify valid upper limit for iosize!!\n");
                    exit(EINVAL);
                }
                if (kqContext.warguments.size <= 0) {
                    error("Please specify valid total size !!\n");
                    exit(EINVAL);
                }
            }
            if ((kqContext.warguments.minSleep != 0) ||
                    (kqContext.warguments.maxSleep != 0)) {
                g_randomSleep = true;
            } else {
                g_randomSleep = false;
            }
            break;

        case 'r':    /* -r or  --read */
            kqParseRwOptions(optarg, OP_READ);
            if ((kqContext.rarguments.blockSize != 0) || 
                    (kqContext.rarguments.count != 0)) {
                g_randomIosize = false;
            } else {
                g_randomIosize = true;
            }
            if (!g_randomIosize) {
                if (kqContext.rarguments.size == 0) {
                    if ((kqContext.rarguments.blockSize == 0) &&
                            (kqContext.rarguments.count == 0)) {
                        error("Please specify count and block size !!\n");
                        exit(EINVAL);
                    }
                    if ((kqContext.rarguments.count == 0)) {
                        error("Please specify either count or size !!\n");
                        exit(EINVAL);
                    }
                    if ((kqContext.rarguments.blockSize == 0)) {
                        error("Please specify either iosize or size!!\n");
                        exit(EINVAL);
                    }
                    kqContext.rarguments.size = kqContext.rarguments.count
                        * kqContext.rarguments.blockSize;
                }
                if (kqContext.rarguments.size != 0) {
                    if ((kqContext.rarguments.blockSize == 0) &&
                            (kqContext.rarguments.count == 0)) {
                        kqContext.rarguments.blockSize = PAGE_SIZE;
                        if ((kqContext.rarguments.size % PAGE_SIZE) == 0) {
                            kqContext.rarguments.count =
                                kqContext.rarguments.size / PAGE_SIZE;
                        } else {
                            error("Please specify size, which is multiple \
                                    of PAGE_SIZE!!\n");
                            exit(EINVAL);
                        }
                    }
                    if ((kqContext.rarguments.blockSize != 0) &&
                            (kqContext.rarguments.count == 0)) {
                        if ((kqContext.rarguments.blockSize %
                                    kqContext.rarguments.blockSize) == 0) {
                            kqContext.rarguments.count =
                                kqContext.rarguments.size /
                                kqContext.rarguments.blockSize;
                        } else {
                            error("Please specify valid iosize and size!!\n");
                            exit(EINVAL);
                        }
                    }
                    if ((kqContext.rarguments.blockSize == 0) &&
                            (kqContext.rarguments.count != 0)) {
                        if ((kqContext.rarguments.size %
                                    kqContext.rarguments.count) == 0) {
                            kqContext.rarguments.blockSize =
                                kqContext.rarguments.size /
                                kqContext.rarguments.count;
                        } else {
                            error("Please specify valid count and size!!\n");
                            exit(EINVAL);
                        }
                    }
                }
            } else {
                if (kqContext.rarguments.count != 0) {
                    error("count is not a valid option with random iosize!!\n");
                    exit(EINVAL);
                }
                if (kqContext.rarguments.maxBlockSize <= 0) {
                    error("Please specify valid upper limit for iosize!!\n");
                    exit(EINVAL);
                }
                if (kqContext.rarguments.size <= 0) {
                    error("Please specify valid total size !!\n");
                    exit(EINVAL);
                }
            }
            if ((kqContext.rarguments.minSleep != 0) ||
                    (kqContext.rarguments.maxSleep != 0)) {
                g_randomSleep = true;
            } else {
                g_randomSleep = false;
            }
            break;

        case 'y':    /* -y or  --wthreads */
            kqContext.numWriteThreads = atoi(optarg);
            if (kqContext.numWriteThreads == 0) {
                error("The number of write threads is incorrect !!\n");
                exit(EINVAL);
            }
            break;

        case 'x':    /* -x or  --rthreads */
            kqContext.numReadThreads = atoi(optarg);
            if (kqContext.numReadThreads == 0) {
                error("The number of read threads is incorrect !!\n");
                exit(EINVAL);
            }
            break;

        case 'q':    /* -q or  --sequence */
            if (strcmp(optarg, "seq") == 0) {
                kqContext.sequence = IO_SEQUENCE;
            } else if (strcmp(optarg, "random") == 0) {
                kqContext.sequence = IO_RANDOM;
            } else {
                error("Incorrect sequence option  given. See help\n");
                exit(EINVAL);
            }
            break;

        case 't':    /* -t or  --type */
            if (strcmp(optarg, "sparse") == 0) {
                kqContext.type = IO_SPARSE;
            } else if (strcmp(optarg, "non-sparse") == 0) {
                kqContext.type = IO_NOSPARSE;
            } else {
                error("Incorrect sparse value given. See help\n");
                exit(EINVAL);
            }
            break;

        case 'T':    /* -T or  --timeout */
            kqContext.timeout = atof(optarg);
            if (kqContext.timeout)
                kqCommonAddTimeout();
            break;

        case 'P':    /* -P or  --pattern */
            kqGetPattern(optarg);
            break;

        case 'F':    /* -F or  --Pattern */
            kqGetPatternFromFile(optarg);
            break;

        case 'f':    /* -f or  --rflags */
            if (strcmp(optarg, "mmap") == 0) {
                kqContext.rarguments.rwflag = IO_MMAP;
            } else if (strcmp(optarg, "directio") == 0) {
                kqContext.rarguments.rwflag = IO_DIRECT;
            } else if (strcmp(optarg, "bufferedio") == 0) {
                kqContext.rarguments.rwflag = IO_BUFFERED;
            } else {
                error("Incorrect read flag value given. See help\n");
                exit(EINVAL);
            }
            break;

        case 'k':    /* -k or  --wflags */
            if (strcmp(optarg, "mmap") == 0) {
                kqContext.warguments.rwflag = IO_MMAP;
            } else if (strcmp(optarg, "directio") == 0) {
                kqContext.warguments.rwflag = IO_DIRECT;
            } else if (strcmp(optarg, "bufferedio") == 0) {
                kqContext.warguments.rwflag = IO_BUFFERED;
            } else {
                error("Incorrect write flag value given. See help\n");
                exit(EINVAL);
            }
            break;

        case '?':    /* The user specified an invalid option. */
            fprintf(stderr, "Invalid option given\n");
            fprintf(stdout, USAGE_MSG);
            exit(EINVAL);
            break;

        case -1:     /* Done with options.  */
            break;

        default:     /* Something else: unexpected.  */
            fprintf(stderr, "Invalid option given\n");
            fprintf(stdout, USAGE_MSG);
            exit(EINVAL);
            break;
        }
    } while (next_option != -1);
}


/*
 * Function    : kqDefaultPattern
 *
 * Description : Function to initialize default pattern if pattern file or
 *               string is not specified.
 */
void kqDefaultPattern()
{
    int i;
    char *pattern = NULL;

    debug("%s\n", __FUNCTION__);

    if (g_patternLen == 0) {
        pattern = (char *) malloc(10 * sizeof(char));
        if (pattern == NULL) {
            error("Allocation for default pattern failed. \n");
             exit(ENOMEM);
        } else {
            debug("Allocation for default pattern done successfully. \n");
        }

        for (i = 0; i < 10; i++) {
            sprintf(pattern, "%s%d", pattern, i);
        }
        g_pattern = pattern;
        g_patternLen = strlen(g_pattern);
        debug("Default pattern %s\nlength %"PRIu32"\n", g_pattern, g_patternLen);
    }
}


/*
 * Function    : kqDefaultPattern
 *
 * Description : Function to validate arguments
 */
void kqValidateArguments()
{
    debug("%s\n", __FUNCTION__);

    if (strlen(kqContext.inputFile) && strlen(kqContext.outputFile)) {
        error("Both input and output files are not allowed !\n");
        exit(EINVAL);
    }

    if (kqContext.opcode == OP_READ) {
        if (kqContext.rarguments.rwflag == IO_DIRECT) {
            if (((kqContext.rarguments.blockSize % 512) != 0) ||
               ((kqContext.rarguments.size % 512) != 0)) {
                error("For directio, both  offset iosize should \
                       be multiple of 512 (sector aligned) \n");
                exit(EINVAL);
            }
        }
    } else if (kqContext.opcode == OP_WRITE) {
        if (kqContext.warguments.rwflag == IO_DIRECT) {
            if (((kqContext.warguments.blockSize % 512) != 0) ||
               ((kqContext.warguments.size % 512) != 0)) {
                error("For directio, both  offset iosize should \
                       be multiple of 512 (sector aligned) \n");
                exit(EINVAL);
            }
        }
    } else {
        error("No I/O operation specified !\n");
        exit(EINVAL);
    }
    if ((strcmp(kqContext.inputFile, "-") == 0) &&
        (kqContext.numReadThreads > 1)) {
        error("Having more than one thread for stdin input is not allowed\n");
        exit(EINVAL);
    }

    if ((strcmp(kqContext.outputFile, "-") == 0) &&
        (kqContext.numWriteThreads > 1)) {
        error("Having more than one thread for stdout output is not allowed\n");
        exit(EINVAL);
    }

    if ((strcmp(kqContext.outputFile, "-") == 0)) {
        if (kqContext.verify == TRUE) {
            error("Verify with stdout is not allowed. \n");
            exit(EINVAL);
        }

        if (kqContext.warguments.rwflag == IO_DIRECT) {
            error("Direct I/O for stdout is not allowed\n");
            exit(EINVAL);
        }
        if (kqContext.warguments.rwflag == IO_MMAP) {
            error("Mmap I/O for stdout is not allowed \n");
            exit(EINVAL);
        }
        if (kqContext.sequence == IO_RANDOM) {
            error("Random sequence for stdout is not allowed\n");
            exit(EINVAL);
        }
    }
    if (strcmp(kqContext.inputFile, "-") == 0) {
        if (kqContext.rarguments.rwflag == IO_DIRECT) {
            error("Direct I/O method for stdin is not allowed\n");
            exit(EINVAL);
        }
        if (kqContext.rarguments.rwflag == IO_MMAP) {
            error("Mmap I/O for stdin is not allowed \n");
            exit(EINVAL);
        }
        if (kqContext.sequence == IO_RANDOM) {
            error("Random sequence for stdin is not allowed\n");
            exit(EINVAL);
        }
    }
    if ((kqContext.type == IO_NOSPARSE) && (kqContext.sparseFactor > 1)) {
        error("Non-sparse cannot have sparse factor more than 1(default)!\n");
        exit(EINVAL);
    }
    if ((kqContext.numReadThreads > MAX_THREADS) ||
        (kqContext.numReadThreads <= 0)) {
        error("Number of read threads should be between 0 and MAX_THREADS!\n");
        exit(EINVAL);
    }
    if ((kqContext.numWriteThreads > MAX_THREADS) ||
        (kqContext.numWriteThreads <= 0)) {
        error("Number of write threads should be between 0 and %"PRIu32"!\n",
               MAX_THREADS);
        exit(EINVAL);
    }
    if ((kqContext.warguments.rwflag == IO_DIRECT) && g_randomIosize) {
        error(" diectio io can not be used with random iosize!!");
        exit(EINVAL);
    }
    if ((kqContext.rarguments.rwflag == IO_DIRECT) && g_randomIosize) {
        error(" diectio io can not be used with random iosize!!");
        exit(EINVAL);
    }
}


int main(int argc, char **argv)
{
    if (argc  <= 1) {
        printf("\n"USAGE_MSG"\n");
        exit(EINVAL);
    }
    kqInitialiseDefaultContext();
    kqParseArguments(argc, argv);
    kqDefaultPattern();
    kqValidateArguments();
    #if defined(linux) 
    kqNiceness();
    #endif
    kqExecuteTc();
    kqReportResults();
    return SUCCESS;
}
