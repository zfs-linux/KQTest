#include "../iotest.h"

/*
 * Function     : kqNicenss
 *
 * Description  : This function changes the sheduling priority (nice value) of 
 *                the process.
 *
 * Parameters   :
 *
 */
void kqNiceness()
{

    debug("%s\n", __FUNCTION__);

    if (nice(kqContext.nice) == -1) {
        error("Using default priority. Setting up new scheduling priority"
                "failed %s \n",  strerror(errno));
        exit(-1);
    }
}


/*
 * Function     : kqTimeElapsed
 *
 * Description  : This function calculates the time elapsed.
 *
 * Parameters   :
 *
 * Return Value :
 *                  Retruns the time from gettimeofday function.
 */
int64 kqTimeElapsed()
{
    struct timeval tp;

    debug("%s\n", __FUNCTION__);

    if (gettimeofday(&tp, (struct timezone *) NULL) == -1) {
            error("gettimeofday failed  %s \n", strerror(errno));
            exit(-1);
    }
    return (int64)(((int64) (tp.tv_sec)) * 1000000 + (int64) (tp.tv_usec));
}


/*
 * Function     : kqIoOpenInputFile
 *
 * Description  : This function opens the input file.
 *
 * Parameters   :
 *      1. fd       File Desscriptor
 *
 * Return Value :
 *                  Returns SUCCESS if file is opened successfully.
 *                  Returns FAILURE if opening of file fails.
 *
 */
int kqIoOpenInputFile(int *fd)
{

    debug("%s\n", __FUNCTION__);

    if (strncmp(kqContext.inputFile, "-", 1) != 0) {
        if (kqContext.rarguments.rwflag == IO_DIRECT) {
            *fd = open(kqContext.inputFile, O_RDONLY | O_DIRECT);
            if (*fd == -1) {
                error("open %s errorcode %s \n", kqContext.inputFile,
                      strerror(errno));
                return FAILURE;
            } else {
                return SUCCESS;
            }
        }
        *fd = open(kqContext.inputFile, O_RDONLY);
        if (*fd == -1) {
            error("open %s errorcode %s \n", kqContext.inputFile,
                  strerror(errno));
            return FAILURE;
        } else {
            return SUCCESS;
        }
    } else {
        debug("stdin is the input file\n");
        *fd = 0;
    }
    return SUCCESS;
}


/*
 * Function     : kqIoOpenOutputFile
 *
 * Description  : This function opens the output file.
 *
 * Parameters   :
 *      1. fd       File Desscriptor
 *
 * Return Value :
 *                  Return SUCCESS if file is opened successfully.
 *                  Return FAILURE if opening of file fails.
 */
int kqIoOpenOutputFile(int *fd)
{

    debug("%s\n", __FUNCTION__);

    if (strncmp(kqContext.outputFile, "-", 1) != 0) {
        if (kqContext.warguments.rwflag == IO_DIRECT) {
            *fd = open(kqContext.outputFile, O_RDWR | O_CREAT | O_DIRECT,
                       S_IRWXU | S_IRWXG | S_IRWXO);
            if (*fd == -1) {
                error("open %s errocode %s \n", kqContext.outputFile,
                       strerror(errno));
                return FAILURE;
            } else {
                return SUCCESS;
            }
        }
        *fd = open(kqContext.outputFile, O_RDWR | O_CREAT, S_IRWXU | S_IRWXG |
                   S_IRWXO);
    } else {
        debug("stdout is the output file\n");
        *fd = 1;
    }
    if (*fd == -1) {
        error("open %s errocode %s \n", kqContext.outputFile, strerror(errno));
        return FAILURE;
    } else {
        return SUCCESS;
    }
}


/*
 * Function     : kqIoCommonRead
 *
 * Description  : This function reads from the file.
 *
 *  Parameters  :
 *      1. fd       File descriptor.
 *      2. offset   Offset from which read needs to be started.
 *      3. size     iosize
 *      4. buffer   Buffer which will filled after read operation.
 *
 * Return Value :
 *                  Returns SUCCESS if read was successful.
 *                  Returns FAILURE if read failed.
 */
