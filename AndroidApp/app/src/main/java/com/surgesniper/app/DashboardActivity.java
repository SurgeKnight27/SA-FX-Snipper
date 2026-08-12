package com.surgesniper.app;

import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DashboardActivity extends AppCompatActivity {

    private TextView engineStatus;
    private TextView price;
    private TextView trend;
    private TextView signal;
    private TextView confidence;

    private TextView balance;
    private TextView equity;
    private TextView profit;

    private TextView marketHunter;
    private TextView riskCommander;
    private TextView brokerStatus;

    private final Handler handler = new Handler();

    /*
     * ========================================
     * LOCAL FLASK DASHBOARD
     * ========================================
     *
     * Flask runs locally on the same Android
     * device through Termux.
     */
    private static final String BASE_URL =
            "http://127.0.0.1:5000";

    private static final String STATUS_URL =
            BASE_URL + "/api/status";

    private static final String ACCOUNT_URL =
            BASE_URL + "/api/account";

    /*
     * Dashboard refresh interval.
     *
     * Previous value:
     * 2000 ms
     *
     * New value:
     * 5000 ms
     *
     * This greatly reduces request frequency and
     * CPU/network activity.
     */
    private static final long REFRESH_INTERVAL =
            5000;

    /*
     * Prevent multiple dashboard requests from
     * running at the same time.
     */
    private volatile boolean requestRunning =
            false;

    /*
     * Only refresh while this Activity is visible.
     */
    private volatile boolean dashboardActive =
            false;

    private final Runnable updater =
            new Runnable() {

                @Override
                public void run() {

                    if (!dashboardActive) {
                        return;
                    }

                    if (!requestRunning) {
                        requestRunning = true;
                        fetchDashboardData();
                    }

                    handler.postDelayed(
                            this,
                            REFRESH_INTERVAL
                    );
                }
            };

    @Override
    protected void onCreate(
            Bundle savedInstanceState
    ) {

        super.onCreate(savedInstanceState);

        setContentView(
                R.layout.activity_dashboard
        );

        engineStatus =
                findViewById(
                        R.id.dashboardEngineStatus
                );

        price =
                findViewById(
                        R.id.dashboardPrice
                );

        trend =
                findViewById(
                        R.id.dashboardTrend
                );

        signal =
                findViewById(
                        R.id.dashboardSignal
                );

        confidence =
                findViewById(
                        R.id.dashboardConfidence
                );

        balance =
                findViewById(
                        R.id.dashboardBalance
                );

        equity =
                findViewById(
                        R.id.dashboardEquity
                );

        profit =
                findViewById(
                        R.id.dashboardProfit
                );

        marketHunter =
                findViewById(
                        R.id.marketHunterStatus
                );

        riskCommander =
                findViewById(
                        R.id.riskCommanderStatus
                );

        brokerStatus =
                findViewById(
                        R.id.brokerStatus
                );

        /*
         * Initial UI state.
         */

        engineStatus.setText(
                "● CONNECTING"
        );

        price.setText("--");

        trend.setText("--");

        signal.setText("--");

        confidence.setText("--%");

        balance.setText("$0.00");

        equity.setText("$0.00");

        profit.setText("$0.00");

        marketHunter.setText(
                "● Market Hunter       CONNECTING"
        );

        riskCommander.setText(
                "● Risk Commander      ACTIVE"
        );

        brokerStatus.setText(
                "● Broker Connection   MT5API CONNECTING"
        );
    }

    @Override
    protected void onResume() {

        super.onResume();

        /*
         * Dashboard becomes active only when
         * actually visible.
         */
        dashboardActive = true;

        handler.removeCallbacks(updater);

        /*
         * Start one immediate refresh.
         */
        handler.post(updater);
    }

    @Override
    protected void onPause() {

        /*
         * Stop dashboard polling immediately when
         * the Activity is no longer visible.
         */
        dashboardActive = false;

        handler.removeCallbacks(updater);

        super.onPause();
    }

    private void fetchDashboardData() {

        new Thread(
                () -> {

                    HttpURLConnection statusConnection =
                            null;

                    HttpURLConnection accountConnection =
                            null;

                    try {

                        /*
                         * ========================================
                         * STATUS API
                         * ========================================
                         */

                        URL statusUrl =
                                new URL(STATUS_URL);

                        statusConnection =
                                (HttpURLConnection)
                                        statusUrl.openConnection();

                        statusConnection.setRequestMethod(
                                "GET"
                        );

                        statusConnection.setConnectTimeout(
                                3000
                        );

                        statusConnection.setReadTimeout(
                                3000
                        );

                        int statusCode =
                                statusConnection
                                        .getResponseCode();

                        if (statusCode != 200) {

                            throw new Exception(
                                    "Status HTTP "
                                            + statusCode
                            );
                        }

                        BufferedReader statusReader =
                                new BufferedReader(
                                        new InputStreamReader(
                                                statusConnection
                                                        .getInputStream()
                                        )
                                );

                        StringBuilder statusResponse =
                                new StringBuilder();

                        String line;

                        while (
                                (line =
                                        statusReader.readLine())
                                        != null
                        ) {

                            statusResponse.append(line);
                        }

                        statusReader.close();

                        JSONObject statusData =
                                new JSONObject(
                                        statusResponse.toString()
                                );

                        /*
                         * ========================================
                         * MARKET DATA
                         * ========================================
                         */

                        String engine =
                                statusData.optString(
                                        "engine",
                                        "OFFLINE"
                                );

                        String broker =
                                statusData.optString(
                                        "broker",
                                        "MT5API"
                                );

                        String brokerState =
                                statusData.optString(
                                        "broker_status",
                                        "OFFLINE"
                                );

                        String marketPrice =
                                statusData.optString(
                                        "price",
                                        "--"
                                );

                        String marketTrend =
                                statusData.optString(
                                        "trend",
                                        "--"
                                );

                        String marketSignal =
                                statusData.optString(
                                        "signal",
                                        "--"
                                );

                        String aiConfidence =
                                statusData.optString(
                                        "confidence",
                                        "0"
                                );

                        String ready =
                                statusData.optString(
                                        "ready",
                                        "false"
                                );

                        /*
                         * ========================================
                         * ACCOUNT API
                         * ========================================
                         */

                        URL accountUrl =
                                new URL(ACCOUNT_URL);

                        accountConnection =
                                (HttpURLConnection)
                                        accountUrl.openConnection();

                        accountConnection.setRequestMethod(
                                "GET"
                        );

                        accountConnection.setConnectTimeout(
                                3000
                        );

                        accountConnection.setReadTimeout(
                                3000
                        );

                        int accountCode =
                                accountConnection
                                        .getResponseCode();

                        if (accountCode != 200) {

                            throw new Exception(
                                    "Account HTTP "
                                            + accountCode
                            );
                        }

                        BufferedReader accountReader =
                                new BufferedReader(
                                        new InputStreamReader(
                                                accountConnection
                                                        .getInputStream()
                                        )
                                );

                        StringBuilder accountResponse =
                                new StringBuilder();

                        while (
                                (line =
                                        accountReader.readLine())
                                        != null
                        ) {

                            accountResponse.append(line);
                        }

                        accountReader.close();

                        JSONObject accountData =
                                new JSONObject(
                                        accountResponse.toString()
                                );

                        /*
                         * ========================================
                         * LIVE ACCOUNT VALUES
                         * ========================================
                         */

                        double balanceValue =
                                accountData.optDouble(
                                        "balance",
                                        0.0
                                );

                        double equityValue =
                                accountData.optDouble(
                                        "equity",
                                        0.0
                                );

                        double profitValue =
                                accountData.optDouble(
                                        "profit",
                                        0.0
                                );

                        String balanceText =
                                String.format(
                                        "$%.2f",
                                        balanceValue
                                );

                        String equityText =
                                String.format(
                                        "$%.2f",
                                        equityValue
                                );

                        String profitText =
                                String.format(
                                        "$%.2f",
                                        profitValue
                                );

                        /*
                         * ========================================
                         * UPDATE UI
                         * ========================================
                         */

                        if (dashboardActive) {

                            runOnUiThread(
                                    () -> {

                                        if (
                                                "ONLINE"
                                                        .equalsIgnoreCase(
                                                                engine
                                                        )
                                        ) {

                                            engineStatus.setText(
                                                    "● ONLINE"
                                            );

                                        } else {

                                            engineStatus.setText(
                                                    "● OFFLINE"
                                            );
                                        }

                                        price.setText(
                                                marketPrice
                                        );

                                        trend.setText(
                                                marketTrend
                                        );

                                        signal.setText(
                                                marketSignal
                                        );

                                        confidence.setText(
                                                aiConfidence
                                                        + "%"
                                        );

                                        balance.setText(
                                                balanceText
                                        );

                                        equity.setText(
                                                equityText
                                        );

                                        profit.setText(
                                                profitText
                                        );

                                        if (
                                                "true"
                                                        .equalsIgnoreCase(
                                                                ready
                                                        )
                                        ) {

                                            marketHunter.setText(
                                                    "● Market Hunter       ONLINE"
                                            );

                                        } else {

                                            marketHunter.setText(
                                                    "● Market Hunter       SCANNING"
                                            );
                                        }

                                        riskCommander.setText(
                                                "● Risk Commander      ACTIVE"
                                        );

                                        brokerStatus.setText(
                                                "● Broker Connection   "
                                                        + broker
                                                        + " "
                                                        + brokerState
                                        );
                                    }
                            );
                        }

                    } catch (Exception e) {

                        if (dashboardActive) {

                            runOnUiThread(
                                    () -> {

                                        engineStatus.setText(
                                                "● OFFLINE"
                                        );

                                        marketHunter.setText(
                                                "● Market Hunter       OFFLINE"
                                        );

                                        brokerStatus.setText(
                                                "● Broker Connection   OFFLINE"
                                        );
                                    }
                            );
                        }

                    } finally {

                        if (
                                statusConnection != null
                        ) {

                            statusConnection.disconnect();
                        }

                        if (
                                accountConnection != null
                        ) {

                            accountConnection.disconnect();
                        }

                        /*
                         * Allow the next scheduled refresh.
                         */
                        requestRunning = false;
                    }

                }
        ).start();
    }

    @Override
    protected void onDestroy() {

        dashboardActive = false;

        handler.removeCallbacks(
                updater
        );

        super.onDestroy();
    }
}
