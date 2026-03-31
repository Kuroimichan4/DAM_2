/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Apache_VS_Nginx;

/**
 *
 * el ciliente funciona con los 2
 * 
 */

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Cliente_Multiple_Apache_Nginx {
    
    private static final int NUM_CLIENTES_MHN = 20;
    private static final String HOST_MHN = "localhost";

    // Cambia este puerto según pruebes Apache o nginx
    private static final int PUERTO_MHN = 5001;

    public static void main(String[] args) {

        for (int i = 0; i < NUM_CLIENTES_MHN; i++) {
            int idCliente_MHN = i + 1;

            new Thread(() -> {
                try (
                    Socket socket_MHN = new Socket(HOST_MHN, PUERTO_MHN);
                    BufferedReader entrada_MHN = new BufferedReader(
                            new InputStreamReader(socket_MHN.getInputStream()));
                    PrintWriter salida_MHN = new PrintWriter(
                            socket_MHN.getOutputStream(), true)
                ) {
                    salida_MHN.println("HOLA");
                    String respuesta_MHN = entrada_MHN.readLine();

                    System.out.println("Cliente " + idCliente_MHN + " -> " + respuesta_MHN);

                } catch (Exception e) {
                    System.out.println("Cliente " + idCliente_MHN + " -> ERROR");
                }
            }).start();
        }
    }
}
