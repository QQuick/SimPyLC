import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.StringWriter;
import java.net.Socket;
import java.lang.Math;

import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;

class Client {
    public static void main (String args []) {
        try {
            final var finity = 1e20;
            final var maxMessageLength = 4096;
            var socket = new Socket ("", 50008);
            var sensorStream = new DataInputStream (socket.getInputStream ());
            var actuatorStream = new DataOutputStream (socket.getOutputStream ());
            
            while (true) {
                var sensorBytes = new byte [maxMessageLength];
                sensorStream.readFully (sensorBytes, 0, maxMessageLength);
                var sensorString = new String (sensorBytes, "ASCII");
                sensorString = sensorString.replaceAll (" ", "");
                var sensorParser = new JSONParser ();
                var sensorObject = (JSONObject) sensorParser.parse (sensorString);
                var rawLidarDistances = (JSONArray) sensorObject.get ("lidarDistances");
                var lidarDistances = new double [rawLidarDistances.size ()];

                for (int distanceIndex = 0; distanceIndex < lidarDistances.length; distanceIndex++) {
                    lidarDistances [distanceIndex] = (double) rawLidarDistances.get (distanceIndex);
                }

                var lidarHalfApertureAngle = (int)(long) sensorObject.get ("lidarHalfApertureAngle");

                // ====== BEGIN of control algorithm

                var nearestObstacleDistance = finity;
                var nearestObstacleAngle = 0.;
                
                var nextObstacleDistance = finity;
                var nextObstacleAngle = 0.;

                for (int lidarAngle = -lidarHalfApertureAngle; lidarAngle < lidarHalfApertureAngle; lidarAngle++) {
                    int distanceIndex = lidarAngle < 0 ? lidarAngle + lidarHalfApertureAngle : lidarAngle;
                    var lidarDistance = lidarDistances [distanceIndex];
                    
                    if (lidarDistance < nearestObstacleDistance) {
                        nextObstacleDistance = nearestObstacleDistance;
                        nextObstacleAngle = nearestObstacleAngle;
                        
                        nearestObstacleDistance = lidarDistance;
                        nearestObstacleAngle = lidarAngle;
                    }
                    else if (lidarDistance < nextObstacleDistance) {
                        nextObstacleDistance = lidarDistance;
                        nextObstacleAngle = lidarAngle;
                    }
                }
                
                var targetObstacleDistance = (nearestObstacleDistance + nextObstacleDistance) / 2;
                var targetObstacleAngle = (nearestObstacleAngle + nextObstacleAngle) / 2;
                
                var steeringAngle = targetObstacleAngle;
                var targetVelocity = (90 - Math.abs (steeringAngle) / 60) / 2;

                // ====== END of control algorithm

                var actuatorObject = new JSONObject ();
                actuatorObject.put ("steeringAngle", steeringAngle);
                actuatorObject.put ("targetVelocity", targetVelocity);
                var actuatorStringWriter = new StringWriter ();
                actuatorObject.writeJSONString (actuatorStringWriter);
                var actuatorString = actuatorStringWriter.toString ();

                while (actuatorString.length () < maxMessageLength) {
                    actuatorString += " ";
                }
                var actuatorBytes = actuatorString.getBytes ("ASCII");
                actuatorStream.write (actuatorBytes);
                
            }
        }
        catch (Exception exception) {
            System.out.println (exception.toString ());
        }
    }
}
