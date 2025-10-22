<?php

namespace MusicianAI\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use MusicianAI\Models\User;
use MusicianAI\Models\Instrument;
use MusicianAI\Models\PracticeSession;
use MusicianAI\Models\Subscription;

class UserController
{
    private User $userModel;
    
    public function __construct()
    {
        $this->userModel = new User();
    }
    
    public function getProfile(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $user = $this->userModel->findById($userId);
            
            if (!$user) {
                return $this->errorResponse($response, 'Usuário não encontrado', 404);
            }
            
            // Remover dados sensíveis
            unset($user['password_hash']);
            
            return $this->successResponse($response, $user);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function updateProfile(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $data = $request->getParsedBody();
            
            // Remover campos que não devem ser atualizados diretamente
            unset($data['id'], $data['password_hash'], $data['created_at']);
            
            $user = $this->userModel->update($userId, $data);
            
            if (!$user) {
                return $this->errorResponse($response, 'Usuário não encontrado', 404);
            }
            
            unset($user['password_hash']);
            
            return $this->successResponse($response, $user);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function deleteAccount(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            
            $success = $this->userModel->delete($userId);
            
            if (!$success) {
                return $this->errorResponse($response, 'Erro ao deletar conta', 500);
            }
            
            return $this->successResponse($response, ['message' => 'Conta deletada com sucesso']);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    private function successResponse(Response $response, array $data, int $statusCode = 200): Response
    {
        $response->getBody()->write(json_encode([
            'success' => true,
            'data' => $data
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
    
    private function errorResponse(Response $response, string $message, int $statusCode = 400): Response
    {
        $response->getBody()->write(json_encode([
            'success' => false,
            'error' => $message
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
}

class InstrumentController
{
    private Instrument $instrumentModel;
    
    public function __construct()
    {
        $this->instrumentModel = new Instrument();
    }
    
    public function getInstruments(Request $request, Response $response): Response
    {
        try {
            $instruments = $this->instrumentModel->findAll();
            
            return $this->successResponse($response, $instruments);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function getInstrument(Request $request, Response $response, array $args): Response
    {
        try {
            $instrument = $this->instrumentModel->findById($args['id']);
            
            if (!$instrument) {
                return $this->errorResponse($response, 'Instrumento não encontrado', 404);
            }
            
            return $this->successResponse($response, $instrument);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function createInstrument(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            $data['id'] = uniqid();
            
            $instrument = $this->instrumentModel->create($data);
            
            return $this->successResponse($response, $instrument, 201);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function updateInstrument(Request $request, Response $response, array $args): Response
    {
        try {
            $data = $request->getParsedBody();
            unset($data['id'], $data['created_at']);
            
            $instrument = $this->instrumentModel->update($args['id'], $data);
            
            if (!$instrument) {
                return $this->errorResponse($response, 'Instrumento não encontrado', 404);
            }
            
            return $this->successResponse($response, $instrument);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function deleteInstrument(Request $request, Response $response, array $args): Response
    {
        try {
            $success = $this->instrumentModel->delete($args['id']);
            
            if (!$success) {
                return $this->errorResponse($response, 'Instrumento não encontrado', 404);
            }
            
            return $this->successResponse($response, ['message' => 'Instrumento deletado com sucesso']);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    private function successResponse(Response $response, array $data, int $statusCode = 200): Response
    {
        $response->getBody()->write(json_encode([
            'success' => true,
            'data' => $data
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
    
    private function errorResponse(Response $response, string $message, int $statusCode = 400): Response
    {
        $response->getBody()->write(json_encode([
            'success' => false,
            'error' => $message
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
}

class PracticeController
{
    private PracticeSession $practiceModel;
    
    public function __construct()
    {
        $this->practiceModel = new PracticeSession();
    }
    
    public function getSessions(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $sessions = $this->practiceModel->findByUserId($userId);
            
            return $this->successResponse($response, $sessions);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function createSession(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $data = $request->getParsedBody();
            
            $data['id'] = uniqid();
            $data['user_id'] = $userId;
            
            $session = $this->practiceModel->create($data);
            
            return $this->successResponse($response, $session, 201);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function getSession(Request $request, Response $response, array $args): Response
    {
        try {
            $session = $this->practiceModel->findById($args['id']);
            
            if (!$session) {
                return $this->errorResponse($response, 'Sessão de prática não encontrada', 404);
            }
            
            return $this->successResponse($response, $session);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function updateSession(Request $request, Response $response, array $args): Response
    {
        try {
            $data = $request->getParsedBody();
            unset($data['id'], $data['user_id'], $data['created_at']);
            
            $session = $this->practiceModel->update($args['id'], $data);
            
            if (!$session) {
                return $this->errorResponse($response, 'Sessão de prática não encontrada', 404);
            }
            
            return $this->successResponse($response, $session);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function deleteSession(Request $request, Response $response, array $args): Response
    {
        try {
            $success = $this->practiceModel->delete($args['id']);
            
            if (!$success) {
                return $this->errorResponse($response, 'Sessão de prática não encontrada', 404);
            }
            
            return $this->successResponse($response, ['message' => 'Sessão deletada com sucesso']);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    private function successResponse(Response $response, array $data, int $statusCode = 200): Response
    {
        $response->getBody()->write(json_encode([
            'success' => true,
            'data' => $data
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
    
    private function errorResponse(Response $response, string $message, int $statusCode = 400): Response
    {
        $response->getBody()->write(json_encode([
            'success' => false,
            'error' => $message
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
}

class SubscriptionController
{
    private Subscription $subscriptionModel;
    
    public function __construct()
    {
        $this->subscriptionModel = new Subscription();
    }
    
    public function getSubscriptions(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $subscriptions = $this->subscriptionModel->findByUserId($userId);
            
            return $this->successResponse($response, $subscriptions);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function createSubscription(Request $request, Response $response): Response
    {
        try {
            $userId = $request->getAttribute('user_id');
            $data = $request->getParsedBody();
            
            $data['id'] = uniqid();
            $data['user_id'] = $userId;
            $data['status'] = 'active';
            
            $subscription = $this->subscriptionModel->create($data);
            
            return $this->successResponse($response, $subscription, 201);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function updateSubscription(Request $request, Response $response, array $args): Response
    {
        try {
            $data = $request->getParsedBody();
            unset($data['id'], $data['user_id'], $data['created_at']);
            
            $subscription = $this->subscriptionModel->update($args['id'], $data);
            
            if (!$subscription) {
                return $this->errorResponse($response, 'Assinatura não encontrada', 404);
            }
            
            return $this->successResponse($response, $subscription);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function cancelSubscription(Request $request, Response $response, array $args): Response
    {
        try {
            $data = ['status' => 'cancelled'];
            $subscription = $this->subscriptionModel->update($args['id'], $data);
            
            if (!$subscription) {
                return $this->errorResponse($response, 'Assinatura não encontrada', 404);
            }
            
            return $this->successResponse($response, ['message' => 'Assinatura cancelada com sucesso']);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    private function successResponse(Response $response, array $data, int $statusCode = 200): Response
    {
        $response->getBody()->write(json_encode([
            'success' => true,
            'data' => $data
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
    
    private function errorResponse(Response $response, string $message, int $statusCode = 400): Response
    {
        $response->getBody()->write(json_encode([
            'success' => false,
            'error' => $message
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus($statusCode);
    }
}
