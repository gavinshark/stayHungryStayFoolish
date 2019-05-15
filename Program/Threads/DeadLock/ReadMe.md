## deadlock debug

### critical section

Tool: Windbg

1. Find locked threads

cmd: ~*kv

Find thread3 &4 is waiting for CS.
```
   3  Id: 1914.278 Suspend: 1 Teb: 000000dd`ea989000 Unfrozen
 # Child-SP          RetAddr           : Args to Child                                                           : Call Site
00 000000dd`eafff9d8 00007ffe`c14657ff : 00000003`00000003 00000206`7470e940 00000000`00000000 00000000`58baa08f : ntdll!NtWaitForAlertByThreadId+0x14
01 000000dd`eafff9e0 00007ffe`c1465706 : 00000000`00000000 00000000`00000000 000000dd`eafffab8 00000000`58bde547 : ntdll!RtlpWaitOnAddressWithTimeout+0x43
02 000000dd`eafffa10 00007ffe`c1465597 : 00007ff6`5e843628 00000000`00000000 00000000`00000000 000000dd`eafffb50 : ntdll!RtlpWaitOnAddress+0xb2
03 000000dd`eafffa80 00007ffe`c1424bf4 : 00000000`00000000 00007ff6`5e8411dd 00000000`000007d0 00000000`00000004 : ntdll!RtlpWaitOnCriticalSection+0xdb
04 000000dd`eafffb50 00007ffe`c1424b20 : 00000000`00000000 00000000`00000000 00000000`00000000 00000206`747626a0 : ntdll!RtlpEnterCriticalSectionContended+0xcc
05 000000dd`eafffb80 00007ff6`5e841041 : 00007ff6`5e842270 00000000`00000000 000000dd`eafff9c8 000000dd`eafffba8 : ntdll!RtlEnterCriticalSection+0x40
06 000000dd`eafffbb0 00007ffe`bd96cd70 : 00000000`00080001 00000000`00000000 00000000`00000000 00000000`00000000 : CSLock!thread1+0x41 [cslock.cpp @ 22]
07 000000dd`eafffbe0 00007ffe`becb84d4 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ucrtbase!thread_start<unsigned int (__cdecl*)(void * __ptr64)>+0x40
08 000000dd`eafffc10 00007ffe`c146e851 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x14
09 000000dd`eafffc40 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21

   4  Id: 1914.174 Suspend: 1 Teb: 000000dd`ea98b000 Unfrozen
 # Child-SP          RetAddr           : Args to Child                                                           : Call Site
00 000000dd`eb0ffa98 00007ffe`c14657ff : 00000003`00000003 00000206`7470e8c8 00000000`00000000 00000000`58baa08f : ntdll!NtWaitForAlertByThreadId+0x14
01 000000dd`eb0ffaa0 00007ffe`c1465706 : 00000000`00000000 00000000`00000000 000000dd`eb0ffb78 00000000`58bde547 : ntdll!RtlpWaitOnAddressWithTimeout+0x43
02 000000dd`eb0ffad0 00007ffe`c1465597 : 00007ff6`5e843650 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlpWaitOnAddress+0xb2
03 000000dd`eb0ffb40 00007ffe`c1424bf4 : 00000000`00000000 00007ff6`5e8411dd 00000000`000007d0 00000000`00000004 : ntdll!RtlpWaitOnCriticalSection+0xdb
04 000000dd`eb0ffc10 00007ffe`c1424b20 : 00000000`00000000 00000000`00000000 00000000`00000000 00000206`747625e0 : ntdll!RtlpEnterCriticalSectionContended+0xcc
05 000000dd`eb0ffc40 00007ff6`5e8410b1 : 00007ff6`5e842308 00000000`00000000 000000dd`eb0ffa88 000000dd`eb0ffc68 : ntdll!RtlEnterCriticalSection+0x40
06 000000dd`eb0ffc70 00007ffe`bd96cd70 : 00000000`00080001 00000000`00000000 00000000`00000000 00000000`00000000 : CSLock!thread2+0x41 [cslock.cpp @ 41]
07 000000dd`eb0ffca0 00007ffe`becb84d4 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ucrtbase!thread_start<unsigned int (__cdecl*)(void * __ptr64)>+0x40
08 000000dd`eb0ffcd0 00007ffe`c146e851 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x14
09 000000dd`eb0ffd00 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21
```

2. Find locked critical section

cmd: !cs -l

!cs Address 指定要显示的临界区地址。 如果省略该参数，调试器显示当前进程中所有临界区。!cs -s 如果可能的话，显示每个临界区的初始堆栈回溯。!cs -l 仅显示锁定的临界区。

Critical section   = 0x00007ff65e843650 = 00007ff6`5e843650 matchs thread4 params, which means thread4 is waiting for cs1

OwningThread       = 0x0000000000000174 means the owner of this CS.

LockCount          = 0x1 means a thread is waiting for this CS.

CSLock!cs1 is the CS name.


```
-----------------------------------------
DebugInfo          = 0x00007ffec1550e10
Critical section   = 0x00007ff65e843650 (CSLock!cs1+0x0)
LOCKED
LockCount          = 0x1
WaiterWoken        = No
OwningThread       = 0x0000000000000278
RecursionCount     = 0x1
LockSemaphore      = 0xFFFFFFFF
SpinCount          = 0x00000000020007d0
-----------------------------------------
DebugInfo          = 0x00007ffec1550e40
Critical section   = 0x00007ff65e843628 (CSLock!cs2+0x0)
LOCKED
LockCount          = 0x1
WaiterWoken        = No
OwningThread       = 0x0000000000000174
RecursionCount     = 0x1
LockSemaphore      = 0xFFFFFFFF
SpinCount          = 0x00000000020007d0
```

3. Check owner threads

cmd: ~~[0x0000000000000174/278]

Finds that CS2 is owned by thread4 and CS1 is owned by thread3.

```
0:007> ~~[0x0000000000000174]
   4  Id: 1914.174 Suspend: 1 Teb: 000000dd`ea98b000 Unfrozen
      Start: ucrtbase!thread_start<unsigned int (__cdecl*)(void * __ptr64)> (00007ffe`bd96cd30)
      Priority: 0  Priority class: 32  Affinity: f
0:007> ~~[0x0000000000000278]
   3  Id: 1914.278 Suspend: 1 Teb: 000000dd`ea989000 Unfrozen
      Start: ucrtbase!thread_start<unsigned int (__cdecl*)(void * __ptr64)> (00007ffe`bd96cd30)
      Priority: 0  Priority class: 32  Affinity: f
```

4. Check Code

You know the owner threads and hanging threads now. Use the call stack to review your code.