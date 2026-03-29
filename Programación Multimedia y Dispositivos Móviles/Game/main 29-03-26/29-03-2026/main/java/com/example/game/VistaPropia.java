package com.example.game;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.util.AttributeSet;
import android.view.KeyEvent;
import android.view.View;
import android.view.MotionEvent; // esto es para que el usuario pueda tocar la pantalla
import android.media.MediaPlayer; // para los efectos en este caso también sirve el media player
import android.media.AudioAttributes; // para los efectos
import android.media.SoundPool; // para los efectos consume menos que mediaplayer

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Rect;

import android.graphics.Matrix; // para rotar los bitmaps

import androidx.core.content.res.ResourcesCompat;

public class VistaPropia extends View {

    // - Jugador - //
    String nombreJugador_MHN = "Jugador";
    int nivelDificultad_MHN;

    int posX_MHN = 0; //alto pero visto de lado
    int posY_MHN = 0; // ancho
    int radio_MHN = 80;
    int radioColision_MHN = 60;


    int puntuacion_MHN = 0;
    // - balas jugador - //
    int balaX_MHN = 0;
    int balaY_MHN = 0;
    int balaRadio_MHN = 15;
    int velocidadBala_MHN = 30;
    boolean balaActiva_MHN = false;

    // - Enemigos - //
    int enemigoRadio_MHN = 80;
    int enemigoRadioColision_MHN = 60;
    int enemigos_MHN = 3;
    int[] enemigoX_MHN = new int[enemigos_MHN];
    int[] enemigoY_MHN = new int[enemigos_MHN];

    final int TIPO_NORMAL_MHN = 0;
    final int TIPO_DISPARADOR_MHN = 1;
    final int TIPO_PERSEGUIDOR_MHN = 2;
    int[] tipoEnemigo_MHN = new int[enemigos_MHN];

    // -- Velocidad enemigos -- //
    int velocidadX_MHN = 12; //velocidad lateral
    int velocidadY_MHN = 0; // velocidad vertical
    boolean[] enemigosActivos_MHN = new boolean[enemigos_MHN];
    boolean juegoIniciado_MHN = false;
    boolean gameOver_MHN = false;

    // - Balas enemigas - //
    int balaEnemigoX_MHN = 0;
    int balaEnemigoY_MHN = 0;
    int balaEnemigoRadio_MHN = 25;
    int velocidadBalaEnemigo_MHN = 30;
    boolean balaEnemigoActiva_MHN = false;


    //- pincel-//
    Paint pincel_MHN = new Paint();

    // - Temporizador - //
    long tiempoInicio_MHN = 0;
    int aumentoVelocidad_MHN = 0;

    // - Efectos sonido - //
    SoundPool soundPool_MHN;
    int sonidoExplosion_MHN;
    int sonidoDisparo_MHN;

    // - Efectos sonido Enemigo- //
    int sonidoExplosionEnemigo_MHN;
    int sonidoDisparoEnemigo_MHN;

    // - Imágenes Jugador - //
    Bitmap naveJugadorBitmap_MHN;
    Bitmap naveJugadorRotada_MHN;
    Bitmap balaJugadorBitmap_MHN;

    // - Imagenes Enemigo - //
    Bitmap naveEnemigaNormalBitmap_MHN;
    Bitmap naveEnemigaNormalRotada_MHN;

    Bitmap naveEnemigaDisparadoraBitmap_MHN;
    Bitmap naveEnemigaDisparadoraRotada_MHN;

    Bitmap naveEnemigaPerseguidoraBitmap_MHN;
    Bitmap naveEnemigaPerseguidoraRotada_MHN;

    Bitmap balaEnemigaBitmap_MHN;


    // - Botones Reinicio - //
    Rect btnReiniciar_MHN;
    Rect btnMenu_MHN;

    // - Fuentes - //
    Typeface fuenteGameOver_MHN;
    Typeface fuenteHUD_MHN;
    Typeface fuenteBotones_MHN;




    boolean sonidoGameOver_MHN = false;

    //- Fondo estrellado -//
    int numEstrellas_MHN = 60;
    int[] estrellasX_MHN = new int[numEstrellas_MHN];
    int[] estrellasY_MHN = new int[numEstrellas_MHN];
    boolean estrellasInicializadas_MHN = false;



