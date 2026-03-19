package com.example.game;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;
import android.view.MotionEvent; // esto es para que el usuario pueda tocar la pantalla

public class VistaPropia extends View {

    int posX = 550; //alto
    int posY = 300; // ancho
    int radio = 100;

    // ------------ esto lo dejo por si lo aprovecho para el movimiento de las naves enemigas
    int velocidadX = 0; //velocidad lateral
    int velocidadY = 0; // velocidad vertical

    int puntuacion = 0;
    // - Enemigo - //
    int enemigoX = 550;
    int enemigoY = 1000;
    int enemigoRadio = 100;

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

        // - circulo - //
        pincel.setARGB(255, 0, 0, 0); // Negro
        canvas.drawCircle(posX, posY , radio, pincel); // dibuja circulos drawCircle(centroX, centroY, radio, paint).

        // - enemigo - //
        pincel.setARGB(255, 255, 0, 0); // Rojo
        canvas.drawCircle(enemigoX, enemigoY, enemigoRadio, pincel);

        // - puntuación - // ** Hay que cambiarlo xq el juego va a ser en horizontal
        pincel.setARGB(255, 255, 255, 255); // Blanco
        pincel.setTextSize(80);
        canvas.drawText("Puntos: " + puntuacion , 100, 100, pincel);

        // - distancia entre circulos - //
        int distX = posX - enemigoX;
        int distY = posY - enemigoY;
        double distancia = Math.sqrt(distX * distX + distY * distY); // sqrt es para sacar la raiz cuadrada y despejar la distancia

        if (distancia < radio + enemigoRadio) { // si la distancia entre los 2 es menor al radio que ocupan, se chocan
            puntuacion = puntuacion + 1;

            enemigoX = 550;
            enemigoY = 1100;
        }


        //- movimiento automático-// ** igual se queda para el movimiento de las naves enemigas
        posX = posX + velocidadX; // esto mueve el objeto en pantalla y se repite
        posY = posY + velocidadY;

        // - detector de bordes - //
        // ancho
        if (posX + radio >= ancho || posX - radio <= 0) {
            velocidadX = -velocidadX;
        }
        // alto
        if (posY + radio >= alto || posY - radio <= 0) {
            velocidadY = -velocidadY;
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
                posY = (int) event.getY();

                //repintar al tocar
                invalidate();
                break; // esto es para que ejecute solo el case correcpondiente y no ejecute todos en secuencia
        }
        return true; // tiene que devolver true para que funcione, si no ignora el toque (puede ser util ignorar el toque para implementar según quié mecánicas)
    }


}
