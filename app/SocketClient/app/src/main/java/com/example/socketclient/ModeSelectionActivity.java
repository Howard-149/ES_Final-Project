package com.example.socketclient;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;

public class ModeSelectionActivity extends AppCompatActivity {

    private String name;
    private String ip;
    private int port;

    Button config;
    Button todolist;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();

        setContentView(R.layout.activity_mode_selection);
        init_setting();
        init_callback();
        init_variables();
    }

    private void init_setting(){
        config = (Button)findViewById(R.id.config_button);
        todolist = (Button)findViewById(R.id.todolist_button);
    }

    private void init_callback(){
        config.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick (View view){
                Bundle bundle = new Bundle();
                bundle.putString("name", name);
                bundle.putString("ip", ip);
                bundle.putString("port", Integer.toString(port));

                Intent it = new Intent();
                it.putExtras(bundle);
                it.setClass(ModeSelectionActivity.this, ClientActivity.class);
                startActivity(it);
            }
        });

        todolist.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Bundle bundle = new Bundle();
                bundle.putString("name", name);
                bundle.putString("ip", ip);
                bundle.putString("port", Integer.toString(port));

                Intent it = new Intent();
                it.putExtras(bundle);
                it.setClass(ModeSelectionActivity.this, TodoListActivity.class);
                startActivity(it);
            }
        });
    }

    private void init_variables(){
        Intent it = this.getIntent();
        if (it != null) {

            Bundle bundle = it.getExtras();

            if (bundle != null) {

                name = bundle.getString("name");
                ip = bundle.getString("ip");
                port = Integer.parseInt(bundle.getString("port"));
            }
        }
    }
}