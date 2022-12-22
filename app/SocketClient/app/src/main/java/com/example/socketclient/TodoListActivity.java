package com.example.socketclient;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.Pair;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.socketclient.Adapter.ToDoAdapter;
import com.example.socketclient.Model.ToDoModel;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.Socket;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TodoListActivity extends AppCompatActivity implements DialogCloseListener{

    private RecyclerView taskRecyclerView;
    private ToDoAdapter tasksAdapter;
    public List<ToDoModel> taskList;
    public JSONObject todoListJSON;

    private ProgressDialog loader;

    static public TextView temp;

    private FloatingActionButton add_btn;
    private Button leave_btn;

    // THREAD
    private TodoListActivity.TodoListThread todoListThread;

    // SOCKET
    public Socket socket;
    public String name;
    public String ip;
    public int port;
    // SOCKET IO
    private  BufferedReader read;
    private  DataOutputStream write;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_todo_list);



        init_setting();
        init_callback();
        init_socket();

//        taskList.add(newTask(1,0,"Test1"));
//        taskList.add(newTask(1,0,"Test2"));
//        taskList.add(newTask(1,0,"Test3"));
//        updateToDoList();


    }

    private void init_setting(){
        taskRecyclerView = findViewById(R.id.tasksRecyclerView);
        taskRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        tasksAdapter = new ToDoAdapter(this);
        taskRecyclerView.setAdapter(tasksAdapter);

        loader = new ProgressDialog(this);

        temp = findViewById(R.id.temp);

        add_btn = findViewById(R.id.fab);
        leave_btn = findViewById(R.id.leave_btn);

        ItemTouchHelper itemTouchHelper = new ItemTouchHelper(new RecyclerItemTouchHelper(tasksAdapter));
        itemTouchHelper.attachToRecyclerView(taskRecyclerView);

        taskList = new ArrayList<>();

        updateToDoList();

    }
    private void init_callback(){
        add_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                System.out.println("Press add btn");
                AddNewTask.newInstance().show(getSupportFragmentManager(), AddNewTask.TAG);
            }
        });

        leave_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                disconnect();
            }
        });

        temp.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                System.out.println("beforeTextChanged");
                System.out.println(temp.getText().toString());
            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                String str = temp.getText().toString();
                if (!str.equals("")) {
                    System.out.println("here");
                    System.out.println(str);

                    if (str.substring(0,3).equals("add")) {
                        String[] splitStr = str.split("\\s+");
                        sendJSON(
                                "client","Phone",
                                "task", "phone requests for adding new todo",
                                "data", splitStr[1]
                        );
                        temp.setText("");
                    }
                    else if(str.substring(0,3).equals("del")) {

                        String[] splitStr = str.split("\\s+");
                        sendJSON(
                                "client","Phone",
                                "task", "phone requests for deleting todo at index i",
                                "index", splitStr[1]
                        );
                        temp.setText("");
                    }
                    else if(str.substring(0,3).equals("edi")) {
                        String[] splitStr = str.split("\\s+");
                        sendJSON(
                                "client","Phone",
                                "task", "phone requests for editing todo of id i",
                                "id", splitStr[1],
                                "data", splitStr[2]
                        );
                        temp.setText("");
                    }
                    else if(str.substring(0,3).equals("cha")) {
                        String[] splitStr = str.split("\\s+");
                        sendJSON(
                                "client","Phone",
                                "task", "phone requests for changing status of id i",
                                "id", splitStr[1],
                                "status", splitStr[2]
                        );
                        temp.setText("");
                    }

                    temp.setText("");
                }
            }

        });
    }

    private void init_socket(){
        Intent it = this.getIntent();
        if (it != null) {
            Bundle bundle = it.getExtras();
            if (bundle != null) {
                name = bundle.getString("name");
                ip = bundle.getString("ip");
                port = Integer.parseInt(bundle.getString("port"));
            }
        }

        todoListThread = new TodoListActivity.TodoListThread();
        todoListThread.start();
    }

    private void updateToDoList() {tasksAdapter.setTasks(taskList);}

    private void showLoader(String msg){
        loader.setMessage(msg);
        loader.setCanceledOnTouchOutside(false);
        loader.show();
    }
    private void dismissLoader(){
        loader.dismiss();
    }

    private ToDoModel newTask(int id, int status, String todo){
        ToDoModel tmp = new ToDoModel();
        tmp.setId(id); tmp.setStatus(status); tmp.setTask(todo);
        return tmp;
    }


    @Override
    public void handleDialogClose(DialogInterface dialog){
        tasksAdapter.setTasks(taskList);
        tasksAdapter.notifyDataSetChanged();
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


    private void connect(List<String> keys, List<String> values){
        TodoListActivity.Connect connect = new TodoListActivity.Connect(keys,values);
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


    class TodoListThread extends Thread {
        String input;
        String output;

        @Override
        public void run() {
            try{
                runOnUiThread(() -> {});

                socket = new Socket(ip, port);
                read = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                write = new DataOutputStream(socket.getOutputStream());

                sendJSON("client", "Phone");

                runOnUiThread(()->{showLoader("connecting...");});

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                sendJSON(
                        "client", "Phone",
                        "task", "phone requests for todoList"
                );

                runOnUiThread(()->{dismissLoader();});


                while ((input = read.readLine())!=null) {
                    System.out.println("Received Data");
                    System.out.println(input);

                    JSONArray todoListJSONArray = new JSONArray((input));
                    System.out.println(todoListJSONArray);
                    System.out.println(todoListJSONArray.length());

                    taskList.clear();
                    for (int i = 0 ; i < todoListJSONArray.length() ; i ++){
                        JSONObject datai = todoListJSONArray.getJSONObject(i);
                        ToDoModel tempTask = newTask(datai.getInt("id"),datai.getInt("status"),datai.getString("task"));
                        System.out.println(datai);
                        taskList.add(tempTask);
                    }
                    runOnUiThread(()->{updateToDoList();});

                }

                finish();
            }
            catch(IOException | JSONException e){
                e.printStackTrace();
            }
        }

    }


    class Connect extends Thread{
        List<Pair<String,String>> l;
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

}