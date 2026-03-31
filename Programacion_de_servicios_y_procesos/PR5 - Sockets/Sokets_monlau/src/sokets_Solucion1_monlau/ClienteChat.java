/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package sokets_Solucion1_monlau;

import java.io.*;
import java.net.*;
import java.util.Scanner; 

public class ClienteChat {
     public static void main(String[] args) { // Chat básico sin concurrencia

        try {

            Socket socket = new Socket("localhost", 5000);

            BufferedReader entrada = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));

            PrintWriter salida = new PrintWriter(
                    socket.getOutputStream(), true);

            Scanner teclado = new Scanner(System.in);

            while (true) {

                String mensaje = teclado.nextLine();
                salida.println(mensaje);

                String respuesta = entrada.readLine();
                System.out.println(respuesta);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
