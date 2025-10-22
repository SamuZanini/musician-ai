<?php

use Slim\Factory\AppFactory;
use Slim\Middleware\BodyParsingMiddleware;
use Slim\Middleware\ErrorMiddleware;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use MusicianAI\Config\Database;
use MusicianAI\Middleware\AuthMiddleware;
use MusicianAI\Middleware\CorsMiddleware;
use MusicianAI\Controllers\AuthController;
use MusicianAI\Controllers\UserController;
use MusicianAI\Controllers\InstrumentController;
use MusicianAI\Controllers\PracticeController;
use MusicianAI\Controllers\SubscriptionController;
use MusicianAI\Controllers\AIController;

require_once __DIR__ . '/../vendor/autoload.php';

// Carregar variáveis de ambiente
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

// Criar aplicação Slim
$app = AppFactory::create();

// Middleware de parsing do body
$app->addBodyParsingMiddleware();

// Middleware CORS
$app->add(new CorsMiddleware());

// Middleware de tratamento de erros
$errorMiddleware = $app->addErrorMiddleware(true, true, true);

// Conectar ao banco de dados
try {
    Database::connect();
} catch (Exception $e) {
    error_log("Erro de conexão com banco: " . $e->getMessage());
}

// Rotas públicas
$app->group('/api', function ($group) {
    
    // Autenticação
    $group->post('/auth/register', AuthController::class . ':register');
    $group->post('/auth/login', AuthController::class . ':login');
    $group->post('/auth/refresh', AuthController::class . ':refresh');
    
    // Health check
    $group->get('/health', function (Request $request, Response $response) {
        $response->getBody()->write(json_encode(['status' => 'healthy', 'service' => 'musician-backend']));
        return $response->withHeader('Content-Type', 'application/json');
    });
});

// Rotas protegidas (requerem autenticação)
$app->group('/api', function ($group) {
    
    // Usuários
    $group->get('/user/profile', UserController::class . ':getProfile');
    $group->put('/user/profile', UserController::class . ':updateProfile');
    $group->delete('/user/account', UserController::class . ':deleteAccount');
    
    // Instrumentos
    $group->get('/instruments', InstrumentController::class . ':getInstruments');
    $group->get('/instruments/{id}', InstrumentController::class . ':getInstrument');
    $group->post('/instruments', InstrumentController::class . ':createInstrument');
    $group->put('/instruments/{id}', InstrumentController::class . ':updateInstrument');
    $group->delete('/instruments/{id}', InstrumentController::class . ':deleteInstrument');
    
    // Prática
    $group->get('/practice/sessions', PracticeController::class . ':getSessions');
    $group->post('/practice/sessions', PracticeController::class . ':createSession');
    $group->get('/practice/sessions/{id}', PracticeController::class . ':getSession');
    $group->put('/practice/sessions/{id}', PracticeController::class . ':updateSession');
    $group->delete('/practice/sessions/{id}', PracticeController::class . ':deleteSession');
    
    // Assinaturas
    $group->get('/subscriptions', SubscriptionController::class . ':getSubscriptions');
    $group->post('/subscriptions', SubscriptionController::class . ':createSubscription');
    $group->put('/subscriptions/{id}', SubscriptionController::class . ':updateSubscription');
    $group->delete('/subscriptions/{id}', SubscriptionController::class . ':cancelSubscription');
    
    // Comunicação com IA
    $group->post('/ai/analyze-audio', AIController::class . ':analyzeAudio');
    $group->post('/ai/generate-music', AIController::class . ':generateMusic');
    $group->post('/ai/analyze-practice', AIController::class . ':analyzePractice');
    
})->add(new AuthMiddleware());

// Executar aplicação
$app->run();
