It is recommended by Microsoft to use the same FileMapping Object Handle to share memory between different processes. No matter named FileMapping Object or handle dupicating or handle inherit.

But it is verified that seperate file mapping object of a same shared file in 2 processes can still share memory.

I think it is not recommended.