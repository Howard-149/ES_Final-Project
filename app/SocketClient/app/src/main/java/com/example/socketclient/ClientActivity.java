package com.example.socketclient;

import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.text.method.ScrollingMovementMethod;
import android.util.Pair;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.Socket;
import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import androidx.appcompat.app.AppCompatActivity;



public class ClientActivity extends AppCompatActivity { //主執行緒，也稱UI執行緒，負責更新UI介面，禁止存取網路

    private Button leave_btn;
    private Button send_btn;
    private EditText input_edit_text;
    private TextView content_text;
    private TextView hello_text;

    private TextView server_ip_text;
    private TextView server_port_text;

    private TextView user_phone_key_text;
    private Button user_phone_key_btn;
    private TextView user_line_key_text;
    private Button user_line_key_btn;

    private TextView bluetooth_threshold_text;
    private Button bluetooth_threshold_btn;


    private ClientThread clientThread;
    private Socket socket;
    private String name;
    private String ip;
    private int port;

    private  BufferedReader read;
    private  DataOutputStream write;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();

        setContentView(R.layout.activity_client);

        init_setting();
        init_callback();
        init_client();

    }

    private void init_setting(){
        leave_btn=(Button)findViewById(R.id.leave_btn);
        send_btn=(Button)findViewById(R.id.send_btn);
        input_edit_text=(EditText)findViewById(R.id.input_edit_text);
        content_text=(TextView)findViewById(R.id.content_text);
        hello_text=(TextView)findViewById(R.id.hello_text);
        content_text.setMovementMethod(ScrollingMovementMethod.getInstance()); // 更新文字時自動滾動到最後一行

        server_ip_text=(TextView)findViewById(R.id.socket_info_ip);
        server_port_text=(TextView)findViewById(R.id.socket_info_port);

        user_phone_key_text=(TextView)findViewById(R.id.user_phone_key);
        user_phone_key_btn = (Button)findViewById(R.id.user_phone_key_btn);

        user_line_key_text=(TextView)findViewById(R.id.user_line_key);
        user_line_key_btn=(Button)findViewById(R.id.user_line_key_btn);

        bluetooth_threshold_text=(TextView)findViewById(R.id.bluetooth_threshold);
        bluetooth_threshold_btn=(Button)findViewById(R.id.bluetooth_threshold_btn);
    }


    public void sendJSON(String... strList) {
        List<String> keys = new ArrayList();
        List<String> values = new ArrayList();
        for(int i = 0 ; i < strList.length ; i += 2) {
            keys.add(strList[i]);
            values.add(strList[i+1]);
        }
        System.out.println(keys);
        System.out.println(values);
        connect(keys,values);
    }


    private void init_callback(){
        send_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                senddata(input_edit_text.getText().toString());
                input_edit_text.setText("");
            }
        });
        leave_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                disconnect();
            }
        });

        user_phone_key_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendJSON(
                        "client","Phone",
                        "task","phone requests for setting user key"
                );
            }
        });

        user_line_key_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendJSON(
                        "client", "Phone",
                        "task", "phone requests for setting user line key"
                );
            }
        });

        bluetooth_threshold_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendJSON(
                        "client", "Phone",
                        "task", "phone requests for setting bluetooth threshold"
                );
            }
        });

    }


    private void init_client() {

        Intent it = this.getIntent();
        if (it != null) {

            Bundle bundle = it.getExtras();

            if (bundle != null) {

                name = bundle.getString("name");
                ip = bundle.getString("ip");
                port = Integer.parseInt(bundle.getString("port"));

                if (name != null && !name.equals("")) {
                    hello_text.setText("Hi! " + name);
                }
            }
        }


        clientThread = new ClientThread();
        clientThread.start();

    }
    private void connect(List<String> keys, List<String> values){
        Connect connect = new Connect(keys,values);
        connect.start();
    }
    private void disconnect(){
        try {
            socket.close();
            finish();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    private void senddata(String msg){
        SendDataThread sendDataThread = new SendDataThread(msg);
        sendDataThread.start();
    }

    class ClientThread extends Thread{ 

        String input;
        String output;

        public void reLoadConfig(JSONObject config) throws JSONException {
            JSONObject socketInfo = config.getJSONObject("socket info");
            JSONObject userInfo = config.getJSONObject("user");
            JSONObject bluetooth = config.getJSONObject("bluetooth");

            String newText = "Configuration";

            String serverIPText = "Server ip : " + socketInfo.get("ip").toString();
            String serverPortText = "Server port : " + socketInfo.get("port").toString();

            String userPhoneKeyText = "Phone BT MAC address : \n        " + userInfo.get("user_phone_key").toString();
            String userLineKeyText = userInfo.get("user_line_key").toString();

            String bluetoothThresholdText = "RSSI threshold : " + bluetooth.get("rssi_threshold");


            runOnUiThread(() -> {
                hello_text.setText(newText);

                server_ip_text.setText(serverIPText);
                server_port_text.setText(serverPortText);

                user_phone_key_text.setText(userPhoneKeyText);
                user_line_key_text.setText(userLineKeyText);

                bluetooth_threshold_text.setText(bluetoothThresholdText);
            });
        }


        @Override
        public void run() {
            try{
                runOnUiThread(() -> hello_text.setText("Connecting..."));

                socket = new Socket(ip, port);
                read = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                write = new DataOutputStream(socket.getOutputStream());

                sendJSON("client", "Phone");

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                sendJSON(
                        "client", "Phone",
                        "task", "phone requests for config"
                );
                input = read.readLine();
                JSONObject config = new JSONObject((input));
                System.out.println(input);

                reLoadConfig(config);


                while ((input = read.readLine())!=null) {
                    System.out.println("Recieved Data");
                    System.out.println(input);
                    JSONObject json_ob = new JSONObject(input);

                    if (!json_ob.has("task"))
                    {
                        reLoadConfig(json_ob);
                        continue;
                    }
                    else if(json_ob.getString("task").equals("done"))   runOnUiThread(() -> content_text.append("Task done!\n"));


                    String get_task = json_ob.getString("task");
                    String get_msg = json_ob.getString("msg");

                    if  (get_task.equals("print log"))
                    {
                        output = get_msg.replace('*','\n');
                        runOnUiThread(() -> content_text.setText(output));
                    }
                    else if (get_task.equals("get line key"))
                    {
                        output = "Please enter your line key\n";
                        runOnUiThread(() -> content_text.setText(output));
                    }

                }

                finish();
            }
            catch(IOException | JSONException e){
                e.printStackTrace();
            }
        }
    }
    class Connect extends Thread{

        List< Pair<String,String> > l;

        public Connect(List<String> keys,List<String> values){
            l = new ArrayList<>();
            for(int i = 0 ; i < keys.size() ; i ++)
            {
                l.add(new Pair<>(keys.get(i), values.get(i)));
            }
        }
        @Override
        public void run() {



            try{
                Map map=new HashMap();
                for(int i = 0 ; i < l.size() ; i ++)
                    map.put(l.get(i).first,l.get(i).second);

                JSONObject value = new JSONObject(map);
                byte[] jsonByte = (value.toString()+"\n").getBytes();

                write.write(jsonByte);
                write.flush();
            }
            catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    class SendDataThread extends Thread{

        String msg;
        String mode;

        public SendDataThread(String M,String m){
            mode = M;
            msg = m;
        }

        public SendDataThread(String m){
            mode = "";
            msg = m;
        }

        @Override
        public void run() {
            try{

                Map map = new HashMap();
                if(!mode.equals(""))
                    map.put("mode",mode);
                map.put("msg",msg);

                JSONObject value = new JSONObject(map);
                byte[] jsonByte = (value.toString()+"\n").getBytes();

                write.write(jsonByte);
                write.flush();
            }
            catch(IOException e){
                e.printStackTrace();
            }
        }
    }


}

