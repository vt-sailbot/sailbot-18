#include <iostream>

#include "network_server.h"
#include <unistd.h>

int main()
{
	NetworkServer server;	
	server.run();

	return 0;
}
