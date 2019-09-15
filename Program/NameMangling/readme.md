conclusion:
1. default parameter only affect caller function when compling(replace with default value), not name mangling
2. only one same name extern C function can be defined in one dll.
3. the export sequence is as alphabetical order
4. import is related with name mangling, not with sequence

void func(int a, int b) is called by console


** extern C **

1. void func(int a, int b)
func
func

2. void func(int a, int b=0)
func
func

3. void func(int a, int b, int c)
func
func
depends on the function logic, maybe not error, c is a random value
CAN only one same extern C link in a dll 

4. void func(int a, int b, intc=0)
func
func
depends on the function logic, maybe not error, c is a random value
CAN only one same extern C link in a dll 


** C++ **

1. void func(int a, int b)
?func@@YAXHH@Z
void func(int,int)

2. void func(int a, int b=0)
?func@@YAXHH@Z
void func(int,int)

3. void func(int a, int b, int c)
?func@@YAXHHH@Z
void func(int,int,int)

4. void func(int a, int b, intc=0)
?func@@YAXHHH@Z
void func(int,int,int)
Error cannot find ?func@@YAXHH@Z in exe