import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

class Client {
    public static void main (String args []) {
        try {
            final var maxMessageLength = 256;
            var socket = new Socket ("", 50008);
            var inStream = new DataInputStream (socket.getInputStream ());
            var outStream = new DataOutputStream (socket.getOutputStream ());
            
            for (int  counter = -1; ; counter--) {
                var counterString = Integer.toString (counter);

                while (counterString.length () < maxMessageLength) {
                    counterString += " ";
                }

                var counterBytes = counterString.getBytes ("ASCII");
                outStream.write (counterBytes);
                var inBytes = new byte [maxMessageLength];
                inStream.readFully (inBytes, 0, maxMessageLength);
                var inString = new String (inBytes, "ASCII");
                System.out.println (inString.replaceAll (" ", ""));
            }
        }
        catch (Exception exception) {
            System.out.println (exception.toString ());
        }
    }
}
