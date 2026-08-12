package com.surgesniper.app;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
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

    private final Handler handler = new Handler();

    /*
     * ========================================
     * LOCAL FLASK DASHBOARD
     * ========================================
     *
     * Flask is running in Termux on the same
     * Android device.
     *
     * 127.0.0.1:5000 has already been verified
     * from Termux with /api/status.
     */
    private static final String BASE_URL =
            "http://127.0.0.1:5000";

    private static final String API_URL =
            BASE_URL + "/api/status";

    /*
     * ========================================
     * CONTINUOUS SCANNER
     * ========================================
     */

    private final Runnable scanner = new Runnable() {

        @Override
        public void run() {

            if (!engineRunning) {
                return;
            }

            fetchMarketData();

            handler.postDelayed(
                    this,
                    2000
            );
        }
    };

    /*
     * ========================================
     * ACTIVITY START
     * ========================================
     */

    @Override
    protected void onCreate(
            Bundle savedInstanceState
    ) {

        super.onCreate(savedInstanceState);

        setContentView(
                R.layout.activity_main
        );

        statusText =
                findViewById(
                        R.id.statusText
                );

        priceText =
                findViewById(
                        R.id.priceText
                );

        trendText =
                findViewById(
                        R.id.trendText
                );

        signalText =
                findViewById(
                        R.id.signalText
                );

        confidenceText =
                findViewById(
                        R.id.confidenceText
                );

        Button startEngineButton =
                findViewById(
                        R.id.startEngineButton
                );

        Button stopEngineButton =
                findViewById(
                        R.id.stopEngineButton
                );

        Button scanMarketButton =
                findViewById(
                        R.id.scanMarketButton
                );

        Button dashboardButton =
                findViewById(
                        R.id.dashboardButton
                );

        Button settingsButton =
                findViewById(
                        R.id.settingsButton
                );

        /*
         * ========================================
         * INITIAL STATE
         * ========================================
         */

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

        /*
         * ========================================
         * START ENGINE
         * ========================================
         */

        startEngineButton.setOnClickListener(v -> {

            if (engineRunning) {

                Toast.makeText(
                        MainActivity.this,
                        "Engine already running",
                        Toast.LENGTH_SHORT
                ).show();

                return;
            }

            engineRunning = true;

            statusText.setText(
                    "🟢 ENGINE : ONLINE"
            );

            Toast.makeText(
                    MainActivity.this,
                    "Surge-Sniper Engine ONLINE",
                    Toast.LENGTH_SHORT
            ).show();

            /*
             * Start continuous market polling.
             */
            handler.removeCallbacks(
                    scanner
            );

            handler.post(
                    scanner
            );
        });

        /*
         * ========================================
         * STOP ENGINE
         * ========================================
         */

        stopEngineButton.setOnClickListener(v -> {

            engineRunning = false;

            handler.removeCallbacks(
                    scanner
            );

            statusText.setText(
                    "🔴 ENGINE : OFFLINE"
            );

            Toast.makeText(
                    MainActivity.this,
                    "Surge-Sniper Engine OFFLINE",
                    Toast.LENGTH_SHORT
            ).show();
        });

        /*
         * ========================================
         * SCAN MARKET
         * ========================================
         */

        scanMarketButton.setOnClickListener(v -> {

            if (!engineRunning) {

                Toast.makeText(
                        MainActivity.this,
                        "START ENGINE FIRST",
                        Toast.LENGTH_SHORT
                ).show();

                return;
            }

            priceText.setText(
                    "Price : SCANNING..."
            );

            trendText.setText(
                    "Trend : ANALYZING..."
            );

            signalText.setText(
                    "Signal : ANALYZING..."
            );

            confidenceText.setText(
                    "Confidence : CALCULATING..."
            );

            /*
             * Immediate market request.
             */
            fetchMarketData();

            /*
             * Keep continuous scanner alive.
             */
            handler.removeCallbacks(
                    scanner
            );

            handler.postDelayed(
                    scanner,
                    2000
            );
        });

        /*
         * ========================================
         * DASHBOARD
         * ========================================
         */

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

        /*
         * ========================================
         * SETTINGS
         * ========================================
         */

        settingsButton.setOnClickListener(v -> {

            Toast.makeText(
                    MainActivity.this,
                    "Settings Coming Soon",
                    Toast.LENGTH_SHORT
            ).show();
        });
    }

    /*
     * ========================================
     * LIVE MARKET DATA
     * ========================================
     */

    private void fetchMarketData() {

        new Thread(() -> {

            HttpURLConnection connection = null;

            try {

                URL url =
                        new URL(API_URL);

                connection =
                        (HttpURLConnection)
                                url.openConnection();

                connection.setRequestMethod(
                        "GET"
                );

                connection.setConnectTimeout(
                        5000
                );

                connection.setReadTimeout(
                        5000
                );

                int responseCode =
                        connection.getResponseCode();

                if (responseCode != 200) {

                    throw new Exception(
                            "HTTP "
                                    + responseCode
                    );
                }

                BufferedReader reader =
                        new BufferedReader(
                                new InputStreamReader(
                                        connection
                                                .getInputStream()
                                )
                        );

                StringBuilder response =
                        new StringBuilder();

                String line;

                while (
                        (line = reader.readLine())
                                != null
                ) {

                    response.append(line);
                }

                reader.close();

                JSONObject data =
                        new JSONObject(
                                response.toString()
                        );

                String price =
                        data.optString(
                                "price",
                                "--"
                        );

                String trend =
                        data.optString(
                                "trend",
                                "--"
                        );

                String signal =
                        data.optString(
                                "signal",
                                "--"
                        );

                String confidence =
                        data.optString(
                                "confidence",
                                "--"
                        );

                String engine =
                        data.optString(
                                "engine",
                                "OFFLINE"
                        );

                String broker =
                        data.optString(
                                "broker",
                                "MT5API"
                        );

                String feed =
                        data.optString(
                                "feed",
                                "LIVE"
                        );

                runOnUiThread(() -> {

                    /*
                     * A temporary backend failure must
                     * not automatically stop the local
                     * engine state.
                     */
                    if (engineRunning) {

                        statusText.setText(
                                "🟢 ENGINE : ONLINE"
                        );
                    }

                    priceText.setText(
                            "Price : "
                                    + price
                    );

                    trendText.setText(
                            "Trend : "
                                    + trend
                    );

                    signalText.setText(
                            "Signal : "
                                    + signal
                    );

                    confidenceText.setText(
                            "Confidence : "
                                    + confidence
                                    + "%"
                    );
                });

            } catch (Exception e) {

                runOnUiThread(() -> {

                    /*
                     * Do NOT set engineRunning=false.
                     *
                     * The scanner will automatically
                     * retry on its next cycle.
                     */
                    if (engineRunning) {

                        statusText.setText(
                                "🟡 ENGINE : RETRYING"
                        );
                    }
                });

            } finally {

                if (connection != null) {

                    connection.disconnect();
                }
            }

        }).start();
    }

    /*
     * ========================================
     * CLEAN SHUTDOWN
     * ========================================
     */

    @Override
    protected void onDestroy() {

        handler.removeCallbacks(
                scanner
        );

        engineRunning = false;

        super.onDestroy();
    }
}
