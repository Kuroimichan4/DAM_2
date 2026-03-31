/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sokets_Solucion1_monlau;

import java.io.*;
import java.net.*;

public class ServidorChat_1 {

    public static void main(String[] args) {

        try {

            ServerSocket server_MHN = new ServerSocket(5000); // es como un listener en un puerto específico
            System.out.println("Servidor esperando cliente...");

            Socket cliente_MHN = server_MHN.accept(); 
            // socket es el canal de comunicación 
            // hasta que no se conecta un cliente se queda parado
            System.out.println("Cliente conectado");

            BufferedReader entrada_MHN = new BufferedReader(
                    new InputStreamReader(cliente_MHN.getInputStream()));

            PrintWriter salida = new PrintWriter(
                    cliente_MHN.getOutputStream(), true);

            String mensaje_MHN;

            while ((mensaje_MHN = entrada_MHN.readLine()) != null) {  // readline es bloqueante, si no llega un mensaje se queda ahí parado igual que el accept

                System.out.println("Cliente dice: " + mensaje_MHN);

                salida.println("Servidor recibió: " + mensaje_MHN);
            }

            cliente_MHN.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
