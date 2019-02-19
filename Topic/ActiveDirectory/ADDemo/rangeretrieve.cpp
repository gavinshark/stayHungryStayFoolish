// PrintGroupMembers
//
// Takes a pointer to an ldap connection, and a distinguished name, and prints
// all of the values of the 'member' attribute. Uses the range option if necessary.
//
void PrintGroupMembers(LDAP *ld, char *groupdn)
{
    LDAPMessage *res, *entry;
    char *attrs[2];
    DWORD err;
    int   i;
    DWORD start;
    DWORD end = 0;
    PCHAR *vals;
    char rangeattbuf[20];
    int  rangesize;

    attrs[0] = "member";
    attrs[1] = NULL;

    do {
        err = ldap_search_s(ld,
            groupdn,
            LDAP_SCOPE_BASE,
            "(objectClass=*)",
            attrs,
            FALSE,
            &res
        );

        if (LDAP_SUCCESS != err) {
            printf("ldap_search_s failed with %d, %d.\n", err, LdapGetLastError());
            exit(1);
        }

        entry = ldap_first_entry(ld, res);
        if (!entry) {
            printf("ldap_first_entry failed with %d, %d.\n", err, LdapGetLastError());
            exit(1);
        }

        vals = GetRangeValue(ld, entry, "member", &start, &end);
        if (!vals) {
            printf("GetRangeValue failed.\n");
            exit(1);
        }

        for (i = 0; vals[i]; i++) {
            printf("%s\n", vals[i]);
        }

        if (vals) {
            ldap_value_free(vals);
        }

        if (-1 != end) {
            rangesize = ConstructRangeAtt("member", end + 1, -1, rangeattbuf, 20);
            if (20 < rangesize) {
                printf("Not enough buffer to construct range.  Need %d bytes.\n", rangesize);
                exit(1);
            }

            attrs[0] = rangeattbuf;
        }
    } while (-1 != end);
}

// GetRangeValue
// 
// Given an entry returned from a search and an attribute type this function
// will find the attribute type and return the set of values.  Works even if
// the range option is present on the attribute.  If the range option is 
// present then the DWORDs pointed to by the start and end parameters are
// set to the range values.  Otherwise they are set to 0 and -1 respectively.
// The function indicates that the server has sent the last values of the 
// attribute by setting the DWORD pointed to by end to -1 on return.
// 
// On success GetRangeValue returns the set of values returned from
// ldap_get_values. As a result the pointer returned from this function must
// be freed with ldap_value_free().
//
// On failure GetRangeValue returns NULL.
//
// ld      - pointer to a valid ldap connection
// entry   - an entry returned from ldap_first_entry or ldap_next_entry
// atttype - the name of the attribute queried for
// start   - pointer to a DWORD where the beginning of the range is stored
// end     - pointer to a DWORD where the end of the range is stored
// 
PCHAR * GetRangeValue(LDAP *ld, LDAPMessage *entry, char *atttype, DWORD *start, DWORD *end)
{
    BOOL  rangefound = FALSE;
    BerElement *ptr = NULL;
    char *attdescr;
    PCHAR *vals = NULL;

    //
    // Verify that the server sent the atttype requested.
    //
    attdescr = ldap_first_attribute(ld, entry, &ptr);
    while ((NULL != attdescr) && !rangefound) {
        while ((NULL != attdescr) && !(rangefound = ParseRange(atttype, attdescr, start, end))) {
            attdescr = ldap_next_attribute(ld, entry, ptr);
        }
        vals = ldap_get_values(ld, entry, attdescr);
        if (!vals || !(vals[0])) {
            if (vals) {
                ldap_value_free(vals);
                vals = NULL;
            }
            rangefound = FALSE;
            attdescr = ldap_next_attribute(ld, entry, ptr);
        }
    }

    ber_free(ptr, 0);
    return vals;
}

