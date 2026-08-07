package com.surgesniper.app;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {

    private TextView statusText;
    private Button startEngineButton;
    private Button scanMarketButton;
    private Button settingsButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        startEngineButton = findViewById(R.id.startEngineButton);
        scanMarketButton = findViewById(R.id.scanMarketButton);
        settingsButton = findViewById(R.id.settingsButton);

        startEngineButton.setOnClickListener(v -> {
            statusText.setText(
                    "🚀 SURGE-SNIPER\n\n" +
                    "🤖 AI ENGINE        🟢 ONLINE\n\n" +
                    "📡 MARKET HUNTER    🟢 READY\n\n" +
                    "🛡 RISK COMMANDER   🟢 ACTIVE\n\n" +
                    "Broker: Exness Demo\n" +
                    "Status: Connected"
            );

            Toast.makeText(this, "Engine Started", Toast.LENGTH_SHORT).show();
        });

        scanMarketButton.setOnClickListener(v ->
                Toast.makeText(this, "Market Scan Started", Toast.LENGTH_SHORT).show()
        );

        settingsButton.setOnClickListener(v ->
                Toast.makeText(this, "Settings", Toast.LENGTH_SHORT).show()
        );
    }
}
