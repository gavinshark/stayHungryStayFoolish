/***********************************************************************/
/* File Name:   LDAPPageS.c                                            */
/*                                                                     */
/* Description: An example on how to perform an LDAP Paged Search      */
/* using the following APIs                                            */
/*    - ldap_create_page_control()                                     */
/*    - ldap_parse_page_control()                                      */
/*                                                                     */
/* How to compile:                                                     */
/*  Assuming the C source for LDAPPageS.c has been downloaded into     */
/*  a source physical file MyLDAPLib/QCSRC (with record length of at   */
/*  least 146 characters) as member LDAPPageS on an iSeries,           */
/*  program LDAPPageS (*PGM) can be built via the following commands:  */
/*                                                                     */
/*  CRTCMOD MODULE(MyLDAPLib/LDAPPageS)                                */
/*          SRCFILE(MyLDAPLib/QCSRC)                                   */
/*                                                                     */
/*  CRTPGM PGM(MyLDAPLib/LDAPPageS)                                    */
/*         MODULE(MyLDAPLib/LDAPPageS)                                 */
/*         BNDSRVPGM(QSYS/QGLDCLNT QSYS/QGLDBRDR)                      */
/*                                                                     */
/* Usage:                                                              */
/* The input parameters are as follows:                                */
/*   argv[1] = Search base                                             */
/*   argv[2] = filter                                                  */
/*   argv[3] = search scope (0=base, 1=onelevel, OR 2=subtree)         */
/*   argv[4] = Page size                                               */
/*                                                                     */
/***********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <ldap.h>
#include <lber.h>

static char ibmid[] = "Copyright IBM Corporation 2003 LICENSED MATERIAL - PROGRAM PROPERTY OF IBM";
#define     BIND_DN "cn=administrator"
#define     BIND_PW "adminpwd"

char         *server, *base, *filter, *scopes[] = { "BASE", "ONELEVEL", "SUBTREE" };
int      scope;
LDAP         *ld;

int main (int argc, char *argv[])
{
    int        l_rc, l_entries, l_port, l_entry_count=0, morePages, l_errcode=0, page_nbr;
    unsigned long  pageSize;
    struct berval  *cookie=NULL;
    char           pagingCriticality = 'T', *l_dn;
    unsigned long  totalCount;
    LDAPControl    *pageControl=NULL, *M_controls[2] = { NULL, NULL }, **returnedControls = NULL;
    LDAPMessage    *l_result, *l_entry;

   /******************************************************************/
   /* Check input parameters                                         */
   /*                                                                */
   if (argc < 5)
   {
      printf("The input parameters are as follows:\n");
      printf("     1. Search base\n");
      printf("     2. Filter\n");
      printf("     3. Search Scope (0=base, 1=onelevel, OR 2=subtree)\n");
      printf("     4. Page size\n");
   return 0;
   }
   /*                                                                */
   /******************************************************************/

   /******************************************************************/
   /* Set default values: Server and Port. And then parse            */
   /* input parameters into program variables                        */
   /*                                                                */
   server = NULL;
   l_port   = LDAP_PORT;

   base   = argv[1];
   filter = argv[2];
   scope  = atoi(argv[3]);
   pageSize = atoi(argv[4]);
   /*                                                                */
   /******************************************************************/

   /******************************************************************/
   /* Initialize an LDAP session                                     */
   /*                                                                */     
   ld = ldap_init(server, l_port);
   /* Check if connection is OK                                      */
   if (ld == NULL)
   {
      printf("==Error==");
      printf("  Init of server %s at port %d failed.\n", server, l_port);
      return 0;
   }
   /*                                                                */
   /******************************************************************/

   /******************************************************************/
   /* Bind as the ldap administrator                                 */
   /*                                                                */
   l_rc = ldap_simple_bind_s (ld, BIND_DN , BIND_PW);
   if ( l_rc != LDAP_SUCCESS)
   {
      printf("==Error== %s");
      printf("  Unable to Bind to the LDAP server.  Return code is %d.\n", l_rc);
      return 0;
   }
   /*                                                                */
   /******************************************************************/

   printf("  The search parms were:\n");
   printf("        base: %s\n",base);
   printf("       scope: %s\n",scopes[scope]);
   printf("      filter: %s\n",filter);
   printf("   page size: %d\n",pageSize);
   printf("  The entries returned were:\n");
   page_nbr = 1;

   /******************************************************************/
   /* Get one page of the returned results each time                 */
   /* through the loop                                               */
   do
   { 
      l_rc = ldap_create_page_control(ld, pageSize, cookie, pagingCriticality, &pageControl);

      /* Insert the control into a list to be passed to the search.     */
      M_controls[0] = pageControl;

      /* Search for entries in the directory using the parmeters.       */
      l_rc = ldap_search_ext_s(ld, base, scope, filter, NULL, 0, M_controls, NULL, NULL, 0, &l_result);
      if ((l_rc != LDAP_SUCCESS) & (l_rc != LDAP_PARTIAL_RESULTS))
      {
         printf("==Error==");
         printf("  Failure during a search.  Return code is %d.\n",l_rc);
         ldap_unbind(ld);
         break;
      }

      /* Parse the results to retrieve the contols being returned.      */
      l_rc = ldap_parse_result(ld, l_result, &l_errcode, NULL, NULL, NULL, &returnedControls, LDAP_FALSE);

      if (cookie != NULL)
      {
         ber_bvfree(cookie);
         cookie = NULL;
      }

      /* Parse the page control returned to get the cookie and          */
      /* determine whether there are more pages.                        */
      l_rc = ldap_parse_page_control(ld, returnedControls, &totalCount, &cookie);

      /* Determine if the cookie is not empty, indicating there are more pages for these search parameters. */
      if (cookie && cookie->bv_val != NULL && (strlen(cookie->bv_val) > 0))
      {
         morePages = LDAP_TRUE;
      }
      else
      {
         morePages = LDAP_FALSE;
      }

      /* Cleanup the controls used. */
      if (returnedControls != NULL)
      {
         ldap_controls_free(returnedControls);
         returnedControls = NULL;
      }
      M_controls[0] = NULL;
      ldap_control_free(pageControl);
      pageControl = NULL;

      /******************************************************************/
      /* Disply the returned result                                     */
      /*                                                                */
      /* Determine how many entries have been found.                    */
      if (morePages == LDAP_TRUE) 
         printf("===== Page : %d =====\n", page_nbr);
      l_entries = ldap_count_entries(ld, l_result);
    
      if (l_entries > 0)
      {
         l_entry_count = l_entry_count + l_entries;
      }

      for ( l_entry = ldap_first_entry(ld, l_result);
            l_entry != NULL;
            l_entry = ldap_next_entry(ld, l_entry) )
      {
         l_dn = ldap_get_dn(ld, l_entry);
         printf("    %s\n",l_dn);
      }

      /* Free the search results.                                       */
      ldap_msgfree(l_result);
      page_nbr = page_nbr + 1;

   } while (morePages == LDAP_TRUE);

   printf("\n  %d entries found during the search",l_entry_count);
   /* Free the cookie since all the pages for these search parameters   */
   /* have been retrieved.                                              */
   ber_bvfree(cookie);
   cookie = NULL;

   /* Close the LDAP session.                                           */
   ldap_unbind(ld);

   return 0;
}