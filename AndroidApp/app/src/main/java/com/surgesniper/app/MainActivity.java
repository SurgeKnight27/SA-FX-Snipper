package com.surgesniper.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {

    private TextView statusText;
    private TextView priceText;
    private TextView trendText;
    private TextView signalText;
    private TextView confidenceText;

    private boolean engineRunning = false;

    private static final String API_URL =
            "http://10.48.81.190:5001/api/status";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        priceText = findViewById(R.id.priceText);
        trendText = findViewById(R.id.trendText);
        signalText = findViewById(R.id.signalText);
        confidenceText = findViewById(R.id.confidenceText);

        Button startEngineButton =
                findViewById(R.id.startEngineButton);

        Button stopEngineButton =
                findViewById(R.id.stopEngineButton);

        Button scanMarketButton =
                findViewById(R.id.scanMarketButton);

        Button dashboardButton =
                findViewById(R.id.dashboardButton);

        Button settingsButton =
                findViewById(R.id.settingsButton);


        // INITIAL STATE

        statusText.setText("🔴 ENGINE : OFFLINE");

        priceText.setText("Price : --");
        trendText.setText("Trend : --");
        signalText.setText("Signal : --");
        confidenceText.setText("Confidence : --");


        // START ENGINE

        startEngineButton.setOnClickListener(v -> {

            engineRunning = true;

            statusText.setText("🟢 ENGINE : ONLINE");

            Toast.makeText(
                    MainActivity.this,
                    "Surge-Sniper Engine ONLINE",
                    Toast.LENGTH_SHORT
            ).show();
        });


        // STOP ENGINE

        stopEngineButton.setOnClickListener(v -> {

            engineRunning = false;

            statusText.setText("🔴 ENGINE : OFFLINE");

            Toast.makeText(
                    MainActivity.this,
                    "Surge-Sniper Engine OFFLINE",
                    Toast.LENGTH_SHORT
            ).show();
        });


        // SCAN MARKET

        scanMarketButton.setOnClickListener(v -> {

            if (!engineRunning) {

                Toast.makeText(
                        MainActivity.this,
                        "START ENGINE FIRST",
                        Toast.LENGTH_SHORT
                ).show();

                return;
            }

            priceText.setText("Price : SCANNING...");
            trendText.setText("Trend : ANALYZING...");
            signalText.setText("Signal : ANALYZING...");
            confidenceText.setText("Confidence : CALCULATING...");

            fetchMarketData();
        });


        // DASHBOARD

        dashboardButton.setOnClickListener(v -> {

            try {

                startActivity(
                        new android.content.Intent(
                                MainActivity.this,
                                DashboardActivity.class
                        )
                );

            } catch (Exception e) {

                Toast.makeText(
                        MainActivity.this,
                        "Dashboard unavailable",
                        Toast.LENGTH_SHORT
                ).show();
            }
        });


        // SETTINGS

        settingsButton.setOnClickListener(v -> {

            Toast.makeText(
                    MainActivity.this,
                    "Settings Coming Soon",
                    Toast.LENGTH_SHORT
            ).show();
        });
    }


    // ============================================
    // LIVE MARKET DATA
    // ============================================

    private void fetchMarketData() {

        new Thread(() -> {

            HttpURLConnection connection = null;

            try {

                URL url = new URL(API_URL);

                connection =
                        (HttpURLConnection) url.openConnection();

                connection.setRequestMethod("GET");
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(5000);

                int responseCode =
                        connection.getResponseCode();

                if (responseCode != 200) {

                    throw new Exception(
                            "HTTP " + responseCode
                    );
                }

                BufferedReader reader =
                        new BufferedReader(
                                new InputStreamReader(
                                        connection.getInputStream()
                                )
                        );

                StringBuilder response =
                        new StringBuilder();

                String line;

                while ((line = reader.readLine()) != null) {

                    response.append(line);
                }

                reader.close();

                JSONObject data =
                        new JSONObject(response.toString());

                String price =
                        data.optString("price", "--");

                String trend =
                        data.optString("trend", "--");

                String signal =
                        data.optString("signal", "--");

                String confidence =
                        data.optString("confidence", "--");

                String engine =
                        data.optString("engine", "OFFLINE");

                runOnUiThread(() -> {

                    statusText.setText(
                            "🟢 ENGINE : " + engine
                    );

                    priceText.setText(
                            "Price : " + price
                    );

                    trendText.setText(
                            "Trend : " + trend
                    );

                    signalText.setText(
                            "Signal : " + signal
                    );

                    confidenceText.setText(
                            "Confidence : " + confidence + "%"
                    );

                    Toast.makeText(
                            MainActivity.this,
                            "Live Market Data Updated",
                            Toast.LENGTH_SHORT
                    ).show();
                });

            } catch (Exception e) {

                runOnUiThread(() -> {

                    statusText.setText(
                            "🔴 ENGINE : OFFLINE"
                    );

                    priceText.setText(
                            "Price : --"
                    );

                    trendText.setText(
                            "Trend : --"
                    );

                    signalText.setText(
                            "Signal : --"
                    );

                    confidenceText.setText(
                            "Confidence : --"
                    );

                    Toast.makeText(
                            MainActivity.this,
                            "Backend connection failed",
                            Toast.LENGTH_SHORT
                    ).show();
                });

            } finally {

                if (connection != null) {
                    connection.disconnect();
                }
            }

        }).start();
    }
}
