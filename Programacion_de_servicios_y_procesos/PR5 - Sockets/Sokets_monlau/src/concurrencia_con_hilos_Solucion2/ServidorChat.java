/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package concurrencia_con_hilos_Solucion2;

/**
 * ****************************---------- Crea un hilo por cliente
 * @author miriamhernav
 */

import java.io.*;
import java.net.*;

public class ServidorChat {
     public static void main(String[] args) {

        try (ServerSocket server_MHN = new ServerSocket(5000)) {

            System.out.println("Servidor concurrente (hilos) escuchando en puerto 5000...");

            while (true) {
                Socket cliente_MHN = server_MHN.accept();
                System.out.println("Nuevo cliente conectado: " + cliente_MHN.getInetAddress());

                new Thread(new ClienteHandler(cliente_MHN)).start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Clase que maneja a UN cliente en su propio hilo
    static class ClienteHandler implements Runnable {

        private final Socket cliente_MHN;

        ClienteHandler(Socket cliente) {
            this.cliente_MHN = cliente;
        }

        @Override
        public void run() {
            try (
                BufferedReader entrada_MHN = new BufferedReader(
                        new InputStreamReader(cliente_MHN.getInputStream()));
                PrintWriter salida_MHN = new PrintWriter(
                        cliente_MHN.getOutputStream(), true)
            ) {
                salida_MHN.println("Conectado al servidor. Escribe mensajes (exit para salir).");

                String mensaje_MHN;
                while ((mensaje_MHN = entrada_MHN.readLine()) != null) {

                    if (mensaje_MHN.equalsIgnoreCase("exit")) {
                        salida_MHN.println("Conexión cerrada. ¡Adiós!");
                        break;
                    }

                    System.out.println("[" + cliente_MHN.getInetAddress() + "] " + mensaje_MHN);
                    salida_MHN.println("Servidor recibió: " + mensaje_MHN);
                }

            } catch (IOException e) {
                System.out.println("Cliente desconectado abruptamente.");
            } finally {
                try { cliente_MHN.close(); } catch (IOException ignored) {}
            }
        }
    }
}
