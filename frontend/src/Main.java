import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.json.JSONObject;
import org.json.JSONArray;

public class Main extends Application {

    private TextArea resultArea; // Result display area

    @Override
    public void start(Stage stage) {
        TextField stockInput = new TextField();
        stockInput.setPromptText("Enter stock tickers (e.g., AAPL, MSFT)");

        Button optimizeButton = new Button("Optimize Portfolio");

        resultArea = new TextArea();
        resultArea.setEditable(false); // Result area should be non-editable
        resultArea.setPrefHeight(300);
        resultArea.setWrapText(true);

        VBox vbox = new VBox(10, stockInput, optimizeButton, resultArea);
        vbox.setPadding(new Insets(20, 20, 20, 20));
        Scene scene = new Scene(vbox, 500, 400);
        stage.setScene(scene);
        stage.setTitle("Portfolio Optimizer");
        stage.show();

        optimizeButton.setOnAction(e -> {
            String stockData = stockInput.getText().trim();
            if (validateInput(stockData)) {
                try {
                    // Call the API for portfolio optimization (via OptimizerController)
                    OptimizerController controller = new OptimizerController();
                    String response = controller.sendOptimizationRequest(stockData);

                    // Parse and display the response
                    displayResults(response);
                } catch (Exception ex) {
                    resultArea.setText("Error: Could not optimize portfolio.\n" + ex.getMessage());
                    ex.printStackTrace();
                }
            } else {
                resultArea.setText("Invalid input. Please enter stock tickers separated by commas (e.g., AAPL, MSFT).");
            }
        });
    }

    // Display the optimization results in the result area
    private void displayResults(String response) {
        try {
            JSONObject jsonResponse = new JSONObject(response);
            String status = jsonResponse.getString("status");

            if (status.equals("success")) {
                JSONObject performance = jsonResponse.getJSONObject("performance");
                JSONObject optimizedWeights = jsonResponse.getJSONObject("optimized_weights");

                StringBuilder resultBuilder = new StringBuilder();
                resultBuilder.append("Optimized Portfolio Weights:\n");

                // Iterate through optimized_weights and display each stock and its weight
                for (String key : optimizedWeights.keySet()) {
                    double weight = optimizedWeights.getDouble(key) * 100;
                    resultBuilder.append(String.format("%s: %.2f%%\n", key, weight));
                }

                resultBuilder.append("\nPerformance Metrics:\n");
                resultBuilder.append(String.format("Expected Annual Return: %.2f%%\n", performance.getDouble("expected_return") * 100));
                resultBuilder.append(String.format("Risk (Std Dev): %.2f%%\n", performance.getDouble("risk") * 100));
                resultBuilder.append(String.format("Sharpe Ratio: %.2f\n", performance.getDouble("sharpe_ratio")));

                resultArea.setText(resultBuilder.toString());

            } else {
                String message = jsonResponse.getString("message");
                resultArea.setText("Error: " + message);
            }

        } catch (Exception e) {
            resultArea.setText("Error parsing response from server.");
            e.printStackTrace();
        }
    }

    // Validate the input (basic validation for now)
    private boolean validateInput(String stockData) {
        return stockData != null && stockData.matches("([A-Za-z]{1,5})(,\\s*[A-Za-z]{1,5})*");
    }

    public static void main(String[] args) {
        launch(args);
    }
}
