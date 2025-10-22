<?php

namespace MusicianAI\Middleware;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Server\RequestHandlerInterface as RequestHandler;
use MusicianAI\Services\AuthService;

class AuthMiddleware
{
    private AuthService $authService;
    
    public function __construct()
    {
        $this->authService = new AuthService();
    }
    
    public function __invoke(Request $request, RequestHandler $handler): Response
    {
        $authHeader = $request->getHeaderLine('Authorization');
        
        if (empty($authHeader) || !str_starts_with($authHeader, 'Bearer ')) {
            return $this->unauthorizedResponse();
        }
        
        $token = substr($authHeader, 7); // Remove "Bearer "
        
        try {
            $tokenData = $this->authService->validateToken($token);
            
            // Adicionar user_id ao request
            $request = $request->withAttribute('user_id', $tokenData['user_id']);
            
            return $handler->handle($request);
            
        } catch (Exception $e) {
            return $this->unauthorizedResponse();
        }
    }
    
    private function unauthorizedResponse(): Response
    {
        $response = new \Slim\Psr7\Response();
        $response->getBody()->write(json_encode([
            'success' => false,
            'error' => 'Token de acesso inválido ou expirado'
        ]));
        
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus(401);
    }
}

class CorsMiddleware
{
    public function __invoke(Request $request, RequestHandler $handler): Response
    {
        $response = $handler->handle($request);
        
        return $response
            ->withHeader('Access-Control-Allow-Origin', '*')
            ->withHeader('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Origin, Authorization')
            ->withHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    }
}
