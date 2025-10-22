<?php

namespace MusicianAI\Models;

use MusicianAI\Config\Database;

class User
{
    private PDO $db;
    
    public function __construct()
    {
        $this->db = Database::connect();
    }
    
    public function create(array $data): array
    {
        $sql = "INSERT INTO users (id, name, email, password_hash, created_at, updated_at) 
                VALUES (:id, :name, :email, :password_hash, NOW(), NOW())";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'id' => $data['id'],
            'name' => $data['name'],
            'email' => $data['email'],
            'password_hash' => $data['password_hash']
        ]);
        
        return $this->findById($data['id']);
    }
    
    public function findById(string $id): ?array
    {
        $sql = "SELECT * FROM users WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['id' => $id]);
        
        return $stmt->fetch() ?: null;
    }
    
    public function findByEmail(string $email): ?array
    {
        $sql = "SELECT * FROM users WHERE email = :email";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['email' => $email]);
        
        return $stmt->fetch() ?: null;
    }
    
    public function update(string $id, array $data): array
    {
        $fields = [];
        $params = ['id' => $id];
        
        foreach ($data as $key => $value) {
            if ($key !== 'id') {
                $fields[] = "{$key} = :{$key}";
                $params[$key] = $value;
            }
        }
        
        $fields[] = "updated_at = NOW()";
        
        $sql = "UPDATE users SET " . implode(', ', $fields) . " WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        
        return $this->findById($id);
    }
    
    public function delete(string $id): bool
    {
        $sql = "DELETE FROM users WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute(['id' => $id]);
    }
}

class Instrument
{
    private PDO $db;
    
    public function __construct()
    {
        $this->db = Database::connect();
    }
    
    public function create(array $data): array
    {
        $sql = "INSERT INTO instruments (id, name, type, description, created_at, updated_at) 
                VALUES (:id, :name, :type, :description, NOW(), NOW())";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'id' => $data['id'],
            'name' => $data['name'],
            'type' => $data['type'],
            'description' => $data['description']
        ]);
        
        return $this->findById($data['id']);
    }
    
    public function findAll(): array
    {
        $sql = "SELECT * FROM instruments ORDER BY name";
        $stmt = $this->db->prepare($sql);
        $stmt->execute();
        
        return $stmt->fetchAll();
    }
    
    public function findById(string $id): ?array
    {
        $sql = "SELECT * FROM instruments WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['id' => $id]);
        
        return $stmt->fetch() ?: null;
    }
    
    public function update(string $id, array $data): array
    {
        $fields = [];
        $params = ['id' => $id];
        
        foreach ($data as $key => $value) {
            if ($key !== 'id') {
                $fields[] = "{$key} = :{$key}";
                $params[$key] = $value;
            }
        }
        
        $fields[] = "updated_at = NOW()";
        
        $sql = "UPDATE instruments SET " . implode(', ', $fields) . " WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        
        return $this->findById($id);
    }
    
    public function delete(string $id): bool
    {
        $sql = "DELETE FROM instruments WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute(['id' => $id]);
    }
}

class PracticeSession
{
    private PDO $db;
    
    public function __construct()
    {
        $this->db = Database::connect();
    }
    
    public function create(array $data): array
    {
        $sql = "INSERT INTO practice_sessions (id, user_id, instrument_id, duration, notes, created_at, updated_at) 
                VALUES (:id, :user_id, :instrument_id, :duration, :notes, NOW(), NOW())";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'id' => $data['id'],
            'user_id' => $data['user_id'],
            'instrument_id' => $data['instrument_id'],
            'duration' => $data['duration'],
            'notes' => $data['notes']
        ]);
        
        return $this->findById($data['id']);
    }
    
    public function findByUserId(string $userId): array
    {
        $sql = "SELECT ps.*, i.name as instrument_name 
                FROM practice_sessions ps 
                JOIN instruments i ON ps.instrument_id = i.id 
                WHERE ps.user_id = :user_id 
                ORDER BY ps.created_at DESC";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['user_id' => $userId]);
        
        return $stmt->fetchAll();
    }
    
    public function findById(string $id): ?array
    {
        $sql = "SELECT ps.*, i.name as instrument_name 
                FROM practice_sessions ps 
                JOIN instruments i ON ps.instrument_id = i.id 
                WHERE ps.id = :id";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['id' => $id]);
        
        return $stmt->fetch() ?: null;
    }
    
    public function update(string $id, array $data): array
    {
        $fields = [];
        $params = ['id' => $id];
        
        foreach ($data as $key => $value) {
            if ($key !== 'id') {
                $fields[] = "{$key} = :{$key}";
                $params[$key] = $value;
            }
        }
        
        $fields[] = "updated_at = NOW()";
        
        $sql = "UPDATE practice_sessions SET " . implode(', ', $fields) . " WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        
        return $this->findById($id);
    }
    
    public function delete(string $id): bool
    {
        $sql = "DELETE FROM practice_sessions WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute(['id' => $id]);
    }
}

class Subscription
{
    private PDO $db;
    
    public function __construct()
    {
        $this->db = Database::connect();
    }
    
    public function create(array $data): array
    {
        $sql = "INSERT INTO subscriptions (id, user_id, plan_type, status, start_date, end_date, created_at, updated_at) 
                VALUES (:id, :user_id, :plan_type, :status, :start_date, :end_date, NOW(), NOW())";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'id' => $data['id'],
            'user_id' => $data['user_id'],
            'plan_type' => $data['plan_type'],
            'status' => $data['status'],
            'start_date' => $data['start_date'],
            'end_date' => $data['end_date']
        ]);
        
        return $this->findById($data['id']);
    }
    
    public function findByUserId(string $userId): array
    {
        $sql = "SELECT * FROM subscriptions WHERE user_id = :user_id ORDER BY created_at DESC";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['user_id' => $userId]);
        
        return $stmt->fetchAll();
    }
    
    public function findById(string $id): ?array
    {
        $sql = "SELECT * FROM subscriptions WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['id' => $id]);
        
        return $stmt->fetch() ?: null;
    }
    
    public function update(string $id, array $data): array
    {
        $fields = [];
        $params = ['id' => $id];
        
        foreach ($data as $key => $value) {
            if ($key !== 'id') {
                $fields[] = "{$key} = :{$key}";
                $params[$key] = $value;
            }
        }
        
        $fields[] = "updated_at = NOW()";
        
        $sql = "UPDATE subscriptions SET " . implode(', ', $fields) . " WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        
        return $this->findById($id);
    }
    
    public function delete(string $id): bool
    {
        $sql = "DELETE FROM subscriptions WHERE id = :id";
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute(['id' => $id]);
    }
}
