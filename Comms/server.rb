#! /bin/ruby

require 'socket'

PORT = 4242

server = TCPServer.new PORT

while true do
		
	Thread.start(client = server.accept) do
		while true do
			client.puts "Some Data"
		end
		client.close
	end	

end
