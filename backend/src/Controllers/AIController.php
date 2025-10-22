<?php

namespace MusicianAI\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

class AIController
{
    private Client $httpClient;
    private string $aiServiceUrl;
    
    public function __construct()
    {
        $this->httpClient = new Client();
        $this->aiServiceUrl = $_ENV['AI_SERVICE_URL'] ?? 'http://localhost:8001';
    }
    
    public function analyzeAudio(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            // Validar dados de entrada
            if (empty($data['audio_file_path']) || empty($data['analysis_type'])) {
                return $this->errorResponse($response, 'Dados obrigatórios não fornecidos', 400);
            }
            
            // Fazer requisição para o serviço de IA
            $aiResponse = $this->httpClient->post($this->aiServiceUrl . '/analyze-audio', [
                'json' => $data,
                'timeout' => 30
            ]);
            
            $result = json_decode($aiResponse->getBody()->getContents(), true);
            
            return $this->successResponse($response, $result);
            
        } catch (RequestException $e) {
            return $this->errorResponse($response, 'Erro na comunicação com serviço de IA: ' . $e->getMessage(), 500);
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function generateMusic(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            // Validar dados de entrada
            if (empty($data['prompt']) || empty($data['style'])) {
                return $this->errorResponse($response, 'Prompt e estilo são obrigatórios', 400);
            }
            
            // Fazer requisição para o serviço de IA
            $aiResponse = $this->httpClient->post($this->aiServiceUrl . '/generate-music', [
                'json' => $data,
                'timeout' => 60 // Geração musical pode demorar mais
            ]);
            
            $result = json_decode($aiResponse->getBody()->getContents(), true);
            
            return $this->successResponse($response, $result);
            
        } catch (RequestException $e) {
            return $this->errorResponse($response, 'Erro na comunicação com serviço de IA: ' . $e->getMessage(), 500);
        } catch (Exception $e) {
            return $this->errorResponse($response, $e->getMessage(), 500);
        }
    }
    
    public function analyzePractice(Request $request, Response $response): Response
    {
        try {
            $data = $request->getParsedBody();
            
            // Validar dados de entrada
            if (empty($data['audio_data']) || empty($data['reference_track']) || empty($data['instrument'])) {
                return $this->errorResponse($response, 'Dados obrigatórios não fornecidos', 400);
            }
            
            // Fazer requisição para o serviço de IA
            $aiResponse = $this->httpClient->post($this->aiServiceUrl . '/analyze-practice', [
                'json' => $data,
                'timeout' => 45
            ]);
            
            $result = json_decode($aiResponse->getBody()->getContents(), true);
            
            return $this->successResponse($response, $result);
            
        } catch (RequestException $e) {
            return $this->errorResponse($response, 'Erro na comunicação com serviço de IA: ' . $e->getMessage(), 500);
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
