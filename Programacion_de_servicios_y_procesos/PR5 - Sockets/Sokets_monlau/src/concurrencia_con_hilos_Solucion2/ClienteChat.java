/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package concurrencia_con_hilos_Solucion2;

/**
 *
 * @author miriamhernav
 */
import java.io.*;
import java.net.*;
import java.util.Scanner;


public class ClienteChat {
     public static void main(String[] args) {

        try (Socket socket_MHN = new Socket("localhost", 5000)) {

            BufferedReader entrada_MHN = new BufferedReader(
                    new InputStreamReader(socket_MHN.getInputStream()));
            PrintWriter salida_MHN = new PrintWriter(
                    socket_MHN.getOutputStream(), true);

            // Hilo que escucha lo que manda el servidor
            new Thread(() -> {
                try {
                    String linea_MHN;
                    while ((linea_MHN = entrada_MHN.readLine()) != null) {
                        System.out.println(linea_MHN);
                    }
                } catch (IOException ignored) {}
            }).start();

            // Enviar mensajes
            Scanner teclado_MHN = new Scanner(System.in);
            while (true) {
                String msg_MHN = teclado_MHN.nextLine();
                salida_MHN.println(msg_MHN);

                if (msg_MHN.equalsIgnoreCase("exit")) {
                    break;
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
