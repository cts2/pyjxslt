package org.pyjxslt;
import org.apache.commons.cli.Options;
import py4j.GatewayServer;


public class StartGateway {
	/**
	 * Start an XSLT Gateway server.
	 * @param args argument
	 */
	public static void main(String[] args) {
		GatewayServer gatewayServer;

		Options options = new Options();
		
		int port = 0;
		if(args.length == 1) {
			try {
		        port = Integer.parseInt(args[0]);
		    } catch (NumberFormatException e) {
		        System.err.println("Invalid Port Number: " + args[0]);
		        System.exit(1);
		    }
		}
		else if(args.length != 0) {
			System.err.println("Usage: StartGateway [port]");
			System.exit(1);
		}
		if(port > 0)
			gatewayServer = new GatewayServer(new Object(), port);
		else
			gatewayServer = new GatewayServer(new Object());

		gatewayServer.start();
		System.out.print("Gateway Server Started on ");
		if(port > 0) {
			System.out.println("port " + port);
		} else {
			System.out.println("default port");
		}
	}
}
