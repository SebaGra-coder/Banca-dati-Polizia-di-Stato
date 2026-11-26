<?php
header('Content-Type: application/json; charset=utf-8');

$host = getenv('DB_HOST') ?: 'localhost';
$user = getenv('DB_USER') ?: '';
$pass = getenv('DB_PASSWORD') ?: '';
$db   = getenv('DB_NAME') ?: '';

if ($user === '' || $db === '') {
    http_response_code(500);
    echo json_encode(['error' => 'Database configuration missing']);
    exit;
}

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}
$conn->set_charset('utf8mb4');

$argomento = $_GET['argomento'] ?? 'random';
$limit = filter_input(INPUT_GET, 'limit', FILTER_VALIDATE_INT);
$limit = ($limit !== false && $limit !== null) ? max(1, min(100, $limit)) : 10;

$ranges = [
    'costituzionale' => [1, 1000],
    'penale' => [1001, 3000],
    'processuale' => [3001, 5000]
];
[$minId, $maxId] = $ranges[$argomento] ?? [1, 5000];

$stmt = $conn->prepare('SELECT id, testo FROM domande WHERE id BETWEEN ? AND ? ORDER BY RAND() LIMIT ?');
$stmt->bind_param('iii', $minId, $maxId, $limit);
$stmt->execute();
$result = $stmt->get_result();

$quizData = [];
$answerStmt = $conn->prepare('SELECT id, testo, corretta FROM risposte WHERE domanda_id = ?');
while ($row = $result->fetch_assoc()) {
    $questionId = (int)$row['id'];
    $answerStmt->bind_param('i', $questionId);
    $answerStmt->execute();
    $answersResult = $answerStmt->get_result();
    $answers = [];
    while ($answer = $answersResult->fetch_assoc()) {
        $answers[] = [
            'id' => (int)$answer['id'],
            'testo' => $answer['testo'],
            'corretta' => (int)$answer['corretta']
        ];
    }
    $quizData[] = ['id' => $questionId, 'testo' => $row['testo'], 'risposte' => $answers];
}

echo json_encode($quizData, JSON_UNESCAPED_UNICODE);
$answerStmt->close();
$stmt->close();
$conn->close();
