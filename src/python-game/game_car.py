import pygame
from pygame.locals import *
import random
from game_backend import GameBackend
import requests

"""
Execute o arquivo game_backend.py para iniciar o servidor Flask.
Em seguida, execute game_car.py para iniciar o jogo.
A cada desvio bem-sucedido, o jogo comunicará com o backend para registrar o desvio.

"""

class Jogo:
    def __init__(self):
        pygame.init()
        
        # Inicializar o sistema de fontes do pygame
        pygame.font.init()

        # Escolher uma fonte e um tamanho para o texto
        self.font = pygame.font.SysFont(None, 36)
        
        
        self.tamanho = largura, altura = (800, 650)
        
        
        self.largura_estrada = int(largura/1.6)
        self.largura_marcacao = int(largura/80)       
        self.faixa_direita = largura/2 + self.largura_estrada/4
        self.faixa_esquerda = largura/2 - self.largura_estrada/4
        
        
        self.velocidade = 3
        self.tela = pygame.display.set_mode(self.tamanho)
        
        
        pygame.display.set_caption("JOGUINHO DE CORRIDA")
        self.tela.fill((60, 220, 0))
        
        
        self.carro_jogador = CarroJogador('./assets/car.png', self.faixa_direita, altura*0.8)
        self.carro_oponente = CarroOponente('./assets/otherCar.png', self.faixa_esquerda, altura*0.2, self)

    def run_game(self):
        jogo_rodando = True
        contador = 0
        while jogo_rodando:
            contador += 1
            
            print(contador)
            
            if contador == 500:
                self.velocidade += 1
                self.carro_oponente.velocidade = self.velocidade
                contador = 0
            # Inicializar o sistema de fontes do pygame
            pygame.font.init()
    
            # Escolher uma fonte e um tamanho para o texto
            self.font = pygame.font.SysFont(None, 36)
            jogo_rodando = self.manipular_eventos(jogo_rodando)
            self.atualizar_tela()
                
            if self.verificar_colisao():
                print('JOGO ACABOU! VOCÊ PERDEU!')
                self.comunicar_desvio()
                break

        pygame.quit()



    def desenhar_informacoes(self):
        # Renderizar texto para desvios, velocidade e score
        texto_desvios = self.font.render(f'Desvios: {self.carro_jogador.desvios}', True, (255, 255, 255))
        texto_velocidade = self.font.render(f'Velocidade: {self.velocidade}', True, (255, 255, 255))
        texto_score = self.font.render(f'Score: {self.carro_jogador.desvios * self.velocidade}', True, (255, 255, 255))

        # Desenhar texto na tela
        self.tela.blit(texto_desvios, (10, 10))
        self.tela.blit(texto_velocidade, (10, 50))
        self.tela.blit(texto_score, (10, 90))
        
        
    def manipular_eventos(self, jogo_rodando):
        for event in pygame.event.get():
            if event.type == QUIT:
                jogo_rodando = False
            if event.type == KEYDOWN:
                if event.key in [K_a, K_LEFT]:
                    self.carro_jogador.mover_esquerda(self.largura_estrada)
                if event.key in [K_d, K_RIGHT]:
                    self.carro_jogador.mover_direita(self.largura_estrada)
        return jogo_rodando

    def atualizar_tela(self):
        self.tela.fill((60, 220, 0))
        self.desenhar_estrada()
        self.tela.blit(self.carro_jogador.imagem, self.carro_jogador.rect)
        self.carro_oponente.mover()
        self.tela.blit(self.carro_oponente.imagem, self.carro_oponente.rect)
        self.desenhar_informacoes()
        pygame.display.update()

    def desenhar_estrada(self):
        pygame.draw.rect(self.tela, (50,50,50), (self.tamanho[0]/2 - self.largura_estrada/2, 0, self.largura_estrada, self.tamanho[1]))
        pygame.draw.rect(self.tela, (255,240,60), (self.tamanho[0]/2 - self.largura_marcacao/2, 0, self.largura_marcacao, self.tamanho[1]))
        pygame.draw.rect(self.tela, (255,255,255), (self.tamanho[0]/2 - self.largura_estrada/2 + self.largura_marcacao*2, 0, self.largura_marcacao, self.tamanho[1]))

    def verificar_colisao(self):
        return self.carro_jogador.rect.colliderect(self.carro_oponente.rect)
    
    #! Metodos backend
    def comunicar_desvio(self):
        # Aqui, fazemos uma requisição POST para o backend para registrar o desvio
        response = requests.post('http://127.0.0.1:5000/registrar_desvio')
        if response.json().get('success'):
            print("Desvio registrado com sucesso!")
        else:
            print("Erro ao registrar desvio.")

    def atualizar_velocidade_backend(self):
        # Aqui, enviamos a velocidade atual para o backend
        response = requests.post(f'http://127.0.0.1:5000/atualizar_velocidade/{self.velocidade}')
        if response.json().get('success'):
            print("Velocidade atualizada com sucesso no backend!")
        else:
            print("Erro ao atualizar velocidade.")


class Carro:
    def __init__(self, caminho_imagem, x, y):
        self.desvios = 0
        self.imagem = pygame.image.load(caminho_imagem)
        self.rect = self.imagem.get_rect()
        self.rect.center = x, y

class CarroJogador(Carro):
    def mover_esquerda(self, largura_estrada):
        self.rect.move_ip(-int(largura_estrada/2), 0)

    def mover_direita(self, largura_estrada):
        self.rect.move_ip(int(largura_estrada/2), 0)

class CarroOponente(Carro):
    def __init__(self, caminho_imagem, x, y, jogo):
        super().__init__(caminho_imagem, x, y)
        self.velocidade = jogo.velocidade
        self.jogo = jogo

    def mover(self):
        self.rect.move_ip(0, self.velocidade)
        if self.rect.top > self.jogo.tamanho[1]:
            if random.randint(0, 1) == 0:
                self.rect.center = self.jogo.faixa_direita, -200
            else:
                self.rect.center = self.jogo.faixa_esquerda, -200

if __name__ == "__main__":
    jogo = Jogo()
    jogo.run_game()
