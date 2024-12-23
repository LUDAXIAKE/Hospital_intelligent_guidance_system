import java.io.*;
import java.net.Socket;

public class DataGet {
    private final String serverAddress = "localhost";
    private final int port = 5001;
    private String data;

    public void communication() {
        try (Socket socket = new Socket(serverAddress, port);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            String data = in.readLine();
            System.out.println("Received from server: " + data);

            this.data = data;

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getData() {
        return data;
    }
}