// ParseRange
//
// Given an attribute description returned from and LDAP directory, this
// function parses any range option found. If the attribute description
// does not have the attribute type passed in the ParseRange will return
// FALSE. Otherwise ParseRange returns TRUE on success.
//
// atttype  - The attribute name queried for.
// attdescr - The attribute description returned from the server.
// start    - Pointer to a DWORD where the start of the range will be stored on
//            return. Set to 0 if there is no range option.
// end      - Pointer to a DWORD where the end of the range will be stored on
//            return. Set to -1 if there is no range option.
//
BOOL ParseRange(char *atttype, char *attdescr, DWORD *start, DWORD *end)
{
    int atttypelen, attdescrlen;
    char *rangestring = "range=";
    int rangestringlen = strlen(rangestring);
    char *optionstart;
    BOOL rangefound = FALSE;
    char *startstring, *endstring;
    int i;

    if (!_stricmp(atttype, attdescr)) {
        // The attribute was returned without options.
        *start = 0;
        *end = -1;
        return TRUE;
    }

    atttypelen = strlen(atttype);
    attdescrlen = strlen(attdescr);

    if ((atttypelen > attdescrlen) ||
        (';' != attdescr[atttypelen]) ||
        (_strnicmp(atttype, attdescr, atttypelen))
        )
    {
        return FALSE;
    }

    //
    // It is the correct attribute type. Verify that if there is a range option.
    // Start verification after the first semicolon.
    //
    *start = 0;
    *end = -1;
    optionstart = attdescr + atttypelen + 1;

    do {
        if ((attdescrlen - (optionstart - attdescr)) < rangestringlen) {

            // No space left in the string for range option.
            optionstart = attdescr + attdescrlen;

        }
        else if (!_strnicmp(optionstart, rangestring, rangestringlen)) {

            // Found a range string. Ensure that it looks like what is expected
            // and then parse it.
            startstring = optionstart + rangestringlen;
            for (i = 0; isdigit(startstring[i]); i++);

            if ((0 != i) &&
                ('-' == startstring[i]) &&
                (('*' == startstring[i + 1]) ||
                    isdigit(startstring[i + 1])
                    )
                )
            {
                // Acceptable. Finish parsing.
                endstring = &startstring[i + 1];

                *start = strtol(startstring, NULL, 10);
                if ('*' == endstring[0]) {
                    *end = -1;
                }
                else {
                    *end = strtol(endstring, NULL, 10);
                }
                rangefound = TRUE;
            }
        }

        // If necessary, advance to the next option.
        if (!rangefound) {
            while (('\0' != *optionstart) && (';' != *optionstart)) {
                optionstart++;
            }
            // Skip the semicolon.
            optionstart++;
        }

    } while (!rangefound && (attdescrlen > (optionstart - attdescr)));

    return TRUE;
}

// ConstructRangeAtt
//
// This function constructs an attribute description with a range option
// attached. This function returns the number of bytes of buffer required
// for the attribute description. If the returned number is larger than 
// outbuflen, then nothing was written to outbuf, and ConstructRangeAtt should
// be called again with at least the amount of buffer returned.
//
// atttype   - The name of the attribute with the range option.
// start     - The start of the range.
// end       - The end of the range.
// outbuf    - The buffer where the attribute description will be constructed.
// outbuflen - The length, in bytes, of outbuf.
//
int ConstructRangeAtt(char *atttype, DWORD start, DWORD end, char *outbuf, int outbuflen)
{
    char startstring[11], endstring[11];
    int  requiredlen;

    startstring[10] = endstring[10] = '\0';

    // Calculate buffer space required.
    _snprintf_s(startstring, 10, "%u", start);
    if (-1 == end) {
        strcpy_s(endstring, "*");
    }
    else {
        _snprintf_s(endstring, 10, "%u", end);
    }

    requiredlen = strlen(atttype) + strlen(startstring) + strlen(endstring);
    // Add in space for ';range=' and '-' and the terminating null.
    requiredlen += 9;

    // Verify that enough space was passed in.
    if (outbuflen < requiredlen) {
        return requiredlen;
    }

    _snprintf_s(outbuf, outbuflen - 1, "%s;range=%s-%s", atttype, startstring, endstring);
    outbuf[outbuflen - 1] = '\0';

    return requiredlen;
}