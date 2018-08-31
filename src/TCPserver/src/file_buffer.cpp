#include "file_buffer.h"

#include <fcntl.h>

FileBuffer::FileBuffer()
{
	//FileBuffer(DEFAULT_FIFO_PATH);
}

FileBuffer::FileBuffer(const char* fifo_path)
{
	m_fifo_path = std::string(fifo_path);

	std::cout << "Created fifo file at: " << fifo_path << std::endl;
	std::ofstream fifo(m_fifo_path);
	fifo.close();


}



void FileBuffer::read_fifo()
{

	//Super ghetto way to do this but it works

	input.open(m_fifo_path.c_str());

	if (!input.is_open())
	{
		puts("It aint open");
	}


	std::string buff;
	while (std::getline( input, buff) )
	{
		std::cout << "buffer: " << buff << std::endl;
		buffer = buff;
	}
	input.close();

	std::ofstream fifo(m_fifo_path);
	fifo.close();
	
}

void FileBuffer::end()
{

}