    public VistaPropia(Context context) { // hereda de view y convierte la clase en un elemento dibujable que puede ocupar toda la pantalla y se tiene control sobre cada pixel
        super(context);
        init(context);
    }
    public VistaPropia(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }
    private void init(Context context) {
        inicializarEfectos_MHN(context);
        inicializarImagenes_MHN(context);

        fuenteGameOver_MHN = ResourcesCompat.getFont(getContext(), R.font.pixel);
        fuenteHUD_MHN = ResourcesCompat.getFont(getContext(), R.font.partida);
        fuenteBotones_MHN = ResourcesCompat.getFont(getContext(), R.font.partida);
        pincel_MHN.setTypeface(fuenteGameOver_MHN);
        pincel_MHN.setTypeface(fuenteHUD_MHN);
        pincel_MHN.setTypeface(fuenteBotones_MHN);
        pincel_MHN.setShadowLayer(10, 5, 5, Color.BLACK); // Sombra para que se lea mejor sobre el fondo

        // setFocusable sirve para desbloquear señales del ratón y teclado
        setFocusable(true);
        setFocusableInTouchMode(true);
        requestFocus();
    }

    public void setNombreJugador(String nombre) {
        this.nombreJugador_MHN = nombre;
    }

    public void setNivelDificultad(int nivel) {
        this.nivelDificultad_MHN = nivel;

        if (nivel == 1) {
            enemigos_MHN = 3;
        } else if (nivel == 2) {
            enemigos_MHN = 5;
        } else if (nivel == 3) {
            enemigos_MHN = 3;
        }

        enemigoX_MHN = new int[enemigos_MHN];
        enemigoY_MHN = new int[enemigos_MHN];
        enemigosActivos_MHN = new boolean[enemigos_MHN];
       // enemigosPerseguidores_MHN = new boolean[enemigos_MHN];
        tipoEnemigo_MHN = new int[enemigos_MHN];

    }

