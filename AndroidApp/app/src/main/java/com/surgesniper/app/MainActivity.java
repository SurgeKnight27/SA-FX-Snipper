package com.surgesniper.app;

import android.app.Activity;
import android.content.Intent;
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

    private Button startEngineButton;
    private Button stopEngineButton;
    private Button scanMarketButton;
    private Button dashboardButton;
    private Button settingsButton;

    private boolean engineRunning = true;

    private static final String API_URL =
            "http://10.50.59.115:5000/api/status";

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        priceText = findViewById(R.id.priceText);
        trendText = findViewById(R.id.trendText);
        signalText = findViewById(R.id.signalText);
        confidenceText = findViewById(R.id.confidenceText);

        startEngineButton = findViewById(R.id.startEngineButton);
        stopEngineButton = findViewById(R.id.stopEngineButton);
        scanMarketButton = findViewById(R.id.scanMarketButton);
        dashboardButton = findViewById(R.id.dashboardButton);
        settingsButton = findViewById(R.id.settingsButton);

        startEngineButton.setOnClickListener(v -> {

            engineRunning = true;
            statusText.setText("🟢 Engine : ONLINE");

            Toast.makeText(
                    MainActivity.this,
                    "Engine Started",
                    Toast.LENGTH_SHORT
            ).show();

        });

        stopEngineButton.setOnClickListener(v -> {

            engineRunning = false;
            statusText.setText("🔴 Engine : OFFLINE");

            Toast.makeText(
                    MainActivity.this,
                    "Engine Stopped",
                    Toast.LENGTH_SHORT
            ).show();

        });

        scanMarketButton.setOnClickListener(v -> {

            if (!engineRunning) {

                Toast.makeText(
                        MainActivity.this,
                        "Start the Engine First",
                        Toast.LENGTH_SHORT
                ).show();

                return;
            }

            fetchMarketData();

        });

        dashboardButton.setOnClickListener(v -> {

            Intent intent =
                    new Intent(
                            MainActivity.this,
                            DashboardActivity.class
                    );

            startActivity(intent);

        });

        settingsButton.setOnClickListener(v -> {

            Toast.makeText(
                    MainActivity.this,
                    "Settings Coming Soon",
                    Toast.LENGTH_SHORT
            ).show();

        });

    }

    private void fetchMarketData() {

        new Thread(() -> {

            try {

                URL url = new URL(API_URL);

                HttpURLConnection connection =
                        (HttpURLConnection) url.openConnection();

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

                JSONObject json =
                        new JSONObject(response.toString());

                runOnUiThread(() -> {

                    priceText.setText(
                            "Price : " +
                            json.optString("price", "--")
                    );

                    trendText.setText(
                            "Trend : " +
                            json.optString("trend", "--")
                    );

                    signalText.setText(
                            "Signal : " +
                            json.optString("signal", "--")
                    );

                    confidenceText.setText(
                            "Confidence : " +
                            json.optString("confidence", "--") +
                            "%"
                    );

                });

            } catch (Exception e) {

                runOnUiThread(() ->

                        Toast.makeText(
                                MainActivity.this,
                                "Dashboard Offline",
                                Toast.LENGTH_SHORT
                        ).show()

                );

            }

        }).start();

    }

}
