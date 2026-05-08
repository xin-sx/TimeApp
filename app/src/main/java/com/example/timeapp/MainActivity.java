package com.example.timeapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;

public class MainActivity extends Activity {

    private EditText etYear, etMonth, etDay, etHour, etMinute;
    private Button btnModifyYear, btnModifyMonth, btnModifyDay, btnModifyHour, btnModifyMinute, btnSave;
    private MediaPlayer mediaPlayer;

    private static final int REQUEST_PERMISSION = 200;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initViews();
        initListeners();
    }

    private void initViews() {
        etYear = (EditText) findViewById(R.id.etYear);
        etMonth = (EditText) findViewById(R.id.etMonth);
        etDay = (EditText) findViewById(R.id.etDay);
        etHour = (EditText) findViewById(R.id.etHour);
        etMinute = (EditText) findViewById(R.id.etMinute);

        btnModifyYear = (Button) findViewById(R.id.btnModifyYear);
        btnModifyMonth = (Button) findViewById(R.id.btnModifyMonth);
        btnModifyDay = (Button) findViewById(R.id.btnModifyDay);
        btnModifyHour = (Button) findViewById(R.id.btnModifyHour);
        btnModifyMinute = (Button) findViewById(R.id.btnModifyMinute);
        btnSave = (Button) findViewById(R.id.btnSave);
    }

    private void initListeners() {
        btnModifyYear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                playRingtoneAndModify(etYear, "年");
            }
        });

        btnModifyMonth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                playRingtoneAndModify(etMonth, "月");
            }
        });

        btnModifyDay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                playRingtoneAndModify(etDay, "日");
            }
        });

        btnModifyHour.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                playRingtoneAndModify(etHour, "时");
            }
        });

        btnModifyMinute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                playRingtoneAndModify(etMinute, "分");
            }
        });

        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveTimeSettings();
            }
        });
    }

    private void playRingtoneAndModify(final EditText editText, final String label) {
        AudioManager audioManager = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
        int currentVolume = audioManager.getStreamVolume(AudioManager.STREAM_RING);
        
        if (currentVolume == 0) {
            Toast.makeText(this, "请先开启铃声", Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            Uri ringtoneUri = Settings.System.DEFAULT_RINGTONE_URI;
            if (mediaPlayer != null) {
                mediaPlayer.stop();
                mediaPlayer.release();
            }

            mediaPlayer = new MediaPlayer();
            mediaPlayer.setDataSource(this, ringtoneUri);
            mediaPlayer.setAudioStreamType(AudioManager.STREAM_RING);
            mediaPlayer.prepare();
            mediaPlayer.start();

            mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                @Override
                public void onCompletion(MediaPlayer mp) {
                    showModifyDialog(editText, label);
                }
            });

        } catch (IOException e) {
            e.printStackTrace();
            showModifyDialog(editText, label);
        }
    }

    private void showModifyDialog(final EditText editText, final String label) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("修改" + label);
        
        final EditText input = new EditText(this);
        input.setText(editText.getText());
        builder.setView(input);

        builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String value = input.getText().toString();
                if (!value.isEmpty()) {
                    editText.setText(value);
                    Toast.makeText(MainActivity.this, label + "已修改为: " + value, Toast.LENGTH_SHORT).show();
                }
            }
        });

        builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });
        builder.show();
    }

    private void saveTimeSettings() {
        String year = etYear.getText().toString();
        String month = etMonth.getText().toString();
        String day = etDay.getText().toString();
        String hour = etHour.getText().toString();
        String minute = etMinute.getText().toString();

        if (year.isEmpty() || month.isEmpty() || day.isEmpty() || hour.isEmpty() || minute.isEmpty()) {
            Toast.makeText(this, "请填写完整时间", Toast.LENGTH_SHORT).show();
            return;
        }

        String timeStr = year + "年" + month + "月" + day + "日 " + hour + "时" + minute + "分";
        Toast.makeText(this, "时间已保存: " + timeStr, Toast.LENGTH_LONG).show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }
}
