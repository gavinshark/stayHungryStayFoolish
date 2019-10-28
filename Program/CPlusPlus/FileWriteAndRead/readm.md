This is a simple c++ style file read program(write process is by notepad++)

conclusion:
1. You can not delete a file while another process is openning it with a fstream.
2. A reading process can read the attched content by another process.
3. If the reading ptr is at 100, but another process truncate the file to size 10, the original process can read serveral content from the read buffer but soon the buffer is empty and the read process can not read any more.
4. fstream can not read space and return.