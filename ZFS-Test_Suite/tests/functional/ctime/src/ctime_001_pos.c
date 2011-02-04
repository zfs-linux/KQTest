/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at usr/src/OPENSOLARIS.LICENSE.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */

/*
 * Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#pragma ident	"@(#)ctime_001_pos.c	1.1	07/05/25 SMI"

#include <sys/types.h>
#include <sys/stat.h>
#include <utime.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>

/*
 * SUNWstc-stf contrib lib
 */
#include "logapi.h"

#define	ST_ATIME 0
#define	ST_CTIME 1
#define	ST_MTIME 2

#define	ALL_MODE (mode_t)(S_IRWXU|S_IRWXG|S_IRWXO)

typedef struct timetest {
	int	type;
	char	*name;
	int	(*func)(const char *pfile);
} timetest_t;

extern int errno ;

#ifdef __stc_assertion__

/*
 * ID: ctime_001_pos
 *
 * DESCRIPTION:
 * 	Verify time will be changed correctly according to relevant operating.
 *
 * STRATEGY:
 *	1. Define time test array.
 *	2. loop each item in this array.
 *	3. Verify the time will be changed after relevant operating.
 *
 * TESTABILITY: explicit
 *
 * TEST_AUTOMATION_LEVEL: automated
 *
 * CODING_STATUS: COMPLETED (2007-01-30)
 *
 */

#endif	/* __stc_assertion__ */

/*
 * Get file specific time information.
 */
int get_file_time(char *pfile, int what, time_t *ptr);

int do_read(const char *pfile);
int do_write(const char *pfile);
int do_link(const char *pfile);
int do_creat(const char *pfile);
int do_utime(const char *pfile);
int do_chmod(const char *pfile);
int do_chown(const char *pfile);

void cleanup(void);

static char tfile[BUFSIZ] = { 0 };
static char msg[BUFSIZ] = { 0 };

static timetest_t timetest_table[] = {
	{ ST_ATIME,	"st_atime",	do_read		},
	{ ST_ATIME,	"st_atime",	do_utime	},
	{ ST_MTIME,	"st_mtime",	do_creat	},
	{ ST_MTIME,	"st_mtime",	do_write	},
	{ ST_MTIME,	"st_mtime",	do_utime	},
	{ ST_CTIME,	"st_ctime",	do_creat	},
	{ ST_CTIME,	"st_ctime",	do_write	},
	{ ST_CTIME,	"st_ctime",	do_chmod	},
	{ ST_CTIME,	"st_ctime",	do_chown 	},
	{ ST_CTIME,	"st_ctime",	do_link		},
	{ ST_CTIME,	"st_ctime",	do_utime	},
};

#define	NCOMMAND (sizeof (timetest_table) / sizeof (timetest_table[0]))

void
main(int argc, char *argv[])
{
	int i, ret, fd;
	char *penv[] = {"mnt", "test_file"};

	log_assert("Verify access time will be changed when file data" \
	    "was last accessed.");
	log_onexit(cleanup);

	/*
	 * Get envirnment variable value
	 */
/*	for (i = 0; i < sizeof (penv) / sizeof (char *); i++) {
		if ((penv[i] = getenv(penv[i])) == NULL) {
			log_must(-1, "getenv(penv[i])");
		}
	}*/
	(void) snprintf(tfile, sizeof (tfile), "%s/%s", "/tank/zfs","test_file");

	/*
	 * If the test file is existing, remove it firstly
	 */

        printf("file :  %s\n", tfile);
   
	if (access(tfile, F_OK) == 0) {
		unlink(tfile);
	}
	ret = 0;
	if ((fd = open(tfile, O_WRONLY | O_CREAT | O_TRUNC, ALL_MODE)) == -1) {
		ret = errno;
	}
	if (fd != -1) {
		(void) close(fd);
	}
	(void) snprintf(msg, sizeof (msg), \
	    "open(%s, O_WRONLY | O_CREAT | O_TRUNC, ALL_MODE)", tfile);
	log_must(ret, msg);

	for (i = 5; i < NCOMMAND; i++) {
		time_t t1, t2;

		/*
		 * Get original time before operating.
		 */

		ret = get_file_time(tfile, timetest_table[i].type, &t1);
		if (ret != 0) {
			(void) snprintf(msg, sizeof (msg),
			    "get_file_time(%s, %d, &t1)",
			    tfile, timetest_table[i].type);
			log_must(ret, msg);
		}

		/*
		 * Sleep 2 seconds, then invoke command on givin file
		 */
		sleep(2);
		timetest_table[i].func(tfile);

		/*
		 * Get time after operating.
		 */
		ret = get_file_time(tfile, timetest_table[i].type, &t2);
		if (ret != 0) {
			(void) snprintf(msg, sizeof (msg),
			    "get_file_time(%s, %d, &t2)",
			    tfile, timetest_table[i].type);
			log_must(ret, msg);
		}

		if (t1 == t2) {
			snprintf(msg, sizeof (msg), "%s: t1(%ld) == t2(%ld)",
			    timetest_table[i].name, (long)t1, (long)t2);
			log_must(-1, msg);
		} else {
			snprintf(msg, sizeof (msg), "%s: t1(%ld) != t2(%ld)",
			    timetest_table[i].name, (long)t1, (long)t2);
			log_must(0, msg);
		}
	}

	(void) unlink(tfile);

	log_pass("Verify access time will be changed passed.");
}

