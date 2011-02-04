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

#pragma ident	"@(#)largest_file.c	1.3	07/05/25 SMI"

#include "file_common.h"
#include <sys/param.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>

#define MAXOFFSET_T 2147483648

/*
 * --------------------------------------------------------------
 *
 *	Assertion:
 *		The last byte of the largest file size can be
 *		accessed without any errors.  Also, the writing
 *		beyond the last byte of the largest file size
 *		will produce an errno of EFBIG.
 *
 * --------------------------------------------------------------
 *	If the write() system call below returns a "1",
 *	then the last byte can be accessed.
 * --------------------------------------------------------------
 */
static void	sigxfsz(int);
static void	usage(char *);

int
main(int argc, char **argv)
{
	int		fd = 0;
	unsigned long int	offset = (MAXOFFSET_T - 1);
	unsigned long int 	llseek_ret = 0;
	int		write_ret = 0;
	int		err = 0;
	char		mybuf[5]="a";
	char		*testfile;

	if (argc != 2) {
		usage(argv[0]);
	}

	(void) sigset(SIGXFSZ, sigxfsz);

	//testfile = strdup(argv[1]);
	
	testfile = malloc(strlen(argv[1] + 1));

	strcpy(testfile, argv[1]);


	fd = open(testfile, O_CREAT | O_RDWR);
	if (fd < 0) {
		perror("Failed to create testfile");
		err = errno;
		goto out;
	}

	printf(" off : %lu\n", offset);

	llseek_ret = llseek(fd, offset, SEEK_SET);
	if (llseek_ret < 0) {
		perror("Failed to seek to end of testfile");
		err = errno;
		goto out;
	}

	write_ret = write(fd, mybuf, 1);
	if (write_ret < 0) {
		perror("Failed to write to end of file");
		err = errno;
		goto out;
	}

	offset = 0;
	llseek_ret = llseek(fd, offset, SEEK_CUR);
	if (llseek_ret < 0) {
		perror("Failed to seek to end of file");
		err = errno;
		goto out;
	}

	printf(" off : %lu\n", offset);


	write_ret = write(fd, mybuf, 1);
	if (write_ret < 0) {
		if (errno == EFBIG) {
			(void) printf("write errno=EFBIG: success\n");
			err = 0;
		} else {
			perror("Did not receive EFBIG");
			err = errno;
		}
	} else {
		(void) printf("write completed successfully, test failed\n");
		err = 1;
	}

out:
	(void) unlink(testfile);
	free(testfile);
	return (err);
}

static void
usage(char *name)
{
	(void) printf("%s <testfile>\n", name);
	exit(1);
}

/* ARGSUSED */
static void
sigxfsz(int signo)
{
	(void) printf("\nlargest_file: sigxfsz() caught SIGXFSZ\n");
}
