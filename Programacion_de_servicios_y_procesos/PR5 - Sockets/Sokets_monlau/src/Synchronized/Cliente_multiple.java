/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Synchronized;

/**
 *
 * @author Lucifer
 */

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class Cliente_multiple {
    
    private static final int NUM_CLIENTES_MHN = 20; // cambia este número si quieres

    public static void main(String[] args) {

        for (int i = 0; i < NUM_CLIENTES_MHN; i++) {

            int idCliente_MHN = i + 1;

            new Thread(() -> {
                try (
                    Socket socket_MHN = new Socket("localhost", 5000);
                    BufferedReader entrada_MHN = new BufferedReader(
                        new InputStreamReader(socket_MHN.getInputStream()));
                    PrintWriter salida = new PrintWriter(
                        socket_MHN.getOutputStream(), true)
                ) {

                    salida.println("TICKET");

                    String respuesta_MHN = entrada_MHN.readLine();

                    System.out.println("Cliente " + idCliente_MHN + " -> " + respuesta_MHN);

                } catch (Exception e) {
                    System.out.println("Error en cliente " + idCliente_MHN);
                }
            }).start();
        }
    }
}
