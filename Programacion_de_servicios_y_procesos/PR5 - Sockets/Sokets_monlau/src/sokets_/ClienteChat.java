/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sokets_;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

/**
 *
 * @author miriamhernav
 */
public class ClienteChat {
        public static void main(String[] args) {

        try {

            Socket socket = new Socket("localhost", 5000);

            BufferedReader entrada = new BufferedReader( // crea el canal para recibir datos
                    new InputStreamReader(socket.getInputStream()));

            PrintWriter salida = new PrintWriter( // crea el canal para enviar datos
                    socket.getOutputStream(), true); // true para envío ionstantáneo

            Scanner teclado = new Scanner(System.in);

            // Hilo para recibir mensajes
            new Thread(() -> {

                try {

                    String mensaje;

                    while ((mensaje = entrada.readLine()) != null) {
                        System.out.println(mensaje);
                    }

                } catch (Exception e) {
                    System.out.println("Conexión cerrada");
                }

            }).start();


            // Enviar mensajes
            while (true) {

                String mensaje = teclado.nextLine();
                salida.println(mensaje);

            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
}
