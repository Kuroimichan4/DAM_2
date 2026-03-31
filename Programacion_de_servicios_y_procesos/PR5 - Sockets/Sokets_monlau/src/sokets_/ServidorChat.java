/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package sokets_;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 *
 * @author miriamhernav
 */
public class ServidorChat {

    static Socket cliente1;
    static Socket cliente2;
    
    
    
 public static void main(String[] args) {
        try {

            ServerSocket server = new ServerSocket(5000);
            System.out.println("Servidor esperando clientes...");

            cliente1 = server.accept();
            System.out.println("Cliente 1 conectado");

            cliente2 = server.accept();
            System.out.println("Cliente 2 conectado");

            new Thread(() -> manejarCliente(cliente1, cliente2, "Cliente1")).start();
            new Thread(() -> manejarCliente(cliente2, cliente1, "Cliente2")).start();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void manejarCliente(Socket origen, Socket destino, String nombre) {

        try {

            BufferedReader entrada = new BufferedReader( // crea un canal para recibir tesxo ya TCP manda bytes
                    new InputStreamReader(origen.getInputStream())); // convierte los bytes en carácteres

            PrintWriter salida = new PrintWriter( // canal para enviar datos al cliente
                    destino.getOutputStream(), true);  // el true lo que hace es que se manden inmediatamente los datos

            String mensaje;

            while ((mensaje = entrada.readLine()) != null) {

                System.out.println(nombre + ": " + mensaje);

                salida.println(nombre + " dice: " + mensaje);
            }

        } catch (Exception e) {
            System.out.println("Cliente desconectado");
        }
    }
}
