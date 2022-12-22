package com.example.socketclient;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import android.view.Window;

public class MainActivity extends AppCompatActivity {

    EditText name;
    EditText ip;
    EditText port;
    Button connect;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();

        setContentView(R.layout.activity_main);
        init_setting();
        init_callback();
    }

    private void init_setting(){
        name = (EditText) findViewById(R.id.name_edit_text);
        ip = (EditText) findViewById(R.id.ip_edit_text);
        port = (EditText) findViewById(R.id.port_edit_text);
        connect = (Button)findViewById(R.id.connect_button);
    }

    private void init_callback(){
        connect.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick (View view){
                Bundle bundle = new Bundle();
                bundle.putString("name", name.getText().toString());
                bundle.putString("ip", ip.getText().toString());
                bundle.putString("port", port.getText().toString());

                Intent it = new Intent();

                it.putExtras(bundle);

                it.setClass(MainActivity.this, ModeSelectionActivity.class); 

                startActivity(it);

            }
        });
    }
}