int
get_file_time(char *pfile, int what, time_t *ptr)
{
	struct stat stat_buf;

	if (pfile == NULL || ptr == NULL) {
		return (-1);
	}

	if (stat(pfile, &stat_buf) == -1) {
		return (-1);
	}

	switch (what) {
		case ST_ATIME:
			*ptr = stat_buf.st_atime;
			return (0);
		case ST_CTIME:
			*ptr = stat_buf.st_ctime;
			return (0);
		case ST_MTIME:
			*ptr = stat_buf.st_mtime;
			return (0);
		default:
			return (-1);
	}
}

int
do_read(const char *pfile)
{
	int fd, ret = 0;
	char buf[BUFSIZ] = { 0 };

	if (pfile == NULL) {
		return (-1);
	}

	if ((fd = open(pfile, O_RDONLY, ALL_MODE)) == -1) {
		return (-1);
	}
	if (read(fd, buf, sizeof (buf)) == -1) {
		ret = errno;
	}
	(void) close(fd);

	(void) snprintf(msg,
	    sizeof (msg), "read(%d, buf, %d)", fd, sizeof (buf));
	log_must(ret, msg);

	return (ret);
}

int
do_write(const char *pfile)
{
	int fd, ret = 0;
	char buf[BUFSIZ] = "call function do_write()";

	if (pfile == NULL) {
		return (-1);
	}

	if ((fd = open(pfile, O_WRONLY, ALL_MODE)) == -1) {
		return (-1);
	}
	if (write(fd, buf, strlen(buf)) == -1) {
		ret = errno;
	}
	(void) close(fd);

	(void) snprintf(msg,
	    sizeof (msg), "write(%d, buf, %d)", fd, strlen(buf));
	log_must(ret, msg);

	return (ret);
}

int
do_link(const char *pfile)
{
	int ret = 0;
	char link_file[BUFSIZ] = { 0 };
	char *ptr = link_file;

	if (pfile == NULL) {
		return (-1);
	}

	/*
	 * Figure out source file directory name, and create
	 * the link file in the same directory.
	 */
	snprintf(link_file, sizeof (link_file), "%s", pfile);
	ptr = strrchr(link_file, '/');
	snprintf(ptr + 1,
	    sizeof (link_file) - (ptr + 1 - link_file), "link_file");

	if (link(pfile, link_file) == -1) {
		ret = errno;
	}
	(void) snprintf(msg, sizeof (msg), "link(%s, %s)", pfile, link_file);
	log_must(ret, msg);

	unlink(link_file);
	return (ret);
}

int
do_creat(const char *pfile)
{
	int fd, ret = 0;

	if (pfile == NULL) {
		return (-1);
	}

	if ((fd = creat(pfile, ALL_MODE)) == -1) {
		ret = errno;
	}
	if (fd != -1) {
		(void) close(fd);
	}

	(void) snprintf(msg, sizeof (msg), "creat(%s, ALL_MODE)", pfile);
	log_must(ret, msg);

	return (ret);
}

int
do_utime(const char *pfile)
{
	int ret = 0;

	if (pfile == NULL) {
		return (-1);
	}

	/*
	 * Times of the file are set to the current time
	 */
	if (utime(pfile, NULL) == -1) {
		ret = errno;
	}
	(void) snprintf(msg, sizeof (msg), "utime(%s, NULL)", pfile);
	log_must(ret, msg);

	return (ret);
}

int
do_chmod(const char *pfile)
{
	int ret = 0;

	if (pfile == NULL) {
		return (-1);
	}

	if (chmod(pfile, ALL_MODE) == -1) {
		ret = errno;
	}
	(void) snprintf(msg, sizeof (msg), "chmod(%s, ALL_MODE)", pfile);
	log_must(ret, msg);

	return (ret);
}

int
do_chown(const char *pfile)
{
	int ret = 0;

	if (pfile == NULL) {
		return (-1);
	}

	if (chown(pfile, getuid(), getgid()) == -1) {
		ret = errno;
	}
	(void) snprintf(msg, sizeof (msg), "chown(%s, %d, %d)", \
	    pfile, (int)getuid(), (int)getgid());
	log_must(ret, msg);

	return (ret);
}

void
cleanup(void)
{
	if ((strlen(tfile) != 0) && (access(tfile, F_OK) == 0)) {
		int ret = 0;
		ret = unlink(tfile);
		(void) snprintf(msg, sizeof (msg), "unlink(%s)", tfile);
		log_must(ret, msg);
	}
}
