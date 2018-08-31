#ifndef FILE_BUFFER_H_
#define FILE_BUFFER_H_
#include "config.h"

#include <string>
#include <iostream>
#include <fstream>


class FileBuffer
{
public:
	FileBuffer();
	FileBuffer(const char* fifo_path);


	void read_fifo();	

	void end();

public:
	std::string buffer;

private:
	//fifo file discriptor
	std::fstream input;

	std::string m_fifo_path;



};

#endif