    @Override
    protected void onDraw(Canvas canvas) {

        // Variables ancho y alto- //
        int ancho = canvas.getWidth(); //ancho de la pantalla para no pintar una línea infinita y se adapta a todas las pantallas
        int alto = canvas.getHeight(); // alto total de la pantalla

        // --- Pintado de pantalla ---//
        // - Fondo - //
        canvas.drawRGB(10, 10, 30);

        // - aleatoriedad estrellas - //
        if (!estrellasInicializadas_MHN) {
            for (int i = 0; i < numEstrellas_MHN; i++) {
                estrellasX_MHN[i] = (int) (Math.random() * ancho);
                estrellasY_MHN[i] = (int) (Math.random() * alto);
            }
            estrellasInicializadas_MHN = true;
        }
        // - Movimiento estrellas - //

        for (int i = 0; i < numEstrellas_MHN; i++) {
            estrellasX_MHN[i] += 2; // Se mueven despacio a la derecha
            // Si se salen por la derecha, vuelven a aparecer por la izquierda
            if (estrellasX_MHN[i] > ancho) {
                estrellasX_MHN[i] = 0;
            }
        }

        // - estrellas - //
        pincel_MHN.setARGB(255, 255, 255, 255);

        for (int i = 0; i < numEstrellas_MHN; i++) {
            canvas.drawCircle(estrellasX_MHN[i], estrellasY_MHN[i], 3, pincel_MHN);
        }

        // - Activa enemigos si no hay ninguno activo - //
        if (!juegoIniciado_MHN) {

            // - Temporizador - //
            tiempoInicio_MHN = System.currentTimeMillis();

            // - Posición inicial del Jugador - //
            posX_MHN = ancho - (radio_MHN * 2);
            posY_MHN = alto / 2;

            // - Posición inicial de los enemigos - //
            for (int i = 0; i < enemigos_MHN; i++) {
                enemigoX_MHN[i] = (-200 * i) - (int)(Math.random() * 500); // salen en -200 * el numero del array y se resta el aleatorio * 200 para que salgan escalonados
                enemigoY_MHN[i] = (int) (Math.random() * (alto - 2 * enemigoRadio_MHN)) + enemigoRadio_MHN;
                enemigosActivos_MHN[i] = true;


            // - Asignar tipo de enemigo según nivel - //
                if (nivelDificultad_MHN == 1) {
                    tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                } else if (nivelDificultad_MHN == 2) {
                    if (i % 2 == 0) {
                        tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                    } else {
                        tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                    }
                } else if (nivelDificultad_MHN == 3) {
                    if (i == 0) {
                        tipoEnemigo_MHN[i] = TIPO_PERSEGUIDOR_MHN;
                    } else if (i == 1) {
                        tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                    } else {
                        tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                    }
                }
            }
            juegoIniciado_MHN = true;
        }

        // - Cañculo de tiempo transcurrido- //
        long tiempoActual_MHN = System.currentTimeMillis();
        long segundosPasados_MHN = (tiempoActual_MHN - tiempoInicio_MHN) / 1000;

        // - Aumento de velocidad - //
        aumentoVelocidad_MHN = (int)(segundosPasados_MHN / 10) * 3; // cada 15 segundos subirá 3 puntos la velocidad
        //- limitador velocidad -//
        if (aumentoVelocidad_MHN > 10) {
            aumentoVelocidad_MHN = 10;
        }

        // - circulo Jugador - //
        //pincel_MHN.setARGB(255, 0, 0, 0); // Negro
        //canvas.drawCircle(posX_MHN, posY_MHN , radio_MHN, pincel_MHN); // dibuja circulos drawCircle(centroX, centroY, radio, paint).
        // - Nave del jugador - //
        Rect rectJugador_MHN = new Rect(
                posX_MHN - radio_MHN,
                posY_MHN - radio_MHN,
                posX_MHN + radio_MHN,
                posY_MHN + radio_MHN
        );
        canvas.drawBitmap(naveJugadorRotada_MHN, null, rectJugador_MHN, null);

//        // - enemigo - //
//        pincel_MHN.setARGB(255, 255, 0, 0); // Rojo
//
//        for (int i = 0; i < enemigos_MHN; i++) {
//            if (enemigosActivos_MHN[i]) {
//                canvas.drawCircle(enemigoX_MHN[i], enemigoY_MHN[i], enemigoRadio_MHN, pincel_MHN);
//            }
//        }
        // - Enemigos con imagen - //
        for (int i = 0; i < enemigos_MHN; i++) {
            if (enemigosActivos_MHN[i]) {
                Rect rectEnemigo_MHN = new Rect(
                        enemigoX_MHN[i] - enemigoRadio_MHN,
                        enemigoY_MHN[i] - enemigoRadio_MHN,
                        enemigoX_MHN[i] + enemigoRadio_MHN,
                        enemigoY_MHN[i] + enemigoRadio_MHN
                );
                Bitmap bitmapEnemigoActual_MHN;

                if (tipoEnemigo_MHN[i] == TIPO_NORMAL_MHN) {
                    bitmapEnemigoActual_MHN = naveEnemigaNormalRotada_MHN;
                } else if (tipoEnemigo_MHN[i] == TIPO_DISPARADOR_MHN) {
                    bitmapEnemigoActual_MHN = naveEnemigaDisparadoraRotada_MHN;
                } else {
                    bitmapEnemigoActual_MHN = naveEnemigaPerseguidoraRotada_MHN;
                }

                canvas.drawBitmap(bitmapEnemigoActual_MHN, null, rectEnemigo_MHN, null);
            }
        }

        // - Posición y movimiento automático Enemigo - //
        for (int i = 0; i < enemigos_MHN; i++) {
            if (enemigosActivos_MHN[i]) {

                // - Movimiento horizontal normal - //
                enemigoX_MHN[i] = enemigoX_MHN[i] + velocidadX_MHN + aumentoVelocidad_MHN; // esto mueve el objeto en pantalla y se repite

                // - Movimiento nivel 3 - //
                if (tipoEnemigo_MHN[i] == TIPO_PERSEGUIDOR_MHN) {
                    int velocidadPersecicion_MHN = 4;

                    if (enemigoY_MHN[i] < posY_MHN) {
                        enemigoY_MHN[i] += velocidadPersecicion_MHN;
                    } else if (enemigoY_MHN[i] > posY_MHN) {
                        enemigoY_MHN[i] -= velocidadPersecicion_MHN;
                    }

                    // - limitar el rango de movimiento - //
                    if (enemigoY_MHN[i] - enemigoRadio_MHN < 0) {
                        enemigoY_MHN[i] = enemigoRadio_MHN;
                    }
                    if (enemigoY_MHN[i] + enemigoRadio_MHN > alto) {
                        enemigoY_MHN[i] = alto - enemigoRadio_MHN;
                    }
                }
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

        // - Disparos en niveles 2 y 3 - //
        if ((nivelDificultad_MHN == 2 || nivelDificultad_MHN == 3) && !balaEnemigoActiva_MHN) {
            int probabilidadDisparo_MHN = (int)(Math.random() * 100); // número aleatorio entre 0 y 99

            if (probabilidadDisparo_MHN < 20) { // x% de probabilidad por fotograma pero como se refresca 60 veces por segundo...

                int enemigoAtacante_MHN = -1;
                int intentos_MHN = 0;

                while (intentos_MHN < 20) {
                    int candidato_MHN = (int)(Math.random() * enemigos_MHN);

                    if (enemigosActivos_MHN[candidato_MHN] &&
                            tipoEnemigo_MHN[candidato_MHN] == TIPO_DISPARADOR_MHN) {
                        enemigoAtacante_MHN = candidato_MHN;
                        break;
                    }

                    intentos_MHN++;
                }
                // - Nave disparadora ataca - //
                if (enemigoAtacante_MHN != -1) {
                    // Ponemos la bala donde está el enemigo que hemos encontrado
                    balaEnemigoX_MHN = enemigoX_MHN[enemigoAtacante_MHN] + enemigoRadio_MHN;
                    balaEnemigoY_MHN = enemigoY_MHN[enemigoAtacante_MHN];
                    balaEnemigoActiva_MHN = true;

                    reproducirSonido_MHN(sonidoDisparoEnemigo_MHN);
                }
            }
        }

        // - Bala - //
        if (balaActiva_MHN) {
            pincel_MHN.setARGB(255, 250, 255, 250);
            canvas.drawRect(balaX_MHN - 30, balaY_MHN - 8, balaX_MHN + 30, balaY_MHN + 8, pincel_MHN);

            // - Movimiento bala - //
            balaX_MHN = balaX_MHN - velocidadBala_MHN;
        }

        // - Desactivar bala - //
        if (balaActiva_MHN && balaX_MHN + balaRadio_MHN < 0) {
            balaActiva_MHN = false;
        }

        // - Bala Enemiga - //
        if (balaEnemigoActiva_MHN) {
            pincel_MHN.setARGB(255, 0, 255, 255); // azul
            canvas.drawCircle(balaEnemigoX_MHN , balaEnemigoY_MHN, balaEnemigoRadio_MHN, pincel_MHN);

            // - Movimiento Bala Enemiga - //
            balaEnemigoX_MHN = balaEnemigoX_MHN + velocidadBalaEnemigo_MHN;
        }
        // - Desactivar bala Enemiga - //
        if (balaEnemigoActiva_MHN && balaEnemigoX_MHN - balaEnemigoRadio_MHN > ancho) {
            balaEnemigoActiva_MHN = false;
        }

        // - puntuación - // ** Hay que cambiarlo xq el juego va a ser en horizontal
        pincel_MHN.setARGB(220, 0, 0, 0);
        //canvas.drawRect(20, 20, 550, 190, pincel_MHN);

        // - Nombre jugador -//
        pincel_MHN.setTextAlign(Paint.Align.LEFT);
        pincel_MHN.setTypeface(fuenteHUD_MHN);
        pincel_MHN.setARGB(255, 255, 255, 255);
        pincel_MHN.setTextSize(42);
        canvas.drawText("Piloto: " + nombreJugador_MHN, 40, 70, pincel_MHN);

        // - Nivel y Velocisdas- //
        pincel_MHN.setTextAlign(Paint.Align.CENTER);
        canvas.drawText("Nivel: " + nivelDificultad_MHN, ancho / 2, 70, pincel_MHN);
        canvas.drawText("Velocidad: " + aumentoVelocidad_MHN, ancho /2, 120, pincel_MHN);

        // - Puntuación - //
        pincel_MHN.setTextAlign(Paint.Align.RIGHT);
        canvas.drawText("Puntos: " + puntuacion_MHN, ancho -40, 70, pincel_MHN);


        // - Distancia entre enemigo - //
        for (int i = 0; i < enemigos_MHN; i++) {
            if (enemigosActivos_MHN[i]) {
                int distX = posX_MHN - enemigoX_MHN[i];
                int distY = posY_MHN - enemigoY_MHN[i];

                // - distancia entre circulos - //
                double distancia = Math.sqrt(distX * distX + distY * distY); // sqrt es para sacar la raiz cuadrada y despejar la distancia

                // - Colisiones - //
                if (distancia < radioColision_MHN + enemigoRadioColision_MHN) { // si la distancia entre los 2 es menor al radio que ocupan, se chocan
                    gameOver_MHN = true;
                }

                // - Colisiuón Disparo Jugador - //
                if (balaActiva_MHN) {
                    int distBalaX = balaX_MHN - enemigoX_MHN[i];
                    int distBalaY = balaY_MHN - enemigoY_MHN[i];
                    double distanciaBala = Math.sqrt(distBalaX * distBalaX + distBalaY * distBalaY);

                    if (distanciaBala < balaRadio_MHN + enemigoRadioColision_MHN) {
                        puntuacion_MHN++;
                        balaActiva_MHN = false;

                        // - Sonido explosion - //
                        reproducirSonido_MHN(sonidoExplosionEnemigo_MHN);

                        // - Respawn al matar un enemigo - //
                        enemigoX_MHN[i] = (-200 * i) - (int)(Math.random() * 500);
                        enemigoY_MHN[i] = (int) (Math.random() * (alto  - 2 * enemigoRadio_MHN)) + enemigoRadio_MHN;

                        // - Respawn nivel -//
                        if (nivelDificultad_MHN == 1) {
                            tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                        } else if (nivelDificultad_MHN == 2) {
                            if (i % 2 == 0) {
                                tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                            } else {
                                tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                            }
                        } else if (nivelDificultad_MHN == 3) {
                            if (i == 0) {
                                tipoEnemigo_MHN[i] = TIPO_PERSEGUIDOR_MHN;
                            } else if (i == 1) {
                                tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                            } else {
                                tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                            }
                        }

                    }
                }

                // - Colisión Disparo enemigo - //
                if (balaEnemigoActiva_MHN) {
                    int distBalaEnemigaX_MHN = balaEnemigoX_MHN - posX_MHN;
                    int distBalaEnemigaY_MHN = balaEnemigoY_MHN - posY_MHN;
                    double distanciaBalaEnemiga = Math.sqrt(distBalaEnemigaX_MHN * distBalaEnemigaX_MHN + distBalaEnemigaY_MHN * distBalaEnemigaY_MHN);

                    if (distanciaBalaEnemiga < balaEnemigoRadio_MHN + radioColision_MHN) {
                        gameOver_MHN = true;
                    }
                }

            }
        }

        // - Respawn al salir de la pantalla -//
        for (int i = 0; i < enemigos_MHN; i++) {
            if (enemigosActivos_MHN[i] && enemigoX_MHN[i] - enemigoRadio_MHN > ancho) {
                enemigoX_MHN[i] = (-200 * i) - (int)(Math.random() * 500);
                enemigoY_MHN[i] = (int) (Math.random() * (alto  - 2 * enemigoRadio_MHN)) + enemigoRadio_MHN;

                // - Respawn nivel -//
                if (nivelDificultad_MHN == 1) {
                    tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                } else if (nivelDificultad_MHN == 2) {
                    if (i % 2 == 0) {
                        tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                    } else {
                        tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                    }
                } else if (nivelDificultad_MHN == 3) {
                    if (i == 0) {
                        tipoEnemigo_MHN[i] = TIPO_PERSEGUIDOR_MHN;
                    } else if (i == 1) {
                        tipoEnemigo_MHN[i] = TIPO_DISPARADOR_MHN;
                    } else {
                        tipoEnemigo_MHN[i] = TIPO_NORMAL_MHN;
                    }
                }
            }
        }

        // - Game over - //
        if (gameOver_MHN) {

            // - Sonido game over - //
            if (!sonidoGameOver_MHN) {
                // - sonido Explosión -//
                reproducirSonido_MHN(sonidoExplosion_MHN);
                sonidoGameOver_MHN = true;
            }
            //------ Pantalla GAME OVER ------- //

            //  fondo negro //
            canvas.drawRGB(0, 0, 0);

            // Centrar textos //
            pincel_MHN.setTextAlign(Paint.Align.CENTER);

            // - Título GAME OVER - //
            pincel_MHN.setTypeface(fuenteGameOver_MHN);
            pincel_MHN.setARGB(255, 255, 0, 0); // Rojo
            pincel_MHN.setTextSize(120);
            canvas.drawText("GAME OVER", ancho / 2, alto / 2, pincel_MHN);

            // - Puntaje final - //
            pincel_MHN.setTypeface(fuenteHUD_MHN);
            pincel_MHN.setARGB(255, 255, 255, 255);
            pincel_MHN.setTextSize(50);
            canvas.drawText("Puntuacion: " + puntuacion_MHN, ancho / 2, alto / 2 + 150, pincel_MHN);
            canvas.drawText("Jugador: " + nombreJugador_MHN, ancho / 2, alto / 2 + 200, pincel_MHN);

            // Botón reiniciar - //
            btnReiniciar_MHN = new Rect(ancho / 2 - 340, alto / 2 + 240, ancho / 2 - 40, alto / 2 + 330);
            pincel_MHN.setARGB(255, 50, 150, 50);
            canvas.drawRect(btnReiniciar_MHN, pincel_MHN);

            pincel_MHN.setARGB(255, 255, 255, 255);
            pincel_MHN.setTextSize(40);
            canvas.drawText("REINICIO", btnReiniciar_MHN.centerX(), btnReiniciar_MHN.centerY() + 14, pincel_MHN);

            // - Botón menú - //
            btnMenu_MHN = new Rect(ancho / 2 - 20, alto / 2 + 240, ancho / 2 + 250, alto / 2 + 330);
            pincel_MHN.setARGB(255, 70, 70, 180);
            canvas.drawRect(btnMenu_MHN, pincel_MHN);

            pincel_MHN.setARGB(255, 255, 255, 255);
            pincel_MHN.setTextSize(40);
            canvas.drawText("MENU", btnMenu_MHN.centerX(), btnMenu_MHN.centerY() +14, pincel_MHN);

            return; // para no seguir actualizando la pantalla, solo mostrará el game over
        }

        invalidate(); // esto hace que repinte la pantalla y entre en bucle, repintado y sumando continuamente y no para de moverse
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) { // MotionEvent es para que el usuario pueda tocar la pantalla. Funciona como listener

        // - Para menú GAME OVER - //
        if (gameOver_MHN) {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                int x = (int) event.getX();
                int y = (int) event.getY();

                if (btnReiniciar_MHN != null && btnReiniciar_MHN.contains(x, y)) {
                    reiniciarJuego_MHN();
                    invalidate();
                    return true;
                }

                if (btnMenu_MHN != null && btnMenu_MHN.contains(x, y)) {
                    ((GameActivity) getContext()).finish();
                    return true;
                }
            }
            return true;
        }

        // Switch con tipo de toque
        switch (event.getAction()) {

            case MotionEvent.ACTION_DOWN: // Si el usuario toca la pantalla...
                // obtenemos la posición del toque
                //posX_MHN = (int) event.getX();
                posY_MHN = (int) event.getY();

                // - Para que no se salga de la pantalla - //
                if (posY_MHN - radio_MHN < 0) {
                    posY_MHN = radio_MHN; // para que la posición no sea negativa y salga de los límites se pone como mínimo el radio de la nave
                }
                if (posY_MHN + radio_MHN > getHeight()) {
                    posY_MHN = getHeight() - radio_MHN; // para que no sea myor a la pantalla es igual al tamaño menos el radio
                }

                // - Diparar - //
                if (!balaActiva_MHN) {
                    balaX_MHN = posX_MHN - radio_MHN;
                    balaY_MHN = posY_MHN;
                    balaActiva_MHN = true;

                    // - sonido disparo -//
                    reproducirSonido_MHN(sonidoDisparo_MHN);
                }
                break;

            case MotionEvent.ACTION_MOVE: // Si el usuario arrastra el dedo por pantalla......

                // obtenemos la posición del toque
                //posX_MHN = (int) event.getX();
                posY_MHN = (int) event.getY();

                // - Para que no se salga de la pantalla - //
                if (posY_MHN - radio_MHN < 0) {
                    posY_MHN = radio_MHN; // para que la posición no sea negativa y salga de los límites se pone como mínimo el radio de la nave
                }
                if (posY_MHN + radio_MHN > getHeight()) {
                    posY_MHN = getHeight() - radio_MHN; // para que no sea myor a la pantalla es igual al tamaño menos el radio
                }

//                if (posY - radio < 0) {
//                    posY = radio;
//                }
//                if (posY + radio > getHeight()) {
//                    posY = getHeight() - radio;
//                }

                // - Diparar - //
                if (!balaActiva_MHN) {
                    balaX_MHN = posX_MHN - radio_MHN;
                    balaY_MHN = posY_MHN;
                    balaActiva_MHN = true;

                    // - sonido disparo -//
                    reproducirSonido_MHN(sonidoDisparo_MHN);
                }

                //repintar al tocar
                invalidate();
                break; // esto es para que ejecute solo el case correcpondiente y no ejecute todos en secuencia
        }
        return true; // tiene que devolver true para que funcione, si no ignora el toque (puede ser util ignorar el toque para implementar según quié mecánicas)
    }

    // --- Control Teclado --- //
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        int paso_MHN = 75;

        switch (keyCode) {
            case KeyEvent.KEYCODE_DPAD_UP:
                posY_MHN -= paso_MHN;
                if (posY_MHN - radio_MHN < 0) {
                    posY_MHN = radio_MHN;
                }
                invalidate();
                return true;

            case KeyEvent.KEYCODE_DPAD_DOWN:
                posY_MHN += paso_MHN;
                if (posY_MHN + radio_MHN > getHeight()) {
                    posY_MHN = getHeight() - radio_MHN;
                }
                invalidate();
                return true;

            case KeyEvent.KEYCODE_SPACE:
            case KeyEvent.KEYCODE_ENTER:
                if (!balaActiva_MHN) {
                    balaX_MHN = posX_MHN - radio_MHN;
                    balaY_MHN = posY_MHN;
                    balaActiva_MHN = true;
                    // - sonido disparo -//
                    reproducirSonido_MHN(sonidoDisparo_MHN);

                }

                invalidate();
                return true;
        }

        return super.onKeyDown(keyCode, event);
    }

