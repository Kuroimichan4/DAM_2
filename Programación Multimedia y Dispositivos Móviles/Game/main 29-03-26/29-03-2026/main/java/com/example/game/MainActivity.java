package com.example.game;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    EditText nombreJugador_MHN;
    Button nivel1_MHN, nivel2_MHN, nivel3_MHN;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        nombreJugador_MHN = findViewById(R.id.nombreJugador_MHN);
        nivel1_MHN = findViewById(R.id.btnNivel1_MHN);
        nivel2_MHN = findViewById(R.id.btnNivel2_MHN);
        nivel3_MHN = findViewById(R.id.btnNivel3_MHN);

        nivel1_MHN.setOnClickListener(v -> abrirJuego(1));
        nivel2_MHN.setOnClickListener(v -> abrirJuego(2));
        nivel3_MHN.setOnClickListener(v -> abrirJuego(3));
    }

    private void abrirJuego(int nivel) {
        String nombre_MHN = nombreJugador_MHN.getText().toString().trim();

        if (nombre_MHN.isEmpty()) {
            nombre_MHN = "Don nadie";
        }

        Intent intent = new Intent(MainActivity.this, GameActivity.class);
        intent.putExtra("nombreJugador", nombre_MHN);
        intent.putExtra("nivelDificultad", nivel);
        startActivity(intent);
    }
}