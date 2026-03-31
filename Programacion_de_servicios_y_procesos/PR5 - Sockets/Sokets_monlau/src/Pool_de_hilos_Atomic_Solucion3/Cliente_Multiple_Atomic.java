/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Pool_de_hilos_Atomic_Solucion3;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
/**
 *
 * @author Lucifer
 */
public class Cliente_Multiple_Atomic {
    
    private static final int NUM_CLIENTES = 20; // puedes subirlo (50, 100...)

    public static void main(String[] args) {

        for (int i = 0; i < NUM_CLIENTES; i++) {

            int idCliente = i + 1;

            new Thread(() -> {
                try (
                    Socket socket = new Socket("localhost", 5000);
                    BufferedReader entrada = new BufferedReader(
                            new InputStreamReader(socket.getInputStream()));
                    PrintWriter salida = new PrintWriter(
                            socket.getOutputStream(), true)
                ) {

                    // Pedimos ticket
                    salida.println("TICKET");

                    String respuesta = entrada.readLine();

                    System.out.println("Cliente " + idCliente + " -> " + respuesta);

                } catch (Exception e) {
                    System.out.println("Cliente " + idCliente + " -> ERROR DE CONEXIÓN");
                }
            }).start();
        }
    }
}
