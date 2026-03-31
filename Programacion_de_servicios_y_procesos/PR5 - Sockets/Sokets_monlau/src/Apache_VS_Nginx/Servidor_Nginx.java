/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Apache_VS_Nginx;


import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
/**
 *
 * @author Lucifer
 */
public class Servidor_Nginx {
    
    private static final int PUERTO = 5001;

    public static void main(String[] args) {
        try (
            Selector selector = Selector.open();
            ServerSocketChannel servidor = ServerSocketChannel.open()
        ) {
            servidor.bind(new InetSocketAddress(PUERTO));
            servidor.configureBlocking(false);
            servidor.register(selector, SelectionKey.OP_ACCEPT);

            System.out.println("Servidor estilo nginx en puerto " + PUERTO);

            while (true) {
                selector.select();

                Iterator<SelectionKey> iterador = selector.selectedKeys().iterator();

                while (iterador.hasNext()) {
                    SelectionKey key = iterador.next();
                    iterador.remove();

                    if (key.isAcceptable()) {
                        aceptarConexion(servidor, selector);
                    } else if (key.isReadable()) {
                        leerYResponder(key);
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void aceptarConexion(ServerSocketChannel servidor, Selector selector) throws IOException {
        SocketChannel cliente = servidor.accept();

        if (cliente != null) {
            cliente.configureBlocking(false);
            cliente.register(selector, SelectionKey.OP_READ);
            System.out.println("Nueva conexión nginx: " + cliente.getRemoteAddress());
        }
    }

    private static void leerYResponder(SelectionKey key) {
        SocketChannel cliente = (SocketChannel) key.channel();
        ByteBuffer buffer = ByteBuffer.allocate(1024);

        try {
            int bytesLeidos = cliente.read(buffer);

            if (bytesLeidos == -1) {
                cliente.close();
                return;
            }

            buffer.flip();
            String mensaje = new String(buffer.array(), 0, buffer.limit()).trim();

            System.out.println("Selector atiende a " + cliente.getRemoteAddress() + " -> " + mensaje);

            String respuesta = "Respuesta nginx\n";
            cliente.write(ByteBuffer.wrap(respuesta.getBytes()));

            cliente.close();

        } catch (IOException e) {
            try {
                cliente.close();
            } catch (IOException ignored) {
            }
        }
    }
}
