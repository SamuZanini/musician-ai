<?php

namespace MusicianAI\Config;

use PDO;
use PDOException;

class Database
{
    private static ?PDO $connection = null;
    
    public static function connect(): PDO
    {
        if (self::$connection === null) {
            try {
                $host = $_ENV['DB_HOST'] ?? 'localhost';
                $port = $_ENV['DB_PORT'] ?? '3306';
                $dbname = $_ENV['DB_NAME'] ?? 'musician_ai';
                $username = $_ENV['DB_USER'] ?? 'root';
                $password = $_ENV['DB_PASS'] ?? '';
                
                $dsn = "mysql:host={$host};port={$port};dbname={$dbname};charset=utf8mb4";
                
                self::$connection = new PDO($dsn, $username, $password, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::ATTR_EMULATE_PREPARES => false,
                ]);
                
            } catch (PDOException $e) {
                throw new Exception("Erro de conexão com banco de dados: " . $e->getMessage());
            }
        }
        
        return self::$connection;
    }
    
    public static function disconnect(): void
    {
        self::$connection = null;
    }
}
