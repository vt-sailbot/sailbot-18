#ifndef NETWORK_SERVER_H_
#define NETWORK_SERVER_H_

#include "config.h"
#include "file_buffer.h"

#include <iostream>
#include <queue>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <signal.h>
#include <unistd.h>


extern bool client_connected;

class NetworkServer
{
public:
	NetworkServer();

	void run();

	// Makes sockets
	void make_socket();
	
	// Binds sockets
	void bind_socket();

	// Connect with client
	void connect();

	//sends data from queue to client
	void send_data();


	//void closes connection with client
	void close_connection();

	//Reads data from /tmp/sailbot-fifo and 
	//adds it to the queue
	void enqueue_data();

private:
	static void handle_sigs(int signum);

private:
	bool m_is_running;


	FileBuffer m_file_buffer;

	int m_port_num;

	// Socket file descriptors
	int m_serverfd, m_clientfd;

	// Connection information
	struct sockaddr_in m_server_addr;

	socklen_t m_size;

	std::queue<std::string> m_message_queue;
};

#endif

/*
 *
 * Create Socket
 * Bind address
 * Listen on port
 * Accept connection
 * Send/recieve connection
 * Whatever fancy cleanup on shutdown
 *
 */
