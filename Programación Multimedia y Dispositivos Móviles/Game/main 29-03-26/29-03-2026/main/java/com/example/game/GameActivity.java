package com.example.game;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import android.media.MediaPlayer;

public class GameActivity extends AppCompatActivity {

    private MediaPlayer mediaPlayer_MHN;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);

        String nombreJugador = getIntent().getStringExtra("nombreJugador");
        int nivelDificultad = getIntent().getIntExtra("nivelDificultad", 1);

        VistaPropia vistaJuego = findViewById(R.id.vistaJuego);

        // setFocusable sirve para desbloquear señales del ratón y teclado
        vistaJuego.setFocusable(true);
        vistaJuego.setFocusableInTouchMode(true);
        vistaJuego.requestFocus();

        vistaJuego.setNombreJugador(nombreJugador);
        vistaJuego.setNivelDificultad(nivelDificultad);


        // para la reproducción de la música y efectos

//        mediaPlayer_MHN = MediaPlayer.create(this, R.raw.musica_fondo);
//        mediaPlayer_MHN.setLooping(true);
//        mediaPlayer_MHN.start();

    }
//
//    // cortar musica al cerrar pantalla o cambiarla -//
//    @Override
//    protected void onPause() {
//        super.onPause();
//        if (mediaPlayer_MHN != null && mediaPlayer_MHN.isPlaying()) {
//            mediaPlayer_MHN.pause();
//        }
//    }
//
//    @Override
//    protected void onResume() {
//        super.onResume();
//        if (mediaPlayer_MHN != null) {
//            mediaPlayer_MHN.start();
//        }
//    }
//
//    @Override
//    protected void onDestroy() {
//        super.onDestroy();
//        if (mediaPlayer_MHN != null) {
//            mediaPlayer_MHN.release();
//            mediaPlayer_MHN = null;
//        }
//    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        VistaPropia vistaJuego = findViewById(R.id.vistaJuego);
        if (vistaJuego != null) {
            vistaJuego.liberarSonidos();
        }
    }
}