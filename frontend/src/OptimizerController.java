import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;
import org.json.JSONArray;
import java.util.Arrays;

public class OptimizerController {

    private static final String API_URL = "http://localhost:5000/optimize";

    public String sendOptimizationRequest(String stockData) throws Exception {
        HttpURLConnection conn = null;
        try {
            URL url = new URL(API_URL);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // Process stockData: split by commas and trim whitespace
            String[] stocksArray = Arrays.stream(stockData.split(","))
                                         .map(String::trim)
                                         .toArray(String[]::new);

            // Create JSON payload for the API request
            JSONObject requestPayload = new JSONObject();
            requestPayload.put("stocks", stocksArray);

            // Optional: Include target_return if needed
            // requestPayload.put("target_return", 0.1);

            // Send request to the backend
            try (OutputStream os = conn.getOutputStream())  {
                byte[] input = requestPayload.toString().getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            // Check the response code
            int responseCode = conn.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK) {
                // Read error response
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                StringBuilder errorResponse = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorResponse.append(errorLine);
                }
                errorReader.close();
                throw new Exception("API Error: " + errorResponse.toString());
            }

            // Read the backend response
            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
            in.close();

            // Return the response from the backend as a String
            return response.toString();

        } catch (Exception e) {
            throw new Exception("Failed to send optimization request: " + e.getMessage(), e);
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }
}
