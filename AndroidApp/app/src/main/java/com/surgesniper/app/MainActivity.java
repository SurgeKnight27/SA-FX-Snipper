package com.surgesniper.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {

    private TextView statusText;
    private Button startEngineButton;
    private Button scanMarketButton;
    private Button settingsButton;

    private static final String API_URL =
            "http://10.50.59.115:5000/api/status";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        startEngineButton = findViewById(R.id.startEngineButton);
        scanMarketButton = findViewById(R.id.scanMarketButton);
        settingsButton = findViewById(R.id.settingsButton);

        startEngineButton.setOnClickListener(v -> getStatus());

        scanMarketButton.setOnClickListener(v ->
                Toast.makeText(this,
                        "Market Scan Started",
                        Toast.LENGTH_SHORT).show()
        );

        settingsButton.setOnClickListener(v ->
                Toast.makeText(this,
                        "Settings",
                        Toast.LENGTH_SHORT).show()
        );
    }

    private void getStatus() {

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

                StringBuilder result = new StringBuilder();
                String line;

                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }

                reader.close();

                runOnUiThread(() ->
                        statusText.setText(
                                "🚀 SURGE-SNIPER LIVE\n\n" +
                                result.toString()
                        )
                );

            } catch (Exception e) {

                runOnUiThread(() ->
                        Toast.makeText(
                                this,
                                "Connection Failed",
                                Toast.LENGTH_SHORT
                        ).show()
                );
            }

        }).start();
    }
}
