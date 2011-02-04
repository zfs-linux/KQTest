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

#pragma ident	"@(#)liblogapi.c	1.3	07/05/04 SMI"

/*
 * logapi C library
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>



#include "stf.h"
#include "logapi.h"

/*LINTLIBRARY*/

#define	MAX_MSGSIZE		256
#define	LBL_ASSERTION		0
#define	LBL_NOTE		1
#define	LBL_ERROR		2
#define	LBL_SUCCESS		3

static void (*cleanup_function)(void) = NULL;

/*
 * Internal utility functions
 */

/*
 * printline
 *
 * Print output line with current time
 *
 * msg - message string
 */
static void
printline(char *msg)
{
	char buf[32];
	struct tm *tm;
	time_t tt;

	(void) time(&tt);
	tm = localtime(&tt);
	(void) strftime(buf, sizeof (buf), "%H:%M:%S", tm);
	(void) fprintf(stdout, "%s %s\n", buf, msg);
	(void) fflush(stdout);
}

/*
 * printmsg
 *
 * Print a message line with a label
 *
 * label - message label number
 * msg - message string
 */
static void
printmsg(int label, char *msg)
{
	char buf[MAX_MSGSIZE];
	static char *msglabel[] = {
		"ASSERTION: ",
		"NOTE: ",
		"ERROR: ",
		"SUCCESS: "
	};

	buf[0] = 0;
	(void) strncat(buf, msglabel[label], MAX_MSGSIZE);
	(void) strncat(buf, msg, MAX_MSGSIZE);
	printline(buf);
}

/*
 * endlog
 *
 * Perform cleanup and exit
 *
 * rcode - result code
 * msg - message text
 */
static void
endlog(int rcode, char *msg)
{
	void (*cleanup)(void);

	if (cleanup_function != NULL) {
		/* Make sure cleanup function is only used once */
		cleanup = cleanup_function;
		log_onexit(NULL);
		/* Call cleanup function */
		log_note("Performing local cleanup");
		cleanup();
	}
	if (msg != NULL) {
		printline(msg);
	}
	exit(rcode);
}

/*
 * Main logapi functions
 */

/*
 * log_assert
 *
 * Output an assertion
 *
 * text - assertion text
 */
void
log_assert(char *text)
{
	printmsg(LBL_ASSERTION, text);
}

/*
 * log_note
 *
 * Output a comment
 *
 * text - comment text
 */
void
log_note(char *text)
{
	printmsg(LBL_NOTE, text);
}

/*
 * log_pos
 *
 * Check status and output success message (zero) or error message (non-zero)
 *
 * status - status value
 * text - message text
 */
void
log_pos(int status, char *text)
{
	if (status == 0)
		printmsg(LBL_SUCCESS, text);
	else
		printmsg(LBL_ERROR, text);
}

/*
 * log_neg
 *
 * Check status and output error message (zero) or success message (non-zero)
 *
 * status - status value
 * text - message text
 */
void
log_neg(int status, char *text)
{
	if (status != 0)
		printmsg(LBL_SUCCESS, text);
	else
		printmsg(LBL_ERROR, text);
}

/*
 * log_must
 *
 * Check status and output success message (zero) or error message (non-zero),
 * and exit with FAIL if status is non-zero
 *
 * status - status value
 * text - message text
 */
void
log_must(int status, char *text)
{
	log_pos(status, text);
	if (status != 0)
		log_fail(NULL);
}

/*
 * log_mustnot
 *
 * Check status and output error message (zero) or success message (non-zero),
 * and exit with FAIL if status is zero
 *
 * status - status value
 * text - message text
 */
void
log_mustnot(int status, char *text)
{
	log_neg(status, text);
	if (status == 0)
		log_fail(NULL);
}

/*
 * log_onexit
 *
 * Sets the exit handler
 *
 * cleanup - cleanup function pointer
 */
void
log_onexit(void (*cleanup)(void))
{
	cleanup_function = cleanup;
}

/*
 * Exit functions
 */

/*
 * log_pass
 *
 * Perform cleanup and exit STF_PASS
 *
 * msg - message text
 */
void
log_pass(char *msg)
{
	endlog(STF_PASS, msg);
}

/*
 * log_fail
 *
 * Perform cleanup and exit STF_FAIL
 *
 * msg - message text
 */
void
log_fail(char *msg)
{
	endlog(STF_FAIL, msg);
}

/*
 * log_unresolved
 *
 * Perform cleanup and exit STF_UNRESOLVED
 *
 * msg - message text
 */
void
log_unresolved(char *msg)
{
	endlog(STF_UNRESOLVED, msg);
}

/*
 * log_notinuse
 *
 * Perform cleanup and exit STF_NOTINUSE
 *
 * msg - message text
 */
void
log_notinuse(char *msg)
{
	endlog(STF_NOTINUSE, msg);
}

/*
 * log_unsupported
 *
 * Perform cleanup and exit STF_UNSUPPORTED
 *
 * msg - message text
 */
void
log_unsupported(char *msg)
{
	endlog(STF_UNSUPPORTED, msg);
}

/*
 * log_untested
 *
 * Perform cleanup and exit STF_UNTESTED
 *
 * msg - message text
 */
void
log_untested(char *msg)
{
	endlog(STF_UNTESTED, msg);
}

/*
 * log_uninitiated
 *
 * Perform cleanup and exit STF_UNINITIATED
 *
 * msg - message text
 */
void
log_uninitiated(char *msg)
{
	endlog(STF_UNINITIATED, msg);
}

/*
 * log_noresult
 *
 * Perform cleanup and exit STF_NORESULT
 *
 * msg - message text
 */
void
log_noresult(char *msg)
{
	endlog(STF_NORESULT, msg);
}

/*
 * log_warning
 *
 * Perform cleanup and exit STF_WARNING
 *
 * msg - message text
 */
void
log_warning(char *msg)
{
	endlog(STF_WARNING, msg);
}

/*
 * log_timed_out
 *
 * Perform cleanup and exit STF_TIMED_OUT
 *
 * msg - message text
 */
void
log_timed_out(char *msg)
{
	endlog(STF_TIMED_OUT, msg);
}

/*
 * log_other
 *
 * Perform cleanup and exit STF_OTHER
 *
 * msg - message text
 */
void
log_other(char *msg)
{
	endlog(STF_OTHER, msg);
}
