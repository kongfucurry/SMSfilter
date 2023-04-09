package com.example.smsfilter;


import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class MainActivity extends AppCompatActivity {

    public static final int UPDATE_TEXT=1;
    private TextView tvContent;
    private EditText etContent;
    private static String string;
    private static String goods;
    private static final String TAG="MainActivty";
    private final OkHttpClient mclient=new OkHttpClient();

    @SuppressLint("HandlerLeak")
    private Handler handler=new Handler(Looper.myLooper()){
        @Override
        public void handleMessage(@NonNull Message msg) {
            if(msg.what==UPDATE_TEXT){
                tvContent.setText(string);
            }
            super.handleMessage(msg);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tvContent = findViewById(R.id.tv_content);
        etContent = findViewById(R.id.et_content);
    }

    //执行一个耗时任务
    public void start(View view){
        new Thread (new Runnable(){
            @Override
            public void run(){
                goods = etContent.getText().toString();
                get(goods);
                Message message=new Message();
                message.what=UPDATE_TEXT;
                handler.sendMessage(message);
            }
        }).start();
        Toast.makeText(this,"开启子线程请求网络！",Toast.LENGTH_SHORT).show();
    }

    private void get(String goods) {
        Request.Builder builder = new Request.Builder();
        builder.url("http://192.168.31.95:8080/getrequest");
        Request request = builder.build();

        Log.d(TAG, "run:" + request);

        OkHttpClient client = new OkHttpClient();


        Call call = mclient.newCall(request);

        try {
            Response response = call.execute();
            if (response.isSuccessful()) {
                string = response.body().string();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

