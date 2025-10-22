<?php

namespace MusicianAI\Services;

use MusicianAI\Models\User;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Exception;

class AuthService
{
    private User $userModel;
    private string $jwtSecret;
    private string $jwtAlgorithm;
    
    public function __construct()
    {
        $this->userModel = new User();
        $this->jwtSecret = $_ENV['JWT_SECRET'] ?? 'your-secret-key';
        $this->jwtAlgorithm = 'HS256';
    }
    
    public function register(array $data): array
    {
        // Verificar se email já existe
        $existingUser = $this->userModel->findByEmail($data['email']);
        if ($existingUser) {
            throw new Exception('Email já está em uso');
        }
        
        // Hash da senha
        $passwordHash = password_hash($data['password'], PASSWORD_DEFAULT);
        
        // Criar usuário
        $userData = [
            'id' => uniqid(),
            'name' => $data['name'],
            'email' => $data['email'],
            'password_hash' => $passwordHash
        ];
        
        $user = $this->userModel->create($userData);
        
        // Gerar tokens
        $tokens = $this->generateTokens($user['id']);
        
        return [
            'user' => $this->sanitizeUser($user),
            'tokens' => $tokens
        ];
    }
    
    public function login(string $email, string $password): array
    {
        $user = $this->userModel->findByEmail($email);
        
        if (!$user || !password_verify($password, $user['password_hash'])) {
            throw new Exception('Credenciais inválidas');
        }
        
        // Gerar tokens
        $tokens = $this->generateTokens($user['id']);
        
        return [
            'user' => $this->sanitizeUser($user),
            'tokens' => $tokens
        ];
    }
    
    public function refreshToken(string $refreshToken): array
    {
        try {
            $decoded = JWT::decode($refreshToken, new Key($this->jwtSecret, $this->jwtAlgorithm));
            
            if ($decoded->type !== 'refresh') {
                throw new Exception('Token inválido');
            }
            
            // Gerar novos tokens
            $tokens = $this->generateTokens($decoded->user_id);
            
            return $tokens;
            
        } catch (Exception $e) {
            throw new Exception('Token de refresh inválido');
        }
    }
    
    public function validateToken(string $token): array
    {
        try {
            $decoded = JWT::decode($token, new Key($this->jwtSecret, $this->jwtAlgorithm));
            
            if ($decoded->type !== 'access') {
                throw new Exception('Token inválido');
            }
            
            return [
                'user_id' => $decoded->user_id,
                'expires_at' => $decoded->exp
            ];
            
        } catch (Exception $e) {
            throw new Exception('Token inválido');
        }
    }
    
    private function generateTokens(string $userId): array
    {
        $now = time();
        
        // Access token (15 minutos)
        $accessPayload = [
            'user_id' => $userId,
            'type' => 'access',
            'iat' => $now,
            'exp' => $now + (15 * 60)
        ];
        
        // Refresh token (7 dias)
        $refreshPayload = [
            'user_id' => $userId,
            'type' => 'refresh',
            'iat' => $now,
            'exp' => $now + (7 * 24 * 60 * 60)
        ];
        
        return [
            'access_token' => JWT::encode($accessPayload, $this->jwtSecret, $this->jwtAlgorithm),
            'refresh_token' => JWT::encode($refreshPayload, $this->jwtSecret, $this->jwtAlgorithm),
            'expires_in' => 15 * 60
        ];
    }
    
    private function sanitizeUser(array $user): array
    {
        unset($user['password_hash']);
        return $user;
    }
}
