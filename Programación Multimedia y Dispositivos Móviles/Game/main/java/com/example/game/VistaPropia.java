package com.example.game;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;
import android.view.MotionEvent; // esto es para que el usuario pueda tocar la pantalla

public class VistaPropia extends View {

    int posX = 550; //alto pero visto de lado
    int posY = 2000; // ancho
    int radio = 100;

    // ------------ esto lo dejo por si lo aprovecho para el movimiento de las naves enemigas
    int velocidadX = 0; //velocidad lateral
    int velocidadY = 12; // velocidad vertical

    int puntuacion = 0;

    // - Enemigos - //
    int enemigoRadio = 100;
    int cantidadEnemigos = 3;
    int[] enemigoX = new int[cantidadEnemigos];
    int[] enemigoY = new int[cantidadEnemigos];
    boolean[] enemigosActivos = new boolean[cantidadEnemigos];
    boolean juegoIniciado = false;
    boolean gameOver = false;

//    int enemigoY = -enemigoRadio;

    //- pincel-//
    Paint pincel = new Paint();



    public VistaPropia(Context context) { // hereda de view y comvierte la clase en un elemento dibujable que puede ocupar toda la pantalla y se tiene control sobre cada pixel
        super(context);
    }
    public VistaPropia(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    protected void onDraw(Canvas canvas) {

        // --- Pintado de pantalla ---//
        // - Fondo - //
        canvas.drawRGB(50, 0, 200);

        // Variables - //
        int ancho = canvas.getWidth(); //ancho de la pantalla para no pintar una línea infinita y se adapta a todas las pantallas
        int alto = canvas.getHeight(); // alto total de la pantalla

        // - Activa enemigos si no hay ninguno activo - //
        if (!juegoIniciado) {

            for (int i = 0; i < cantidadEnemigos; i++) {
                enemigoX[i] = (int) (Math.random() * (ancho - 2 * enemigoRadio)) + enemigoRadio;
                enemigoY[i] = (-200 * i) - (int)(Math.random() * 500); // salen en -200 * el numero del array y se resta el aleatorio * 200 para que salgan escalonados
                enemigosActivos[i] = true;

            }
            juegoIniciado = true;
        }

        // - circulo - //
        pincel.setARGB(255, 0, 0, 0); // Negro
        canvas.drawCircle(posX, posY , radio, pincel); // dibuja circulos drawCircle(centroX, centroY, radio, paint).

        // - enemigo - //
        pincel.setARGB(255, 255, 0, 0); // Rojo

        for (int i = 0; i < cantidadEnemigos; i++) {
            if (enemigosActivos[i]) {
                canvas.drawCircle(enemigoX[i], enemigoY[i], enemigoRadio, pincel);
            }
        }

        // - Posición y movimiento automático Enemigo - //
        for (int i = 0; i < cantidadEnemigos; i++) {
            if (enemigosActivos[i]) {
                enemigoY[i] = enemigoY[i] + velocidadY; // esto mueve el objeto en pantalla y se repite
            }

            // Para hacer un enemigo perseguidor -----------**********
//            if (enemigoX < posX) {
//                enemigoX += 3;
//            } else if (enemigoX > posX) {
//                enemigoX -= 3;
//            }
//
//            enemigoY += velocidadY;

        }

        // - puntuación - // ** Hay que cambiarlo xq el juego va a ser en horizontal
        pincel.setARGB(255, 255, 255, 255); // Blanco
        pincel.setTextSize(80);
        canvas.drawText("Puntos: " + puntuacion , 100, 100, pincel);

        // - Distancia entre enemigo - //
        for (int i = 0; i < cantidadEnemigos; i++) {
            if (enemigosActivos[i]) {
                int distX = posX - enemigoX[i];
                int distY = posY - enemigoY[i];

                // - distancia entre circulos - //
                double distancia = Math.sqrt(distX * distX + distY * distY); // sqrt es para sacar la raiz cuadrada y despejar la distancia

                if (distancia < radio + enemigoRadio) { // si la distancia entre los 2 es menor al radio que ocupan, se chocan
                    gameOver = true;
                }
            }
        }

        // - Respawn -//
        for (int i = 0; i < cantidadEnemigos; i++) {
            if (!enemigosActivos[i]) {
                enemigoX[i] = (int) (Math.random() * (ancho  - 2 * enemigoRadio)) + enemigoRadio;
                enemigoY[i] = (-200 * i) - (int)(Math.random() * 500);
                enemigosActivos[i] = true;
            }
        }

        if (gameOver) {
            canvas.drawRGB(0, 0, 0); // para quitar el juego y pintar un fondo negro
            pincel.setARGB(255, 255, 0, 0); // Rojo
            pincel.setTextSize(120);
            canvas.drawText("GAME OVER", ancho / 2 - 310, alto / 2, pincel);
            return; // para no seguir actualizando la pantalla, solo mostrará el game over
        }

        invalidate(); // esto hace que repinte la pantalla y entre en bucle, repintado y sumando continuamente y no para de moverse
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) { // MotionEvent es para que el usuario pueda tocar la pantalla. Funciona como listener
        // Switch con tipo de toque
        switch (event.getAction()) {

            case MotionEvent.ACTION_DOWN: // Si el usuario toca la pantalla...
            case MotionEvent.ACTION_MOVE: // Si el usuario arrastra el dedo por pantalla......

                // obtenemos la posición del toque
                posX = (int) event.getX();
                //posY = (int) event.getY();

                // - Para que no se salga de la pantalla - //
                if (posX - radio < 0) {
                    posX = radio; // para que la posición no sea negativa y salga de los límites se pone como mínimo el radio de la nave
                }
                if (posX + radio > getWidth()) {
                    posX = getWidth() - radio; // para que no sea myor a la pantalla es igual al tamaño menos el radio
                }
//                if (posY - radio < 0) {
//                    posY = radio;
//                }
//                if (posY + radio > getHeight()) {
//                    posY = getHeight() - radio;
//                }

                //repintar al tocar
                invalidate();
                break; // esto es para que ejecute solo el case correcpondiente y no ejecute todos en secuencia
        }
        return true; // tiene que devolver true para que funcione, si no ignora el toque (puede ser util ignorar el toque para implementar según quié mecánicas)
    }


}
