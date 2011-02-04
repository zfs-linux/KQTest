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
 * Copyright 2007 Sun Microsystems, Inc.	All rights reserved.
 * Use is subject to license terms.
 *
 */

#ifndef _STF_H
#define	_STF_H

#pragma ident	"@(#)stf.h	1.4	07/05/04 SMI"

#ifdef __cplusplus
extern "C" {
#endif

#define	STF_MAX_RESULTS	11

/* result codes */
#define	STF_PASS 0
#define	STF_FAIL 1
#define	STF_UNRESOLVED	2
#define	STF_NOTINUSE	3
#define	STF_UNSUPPORTED 4
#define	STF_UNTESTED	5
#define	STF_UNINITIATED 6
#define	STF_NORESULT	7
#define	STF_WARNING	8
#define	STF_TIMED_OUT	9
#define	STF_OTHER	10

/* result index for results totals array */
/* so your test can say "++results[PASS_INDEX]" */
#define	PASS_INDEX		0
#define	FAIL_INDEX		1
#define	UNRESOLVED_INDEX	2
#define	NOTINUSE_INDEX		3
#define	UNSUPPORTED_INDEX	4
#define	UNTESTED_INDEX		5
#define	UNINITIATED_INDEX	6
#define	NORESULT_INDEX		7
#define	WARNING_INDEX		8
#define	TIMED_OUT_INDEX		9
#define	OTHER_INDEX		10

/* character result names */
static char *result_tbl[] = {
	"PASS",
	"FAIL",
	"UNRESOLVED",
	"NOTINUSE",
	"UNSUPPORTED",
	"UNTESTED",
	"UNINITIATED",
	"NORESULT",
	"WARNING",
	"TIMED_OUT",
	"OTHER"
};

/* function prototypes */

void stf_jnl_env();
void stf_jnl_start();
void stf_jnl_end();
void stf_jnl_testcase_start(char **);
void stf_jnl_testcase_end(char [], int, int);
void stf_jnl_assert_start(char *);
void stf_jnl_assert_end(int);
void stf_jnl_msg(char *);
void stf_jnl_totals(char *, int *);

/*
 * this was moved here per an RFE for use with the ldi testsuite though it is
 * still classified as a private interface--as journaling methods evolve it
 * may change
 */
void stf_jnl_msg_pid(int, char *);

#ifdef __cplusplus
}
#endif

#endif /* _STF_H */