    private void inicializarEfectos_MHN(Context context) {
        AudioAttributes audioAttributes = new AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_GAME)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build();

        soundPool_MHN = new SoundPool.Builder()
                .setMaxStreams(4)
                .setAudioAttributes(audioAttributes)
                .build();

        sonidoDisparo_MHN = soundPool_MHN.load(context, R.raw.shoot, 1);
        sonidoDisparoEnemigo_MHN = soundPool_MHN.load(context, R.raw.enemy_shoot, 1);
        sonidoExplosion_MHN = soundPool_MHN.load(context, R.raw.explosion, 1);
        sonidoExplosionEnemigo_MHN = soundPool_MHN.load(context, R.raw.enemy_explosion, 1);
    }

    private void reproducirSonido_MHN(int idSonido) {
        if (soundPool_MHN != null) {
            soundPool_MHN.play(idSonido, 1, 1, 1, 0, 1);
        }
    }

    public void liberarSonidos() {
        if (soundPool_MHN != null) {
            soundPool_MHN.release();
            soundPool_MHN = null;
        }
    }

    private void inicializarImagenes_MHN(Context context) {
        naveJugadorBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.nave_jugador);
       // naveEnemigaBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.nave_enemiga);
        //balaJugadorBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.bala_jugador);
        //balaEnemigaBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.bala_enemiga);

        naveJugadorRotada_MHN = rotarBitmap_MHN(naveJugadorBitmap_MHN,-90);
        //naveEnemigaRotada_MHN = rotarBitmap_MHN(naveEnemigaBitmap_MHN,90);

        naveEnemigaNormalBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.normal);
        naveEnemigaDisparadoraBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.disparadora);
        naveEnemigaPerseguidoraBitmap_MHN = BitmapFactory.decodeResource(getResources(), R.drawable.perseguidora);

        naveEnemigaNormalRotada_MHN = rotarBitmap_MHN(naveEnemigaNormalBitmap_MHN, 90);
        naveEnemigaDisparadoraRotada_MHN = rotarBitmap_MHN(naveEnemigaDisparadoraBitmap_MHN, 90);
        naveEnemigaPerseguidoraRotada_MHN = rotarBitmap_MHN(naveEnemigaPerseguidoraBitmap_MHN, 90);
    }
    private Bitmap rotarBitmap_MHN(Bitmap bitmapOriginal, float grados) {
        Matrix matrix = new Matrix();
        matrix.postRotate(grados);

        return Bitmap.createBitmap(
                bitmapOriginal,
                0,
                0,
                bitmapOriginal.getWidth(),
                bitmapOriginal.getHeight(),
                matrix,
                true
        );
    }
    private void reiniciarJuego_MHN() {
        puntuacion_MHN = 0;
        balaActiva_MHN = false;
        balaEnemigoActiva_MHN = false;
        gameOver_MHN = false;
        juegoIniciado_MHN = false;
        sonidoGameOver_MHN = false;
        aumentoVelocidad_MHN = 0;
    }
}

