import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
	private int port;

	private static Vector<Info> list;
	private static Vector<Client> clients;

    public static void main(String[] argv) {
		if(argv.length != 1) {
			System.out.println("Usage: java Server [port]");
			return;
		}

		Server server = new Server(Integer.parseInt(argv[0]));
		server.listen();
	}

	Server(int port) {
		this.port	= port;
		list		= new Vector<Info>();
		clients		= new Vector<Client>();
	}

    private void listen() {
    	ServerSocket serverSocket = null;

    	try {
    		serverSocket = new ServerSocket(this.port);
    		System.out.println("Server listening on port " + this.port);

    		while(true) {
    			Socket socket	= serverSocket.accept();
    			Client client	= new Client(socket);

    			this.clients.add(client);
				this.broadcast();

    			client.start();
    		}
    	} catch(IOException e) {
    		e.printStackTrace();
    	} finally {
    		try {
    			if(serverSocket != null) serverSocket.close();
    		} catch(IOException e) {
    			e.printStackTrace();
    		}
    	}
    }

    private static void broadcast() {
    	for(int i = 0; i < clients.size(); i++) {
    		if(clients.get(i).getState() != Thread.State.TERMINATED) {
				int request = 0;
				clients.get(i).send(request);
				clients.get(i).send(Server.list);
			}
    		else clients.remove(i);
    	}
    }
	
	private static void update() {
		for(int i = 0; i < clients.size(); i++) {
			if(clients.get(i).getState() != Thread.State.TERMINATED) {
				for(int j = 0; j < list.size(); j++) {
					if(clients.get(i).name.equals(list.get(j).name)) clients.get(i).index = j;
				}
			}
    		else clients.remove(i);
		}
	}
	
	private static Client getClient(String name) {
		for(int i = 0; i < clients.size(); i++) {
			if(clients.get(i).name.equals(name))
				return clients.get(i);
		}
		return null;
	}

    class Client extends Thread {
		private Socket socket				= null;
		private ObjectInputStream input		= null;
		private ObjectOutputStream output	= null;

		public Info info	= null;
		public String name	= null;
		public int index	= 0;

    	Client(Socket socket) {
    		this.socket = socket;
    		System.out.println(socket);

    		try {
    			this.input	= new ObjectInputStream(socket.getInputStream());
				this.output	= new ObjectOutputStream(socket.getOutputStream());
			} catch(IOException e) {
				e.printStackTrace();
			} finally {
				try {
					this.name	= (String)this.input.readObject();
					this.index	= Server.list.size();
					this.info	= new Info(this.name, "IDLE");
					Server.list.add(this.info);
					
					Server.broadcast();
				} catch(IOException | ClassNotFoundException e) {
					//e.printStackTrace();
				}
			}
    	}

		@Override
        public void run() {
			try {
				int request = (int)this.input.readObject();
				
				switch(request) {
					// Invite to play
					case 1: {
						String r_name	= (String)this.input.readObject();
						Client rival	= Server.getClient(r_name);
						if(rival != null) rival.send(request);
						break;
					}
					// Play game
					case 2: {
						
						break;
					}
				}

			} catch(Exception e) {				
				Server.list.remove(index);
				this.info.state = "EXIT";
				
				Server.broadcast();
				Server.update();
			}
        }

        private void send(Object object) {
        	try {
        		this.output.reset();
        		this.output.writeObject(object);
        	} catch(IOException e) {
        		//e.printStackTrace();
        	}
        }
    }
}
