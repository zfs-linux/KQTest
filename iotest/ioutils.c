#include "iotest.h"

/*
 * Function         : kqTimerHandler
 *
 * Description      : This function handles the timeout alarm.
 *
 * Parameters       :
 *       1. signum       Signal number.
 * Retrun Value
 */
void kqTimerHandler (int signum)
{
    printf("Timer for %g seconds expired so exiting... \n", kqContext.timeout);
    exit(ETIME);
}


/*
 * Function     : kqCommonAddTimeout
 *
 * Description  : This function adds the timer alarm.
 *
 * Parameters   :
 *
 * Retrun Value
 *                  Returns SUCCESS if timer is set.
 *                  Retuens FAILURE if timer is not set.
 */
int kqCommonAddTimeout()
{
    struct itimerval    value;
    int                 which;
    int                 i;

    which = ITIMER_REAL;
    i                           = kqContext.timeout;
    value.it_interval.tv_sec    = 0;
    value.it_interval.tv_usec   = 0;
    value.it_value.tv_sec       = i;
    value.it_value.tv_usec      = (kqContext.timeout - i) * 1000000;
    if (setitimer(which, &value, NULL) == -1) {
        error("Setting timer for timeout failed with  %s errocode \n",
                strerror(errno));
        return FAILURE;
    }
    signal (SIGALRM, &kqTimerHandler);
    return SUCCESS;
}


/*
 * Function    : debug
 *
 * Description : This function provides debug msg wrapper
 */
void debug(const char *format, ...)
{
#if defined (DEBUG)
    va_list arg;
    uint32  thread;

    thread = (unsigned long int)pthread_self();
    va_start (arg, format);
    printf("%"PRIu32" : ", thread);
    vprintf(format, arg);
    va_end(arg);
#endif /* DEBUG */
}


/*
 * Function    : error
 *
 * Description : This function provides error msg wrapper
 */
void error(const char *format, ...)
{
    va_list arg;
    uint32 thread;

    thread = (unsigned long int)pthread_self();
    va_start(arg, format);
    printf("%"PRIu32" : error -> ", thread);
    vprintf(format, arg);
    va_end(arg);
}


/*
 * Function    : kqReportResults
 *
 * Description : This function provides reporting functionality
 */
void kqReportResults()
{
    if (g_verbose_level > 0) {
        kqDisplayContext();
        printf("\nTotal Time               : Read : %6.3lf (mSec) & Write"
                ": %6.3lf (mSec)\n", kqIoPerf.readTotalTime,
                kqIoPerf.writeTotalTime);
        printf("Total Write/Read Size    : Read : %"PRIu64" KB  & Write "
                ": %"PRIu64" KB\n", kqContext.rarguments.size / BYTES_IN_KB,
                kqContext.warguments.size / BYTES_IN_KB);
        if (kqIoPerf.writeTotalTime != 0) {
            printf("Average Write Speed      : %g MB/sec\n",
                    (((double)kqContext.warguments.size /
                    kqIoPerf.writeTotalTime) * 1000) / BYTES_IN_MB);
        }
        if (kqIoPerf.readTotalTime != 0) {
            printf("Average Read Speed       : %g MB/sec\n",
                   (((double)kqContext.rarguments.size /
                    kqIoPerf.readTotalTime) * 1000) / BYTES_IN_MB);
        }
        printf("Average Write Latency    :\n");
        printf("Average Read Latency     :\n");
        printf("Good/Bad Verification    : Failed blocks (%"PRIu64")\n\n"
                , kqIoPerf.failedVerifyOps);
        printf("Bottom 10%% Transfer Rate Average(R)    : \n");
        printf("Top 10%% Transfer Rate Average(R)       : \n");

        printf("Bottom 10%% Transfer Rate Average(W)    : \n");
        printf("Top 10%% Transfer Rate Average(W)       : \n");

        printf("Adjusted 80%% Average Transfer Rate     : \n");
        printf("Bottom 10%% Latency Average             : \n");
        printf("Top 10%% Latency Average                : \n");
        printf("Adjusted 80%% Latency Average           : \n");
    } else {
        printf("\niotest output -> Total Time(mSec) : read (%6.3lf)"
                "write (%6.3lf);", kqIoPerf.readTotalTime,
                kqIoPerf.writeTotalTime);
        printf("Average(MB/s) : ");
        if (kqIoPerf.writeTotalTime != 0) {
            printf("write (%g)", (((double)kqContext.warguments.size /
                                kqIoPerf.writeTotalTime) * 1000) /
                                BYTES_IN_MB);
        }
        if (kqIoPerf.readTotalTime != 0) {
            printf("read (%g)", (((double)kqContext.rarguments.size /
                                kqIoPerf.readTotalTime) * 1000) /
                                BYTES_IN_MB);
        }
        if (kqIoPerf.readTotalTime != 0) {
            printf("; Verification : Failed blocks (%"PRIu64")",
                    kqIoPerf.failedVerifyOps);
        }
        printf("\n");
    }
}

