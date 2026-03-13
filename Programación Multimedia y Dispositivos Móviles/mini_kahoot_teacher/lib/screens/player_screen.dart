import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/firebase_service.dart';

class PlayerScreen extends StatefulWidget {
  const PlayerScreen({super.key});

  @override
  State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> {
  final nameController = TextEditingController();
  final codeController = TextEditingController();

  String? gameId;
  String? playerId;
  String? playerName;
  bool joined = false;
  bool hasAnswered = false;
  int currentQuestionIndex = 0;

  Future<void> joinGame() async {
    

    final name = nameController.text.trim();
    final codeText = codeController.text.trim();

    if (name.isEmpty || codeText.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Completa nombre y código")),
      );
      return;
    }

    final code = int.tryParse(codeText);
    if (code == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("El código debe ser numérico")),
      );
      return;
    }

    final query = await FirebaseFirestore.instance
        .collection('games')
        .where('code', isEqualTo: code)
        .get();

    if (query.docs.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Código no encontrado")),
      );
      return;
    }

// login
    await FirebaseAuth.instance.signInAnonymously();

    gameId = query.docs.first.id;
    playerName = name;

    final playerRef = await FirebaseFirestore.instance
        .collection('games')
        .doc(gameId)
        .collection('players')
        .add({
      'name': name,
      'score': 0,
      'joinedAt': FieldValue.serverTimestamp(),
    });

    playerId = playerRef.id;

    setState(() {
      joined = true;
    });
  }

  @override
  void dispose() {
    nameController.dispose();
    codeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!joined) {
      return Scaffold(
        appBar: AppBar(title: const Text('Jugador')),
        body: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: "Nombre"),
              ),
              TextField(
                controller: codeController,
                decoration: const InputDecoration(labelText: "Código del juego"),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: joinGame,
                child: const Text("Entrar"),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Jugador')),
      body: StreamBuilder<DocumentSnapshot>(
        stream: FirebaseFirestore.instance
            .collection('games')
            .doc(gameId)
            .snapshots(),
        builder: (context, gameSnapshot) {
          if (!gameSnapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final gameData = gameSnapshot.data!.data() as Map<String, dynamic>?;
          if (gameData == null || gameData['status'] != 'playing') {
            return const Center(
              child: Text('Esperando a que el profesor empiece la partida...'),
            );
          }

          final newIndex = gameData['currentQuestion'] ?? 0;
          if (newIndex != currentQuestionIndex) {
            currentQuestionIndex = newIndex;
            hasAnswered = false;
          }

          return StreamBuilder<QuerySnapshot>(
            stream: FirebaseFirestore.instance
                .collection('questions')
                .orderBy('createdAt')
                .snapshots(),
            builder: (context, questionSnapshot) {
              if (!questionSnapshot.hasData) {
                return const Center(child: CircularProgressIndicator());
              }

              final questions = questionSnapshot.data!.docs;

              if (questions.isEmpty) {
                return const Center(child: Text('No hay preguntas disponibles'));
              }

              if (currentQuestionIndex >= questions.length) {
                return const Center(
                  child: Text('La partida ha terminado'),
                );
              }

              final question = questions[currentQuestionIndex].data()
                  as Map<String, dynamic>;

              final List options = question['options'];
              final int correctIndex = question['correctIndex'] ?? 0;

              return Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      question['text'],
                      style: const TextStyle(fontSize: 24),
                    ),
                    const SizedBox(height: 20),
                    ...List.generate(options.length, (index) {
                      final option = options[index].toString();

                      return Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: ElevatedButton(
                          onPressed: hasAnswered
    ? null
    : () async {
        final bool isCorrect = index == correctIndex;

        await FirebaseService().saveAnswer(
          gameId: gameId!,
          playerId: playerId!,
          playerName: playerName!,
          questionIndex: currentQuestionIndex,
          selectedOption: option,
          isCorrect: isCorrect,
        );

        setState(() {
          hasAnswered = true;
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              isCorrect
                  ? '¡Correcto! Has elegido: $option'
                  : 'Incorrecto. Has elegido: $option',
            ),
          ),
        );
      },
                          child: Text(option),
                        ),
                      );
                    }),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}