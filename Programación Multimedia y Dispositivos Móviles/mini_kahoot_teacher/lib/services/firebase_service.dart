import 'dart:math';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class FirebaseService {
  static final _auth = FirebaseAuth.instance; //
  static final _db = FirebaseFirestore.instance;

  static Future<void> login() async {
    if (_auth.currentUser == null) {
      await _auth.signInAnonymously();
    }
  }

  static Future<int> generateUniqueCode() async { // genera el código de la partida
    int code;
    bool exists;

    do {
      code = Random().nextInt(900000) + 100000;
      final query = await _db
          .collection('games')
          .where('code', isEqualTo: code)
          .where('status', isEqualTo: 'waiting')
          .get();
      exists = query.docs.isNotEmpty;
    } while (exists);

    return code;
  }

  static Future<String> createGame() async {
    await login();
    final code = await generateUniqueCode();

    final doc = await _db.collection('games').add({
      'code': code,
      'status': 'waiting',
      'createdAt': FieldValue.serverTimestamp(), // fecha y hora del servidor para evitar problemas de sincronización entre clientes
    });

    return doc.id;
  }

  static Stream<QuerySnapshot> playersStream(String gameId) {
    return _db
        .collection('games')
        .doc(gameId)
        .collection('players')
        .orderBy('score', descending: true)
        .snapshots();
  }

  // para las questions
  //   static Future<void> addDefaultQuestions(String gameId) async {
  //   final questions = [
  //     {
  //       'text': '¿Capital de Francia?',
  //       'options': ['Madrid', 'París', 'Roma', 'Berlín'],
  //       'correctIndex': 1,
  //     },
  //     {
  //       'text': '¿Cuánto es 2 + 2?',
  //       'options': ['3', '4', '5', '6'],
  //       'correctIndex': 1,
  //     },
  //     {
  //       'text': '¿Qué lenguaje usa Flutter?',
  //       'options': ['Java', 'Kotlin', 'Dart', 'Python'],
  //       'correctIndex': 2,
  //     },
  //   ];

  //   for (final q in questions) {
  //     await _db
  //         .collection('games')
  //         .doc(gameId)
  //         .collection('questions')
  //         .add(q);
  //   }
  // }

  static Future<void> startGame(String gameId) async {
    await _db.collection('games').doc(gameId).update({
      'status': 'playing',
      'currentQuestion': 0,
    });
  }

  static Stream<DocumentSnapshot> gameStream(String gameId) {
    return _db.collection('games').doc(gameId).snapshots();
  }

  static Stream<QuerySnapshot> questionsStream(String gameId) {
    return _db
        .collection('games')
        .doc(gameId)
        .collection('questions')
        .snapshots();
  }
  static Future<void> addQuestionToBank({
        required String text,
        required List<String> options,
        required int correctIndex,
    }) async {
        await _db.collection('questions').add({
            'text': text,
            'options': options,
            'correctIndex': correctIndex,
            'createdAt': FieldValue.serverTimestamp(),
        });
    }

  static Future<void> nextQuestion(String gameId) async {
    final doc = await _db.collection('games').doc(gameId).get();
    final data = doc.data();

    if (data == null) return;

    final current = data['currentQuestion'] ?? 0;

    await _db.collection('games').doc(gameId).update({
        'currentQuestion': current + 1,
    });
  }

  Future<void> saveAnswer({
    required String gameId,
    required String playerId,
    required String playerName,
    required int questionIndex,
    required String selectedOption,
    required bool isCorrect,
  }) async {
    final answerId = '${playerId}_$questionIndex';

    final answerRef = _db
        .collection('games')
        .doc(gameId)
        .collection('answers')
        .doc(answerId);

    final playerRef = _db
        .collection('games')
        .doc(gameId)
        .collection('players')
        .doc(playerId);

    await _db.runTransaction((transaction) async {
      final answerSnap = await transaction.get(answerRef);

      // Si ya respondió esta pregunta, no hacemos nada
      if (answerSnap.exists) {
        return;
      }

      transaction.set(answerRef, {
        'playerId': playerId,
        'playerName': playerName,
        'questionIndex': questionIndex,
        'selectedOption': selectedOption,
        'isCorrect': isCorrect,
        'answeredAt': FieldValue.serverTimestamp(),
      });

      if (isCorrect) {
        transaction.update(playerRef, {
          'score': FieldValue.increment(1),
        });
      }
    });
  }
}