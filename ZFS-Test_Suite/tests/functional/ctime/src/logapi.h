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

#ifndef _LOGAPI_H
#define	_LOGAPI_H

#pragma ident	"@(#)logapi.h	1.2	07/03/14 SMI"

#ifdef __cplusplus
extern "C" {
#endif

/* Main Functions */

void log_assert(char *);
void log_note(char *);
void log_pos(int, char *);
void log_neg(int, char *);
void log_must(int, char *);
void log_mustnot(int, char *);
void log_onexit(void (*)(void));

/* Exit Functions */

void log_pass(char *);
void log_fail(char *);
void log_unresolved(char *);
void log_notinuse(char *);
void log_unsupported(char *);
void log_untested(char *);
void log_uninitiated(char *);
void log_noresult(char *);
void log_warning(char *);
void log_timed_out(char *);
void log_other(char *);

#ifdef __cplusplus
}
#endif

#endif /* _LOGAPI_H */
