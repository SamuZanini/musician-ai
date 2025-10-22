<?php

namespace MusicianAI\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use MusicianAI\Models\User;
use MusicianAI\Services\AuthService;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class AuthController
{
    private AuthService $authService;
    
    public function __construct()
    {
        $this->authService = new AuthService();
    }
    
    public function register(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            // Validação básica
            if (empty($data['name']) || empty($data['email']) || empty($data['password'])) {
                return $this->errorResponse($response, 'Dados obrigatórios não fornecidos', 400);
            }
            
            $result = $this->authService->register($data);
            
            return $this->successResponse($response, $result, 201);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function login(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            if (empty($data['email']) || empty($data['password'])) {
                return $this->errorResponse($response, 'Email e senha são obrigatórios', 400);
            }
            
            $result = $this->authService->login($data['email'], $data['password']);
            
            return $this->successResponse($response, $result);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 401);
        }
    }
    
    public function refresh(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            if (empty($data['refresh_token'])) {
                return $this->errorResponse($response, 'Refresh token é obrigatório', 400);
            }
            
            $result = $this->authService->refreshToken($data['refresh_token']);
            
            return $this->successResponse($response, $result);
            
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 401);
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
