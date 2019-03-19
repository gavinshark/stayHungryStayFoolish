#pragma once
#include "stdafx.h"
#include <stdio.h>
#include <vector>
#include <string>
#include "asyncDNSHandler.h"
#include "ws2tcpip.h"
#include <windns.h>
#include <ctime>
#include <Windows.h>
#include <iostream>
using namespace std;

#define ERROR_HOSTNAME_DNSRECORD_NOTEXIST    (0)
#define ERROR_HOSTNAME_DNSRECORD_EXIST       (1)
#define ERROR_HOSTNAME_DNSRECORD_TIME_OUT    (2)
#define ERROR_HOSTNAME_DNSRECORD_IP_FORMAT   (3)
#define ERROR_HOSTNAME_DNSRECORD_OTHER_ERROR (4)

int handleDNSQuery(const wstring strHostName);