int kqIoCommonRead(int fd, uint64 offset, uint64  size, char *buffer)
{
    uint64 len;
    char *buf;

    debug("%s\n", __FUNCTION__);

    if (g_sectorSize == 0) {
            g_sectorSize = 512;
    }
    if (lseek(fd, offset, SEEK_SET) == -1) {
            error("lseek failed %s \n", strerror(errno));
            exit(ESPIPE);
    }
    if (kqContext.rarguments.rwflag == IO_DIRECT) {
        if (posix_memalign((void **)&buf, g_sectorSize, size) != 0) {
            error("posix memalign failed %s \n", strerror(errno));
            return FAILURE;
        }
        len = read(fd, buf, size);
        strncpy(buffer, buf, size);
        free(buf);
    } else {
        len = read(fd, buffer, size);
    }
    if (len != size) {
        error("read file  %-2d error %2"PRIu64" : %s\n", fd, len,
              strerror(errno));
        return FAILURE;
    } else {
        debug("read file  %-2d offset %10"PRIu64" length %10"PRIu64" \n", fd,
              offset, len);
        return SUCCESS;
    }
}


/*
 * Function     : kqIoCommonWrite
 *
 * Description  : This function performs write on the file.
 *
 * Parameters   :
 *      1. fd       File descriptor
 *      2. offset   File offset
 *      3. size     iosize
 *      4. buffer   Buffer, which is filled with pattern for write operation.
 *
 * Return Value :
 *                  Returns SUCCESS if write was successful.
 *                  Returns FAILURE if write failed.
 */
int kqIoCommonWrite(int fd, uint64 offset, uint64 size, char *pattern)
{
    uint64 len;
    char *buf = NULL;

    debug("%s\n", __FUNCTION__);

    if (g_sectorSize == 0) {
            g_sectorSize = 512;
    }
    if (lseek(fd, offset, SEEK_SET) == -1) {
            error("lseek failed %s\n", strerror(errno));
            exit(ESPIPE);
    }
    if (kqContext.warguments.rwflag == IO_DIRECT) {
        if (posix_memalign((void **)&buf, g_sectorSize, size) != 0) {
            error("posix memalign failed\n", strerror(errno));
            return FAILURE;
        }
        strncpy(buf, pattern, size);
        len = write(fd, buf, size);
        free(buf);
    } else {
        len = write(fd, pattern, size);
    }
    if (len != size) {
        error("write file %2d offset %"PRIu64" length %10"PRIu64"\n", fd,
                offset, size);
        return FAILURE;
    } else {
        debug("write file %2d offset %"PRIu64" length %10"PRIu64"\n", fd,
                offset, len);
        return SUCCESS;
    }
}


/*
 * Function     : kqIoGetSectorSize
 *
 * Description  : This function returns the sector size.
 *
 * Parameters   :
 *
 * Return Values:
 *                  Returns the sector size if it is computed
 *                  successfully.
 *                  Returns FAILURE otherwise.
 */
int kqIoGetSectorSize(char *File)
{
    FILE *filePointerMtab;
    FILE *filePointerMounts;
    struct stat fileStat;
    struct stat deviceFileStat;
    struct mntent *mntEntry = NULL;
    int sectorSize = 512;
    int deviceFd;
    int rc;

    debug("%s\n", __FUNCTION__);

    if (stat(File, &fileStat) == -1) {
        error("stat for the file failed %s \n", strerror(errno));
    }
    filePointerMtab = setmntent("/etc/mtab", "r");
    filePointerMounts = setmntent("/proc/mounts", "r");
    while ((mntEntry = getmntent(filePointerMtab)) != NULL)
    {
        stat(mntEntry->mnt_fsname, &deviceFileStat);
        if (fileStat.st_dev == deviceFileStat.st_rdev) {
            if ((deviceFd = open(mntEntry->mnt_fsname, O_RDONLY)) < 0) {
                debug("error while opening device file %s, returning default"
                        " sector size 512 \n", strerror(errno));
                return sectorSize;
            }
            rc = ioctl(deviceFd, BLKSSZGET, &sectorSize);
            if (rc != 0) {
                sectorSize = 512;
            }
            return sectorSize;
        }
    }
    while ((mntEntry = getmntent(filePointerMounts)) != NULL)
    {
        stat(mntEntry->mnt_fsname, &deviceFileStat);
        if (fileStat.st_dev == deviceFileStat.st_rdev) {
            if ((deviceFd = open(mntEntry->mnt_fsname, O_RDONLY)) < 0) {
                error("error while opening device file \n",
                        strerror(errno));
                return FAILURE;
            }
            rc = ioctl(deviceFd, BLKSSZGET, &sectorSize);
            if (rc != 0) {
                sectorSize = 512;
            }
            return sectorSize;
        }
    }
    return sectorSize;
}
