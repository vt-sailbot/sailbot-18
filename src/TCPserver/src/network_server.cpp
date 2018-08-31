#include "network_server.h"

bool client_connected;

NetworkServer::NetworkServer()
{
	std::cout << "Starting TCP_Server" << std::endl;	
	m_file_buffer = FileBuffer("/tmp/sailbot-fifo");

	m_is_running = true;
	m_port_num = DEFAULT_SERVER_PORT;
}


void NetworkServer::run()
{

	make_socket();
	bind_socket();

	//signal(SIGPIPE, SIG_IGN);

	while (m_is_running)
	{
		connect();

		send_data();

		close_connection();
	}

}

void NetworkServer::make_socket()
{
	m_clientfd = socket(AF_INET, SOCK_STREAM, 0);

	if (m_clientfd < 0)
	{
		std::cout << "Error Establishing client socket" << std::endl;
		exit(1);
	}

	std::cout << "Socket server created" << std::endl;

	// set up server info
	m_server_addr.sin_family = AF_INET;
	m_server_addr.sin_addr.s_addr = htons(INADDR_ANY);
	m_server_addr.sin_port = htons(m_port_num);
}

void NetworkServer::bind_socket()
{
	if ( (bind(m_clientfd, (struct sockaddr*) &m_server_addr,
					sizeof(m_server_addr))) < 0 )
	{
		std::cout << "Error, socket already established" << std::endl;
		exit(1);
	}

	m_size = sizeof(m_server_addr);
}

void NetworkServer::connect()
{
	std::cout << "Waiting for client connection" << std::endl;

	listen(m_clientfd, 1);

	m_serverfd = accept(m_clientfd, (struct sockaddr *)&m_server_addr, &m_size);

	if (m_serverfd < 0)
	{
		std::cout << "Error accepting client" << std::endl;
	}
	else
	{
		std::cout << "Client Accepted" << std::endl;
	}
}

void NetworkServer::send_data()
{

	client_connected = true;

	signal(SIGPIPE, NetworkServer::handle_sigs);

	while(m_serverfd > 0 && client_connected)
	{
		enqueue_data();
		
		while (!m_message_queue.empty())
		{

			std::string message;

			message = m_message_queue.front();
			m_message_queue.pop();
			
			std::cout << "Sending data to client: " << message << std::endl;

			message.push_back('\n');
			send(m_serverfd, message.c_str(), message.size(), 0);
		}

		m_message_queue = std::queue<std::string>();

		usleep(DEFAULT_SEND_WAIT_TIME);
	}
	std::cout << "Client Disconnected" << std::endl;
}

void NetworkServer::close_connection()
{
	std::cout << "Terming connection with client IP: " << 
		inet_ntoa(m_server_addr.sin_addr) << std::endl;

	close(m_serverfd);
} 

void NetworkServer::enqueue_data()
{
	m_file_buffer.read_fifo();
	if (m_file_buffer.buffer.size() != 0)
	{
		m_message_queue.push(m_file_buffer.buffer);
	}
	m_file_buffer.buffer.clear();
}

void NetworkServer::handle_sigs(int signum)
{
	std::cout << "Caught signal: " << signum << std::endl;
	client_connected = false;
}
