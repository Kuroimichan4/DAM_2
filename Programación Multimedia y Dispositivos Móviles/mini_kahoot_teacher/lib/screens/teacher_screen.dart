import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../services/firebase_service.dart';
import 'add_question_screen.dart';

class TeacherScreen extends StatefulWidget { // StatefulWidget es un widget que tiene estado mutable, así que cambia en respuesta a eventos o cambios de datos.
  const TeacherScreen({super.key});

  @override
  State<TeacherScreen> createState() => _TeacherScreenState(); // createState es un método que crea el estado mutable. El guion bajo indica que es privada, solo se puede usar dentro de este archivo.
}

class _TeacherScreenState extends State<TeacherScreen> {
  String? gameId;
  int? gameCode;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profesor - Mini Kahoot')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () async {
                final id = await FirebaseService.createGame(); // Crea un nuevo juego en Firebase y devuelve su ID único.

                final doc = await FirebaseFirestore.instance // accede a la colección 'games' en Firestore, obtiene el documento con el ID del juego recién creado y lo almacena en la variable doc.
                    .collection('games')
                    .doc(id)
                    .get();

                setState(() { //avisa que el estado del widget ha cambiado, y se vuelva a construir con la nueva información del juego.
                  gameId = id;
                  gameCode = doc['code'];
                });
              },
              child: const Text('Crear Kahoot'),
            ),
            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const AddQuestionScreen(),
                  ),
                );
              },
              child: const Text('Crear Pregunta'),
            ),
            const SizedBox(height: 20),

            if (gameId != null) ...[
              Text(
                'Código del juego: $gameCode',
                style: const TextStyle(fontSize: 24),
              ),
              const SizedBox(height: 20),

              ElevatedButton(
                onPressed: () async {
                  await FirebaseService.startGame(gameId!);
                },
                child: const Text('Empezar partida'),
              ),
              const SizedBox(height: 20),

              ElevatedButton(
                onPressed: () async {
                  await FirebaseService.nextQuestion(gameId!);
                },
                child: const Text('Siguiente pregunta'),
              ),
              const SizedBox(height: 20),

              const Text(
              'Ranking de alumnos conectados:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

             
              Expanded(
                child: StreamBuilder<QuerySnapshot>( // StreamBuilder construye su contenido según los datos que recibe de un Stream. Se conecta a un Stream de Firestore que devuelve los jugadores conectados al juego.
                // es resultado de una consulta a Firestore que contiene varios documentos. Cada documento es un jugador en este caso. Pero las preguntas también serán documentos 
                  stream: FirebaseService.playersStream(gameId!), // método que devuelve un Stream de jugadores conectados
                  builder: (context, snapshot) {
                    if (!snapshot.hasData) { // snapshot.hasData es una propiedad que indica si el Stream ha recibido datos. Si no ha recibido datos
                      return const CircularProgressIndicator(); // muestra un indicador de carga mientras espera los datos
                    }

                    final docs = snapshot.data!.docs; // snapshot.data es el resultado de la consulta a Firestore, y .docs es la lista de documentos
                    
                    if (docs.isEmpty) {
                      return const Center(
                        child: Text('Ningún alumno conectado aún'),
                      );
                    }

                    return ListView(
                      children: docs.map((doc) {
                        return ListTile(
                          leading: CircleAvatar(
                            child: Text('${docs.indexOf(doc) + 1}'),
                          ),
                          title: Text(doc['name']),
                          subtitle: Text('Puntuación: ${doc['score'] ?? 0}'),
                        );
                      }).toList(),
                    );
                  },
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}