/*
 * Function    : kqInitialiseDefaultContext
 *
 * Description : This function populates the default caontext
 */
void kqInitialiseDefaultContext()
{
    kqContext.verify                = FALSE;
    kqContext.numWriteThreads       = 1;
    kqContext.numReadThreads        = 1;
    kqContext.sequence              = IO_SEQUENCE;
    kqContext.type                  = IO_NOSPARSE;
    kqContext.timeout               = NO_TIMEOUT;
    kqContext.verbose               = FALSE;
    kqContext.rarguments.offset     = 0;
    kqContext.rarguments.count      = 0;
    kqContext.rarguments.blockSize  = 0;
    kqContext.rarguments.size       = 0;
    kqContext.warguments.offset     = 0;
    kqContext.warguments.count      = 0;
    kqContext.warguments.blockSize  = 0;
    kqContext.warguments.size       = 0;
    kqContext.seed                  = 0;
    kqContext.rarguments.sleep      = 0;
    kqContext.sparseFactor          = 1;
    g_patternLen = 0;
}


/*
 * Function    : kqDisplayContext
 *
 * Description : Display the context values
 */
void kqDisplayContext()
{
    printf("--------------------------------------------------------------"
           "-------------------\n");
    if ((strcmp(kqContext.inputFile, kqContext.outputFile)) != 0) {
        printf("Input File    :");
        printf(" %-25s", kqContext.inputFile);
    }
    printf("Output File   :");
    printf(" %s\n", kqContext.outputFile);
    printf("Seed          : %-25"PRIu64"" , (kqContext.seed));
    if (kqContext.verify == FALSE) {
        printf("Verification  : %s\n", "No");
    } else {
        printf("Verification  : %s\n", "Yes");
    }

    printf("Write Threads : %-25d", kqContext.numWriteThreads);
    printf("Read Threads  : %"PRIu16"\n", kqContext.numReadThreads);

    if (kqContext.sequence == 0) {
        printf("Sequence      : %-25s", "Sequential");
    } else {
        printf("Sequence      : %-25s", "Random");
    }
    if (kqContext.type == 0) {
        printf("Type          : %s(factor : %"PRIu16")\n", "Sparse",
                kqContext.sparseFactor);
    } else {
        printf("Type          : %s\n", "No-Sparse");
    }
    if (kqContext.timeout != -1) {
        printf("Timeout       : %-25g", kqContext.timeout);
    } else {
        printf("Timeout       : %-25s", "Infinite");
    }
    if (kqContext.warguments.rwflag == IO_MMAP) {
        printf("Write IO      : %s\n", "Memory Mapped I/O");
    }
    if (kqContext.warguments.rwflag == IO_DIRECT) {
        printf("Write IO      : %s\n", "Direct I/O");
    } else  if (kqContext.warguments.rwflag == IO_BUFFERED) {
        printf("Write IO      : %s\n", "Buffered I/O");
    }
    if (kqContext.rarguments.rwflag == IO_MMAP) {
        printf("Read IO       : %-25s\n", "Memory Mapped I/O");
    }
    if (kqContext.rarguments.rwflag == IO_DIRECT) {
        printf("Read IO       : %-25s\n", "Direct I/O");
    } else if (kqContext.rarguments.rwflag == IO_BUFFERED) {
        printf("Read IO       : %-25s\n", "Buffered I/O");
    }
    printf("-------------------------------------------------------------"
           "--------------------\n");

}

int kqValidateFilename(char *path)
{
    /* kept as a place holeder code will be added later */
    return SUCCESS;
}
