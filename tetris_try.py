#!/usr/bin/python3
'''#!/usr/bin/env/python'''

import pygame
import os
import random
import const
import gamestate

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

def draw_screen(surface, game_state, OPP_level, OPP_score, OPP_lines):
    pygame.draw.rect(surface, (125,125,125), (const.left-5, const.top-5, const.board_w*const.block_size+10, const.board_h*const.block_size+10))
    pygame.draw.rect(surface, (20,20,20), (const.left,const.top,const.board_w*const.block_size, const.board_h*const.block_size))
    
    font = pygame.font.SysFont('Arial', 25)
    smallfont = pygame.font.SysFont('Arial', 15)
    pygame.draw.rect(surface, (125,125,125), (270,45,110,150))
    surface.blit(font.render('Next', True, (255,255,255)), (300,50))
    if game_state.next_piece:
        for i, j in game_state.next_piece[1]:
            pygame.draw.rect(surface, const.color_list[game_state.next_piece[0]], (230+i*const.block_size,100+j*const.block_size, const.block_size, const.block_size))

    pygame.draw.rect(surface, (125,125,125), (270, 200, 110, 125))
    surface.blit(font.render("YOU:", True, (255,255,255)), (300,210))
    surface.blit(smallfont.render("Score: ", True, (255,255,255)), (280, 245))
    surface.blit(smallfont.render(str(game_state.score),True, (255,255,255)),(350, 245))
    surface.blit(smallfont.render("Level: ", True, (255,255,255)), (280, 270))
    surface.blit(smallfont.render(str(game_state.level), True, (255,255,255)), (350,270))
    surface.blit(smallfont.render("Attacks: ", True, (255,255,255)), (280,295))
    surface.blit(smallfont.render(str(game_state.lines), True, (255,255,255)), (350,295))
    pygame.draw.rect(surface, (125,125,125), (270, 330, 110, 125))
    surface.blit(font.render("OPP:", True, (255,255,255)), (300,340))
    surface.blit(smallfont.render("Score: ", True, (255,255,255)), (280, 375))
    surface.blit(smallfont.render(str(OPP_score),True, (255,255,255)),(350, 375))
    surface.blit(smallfont.render("Level: ", True, (255,255,255)), (280, 400))
    surface.blit(smallfont.render(str(OPP_level), True, (255,255,255)), (350,400))
    surface.blit(smallfont.render("Attacks: ", True, (255,255,255)), (280,425))
    surface.blit(smallfont.render(str(OPP_lines), True, (255,255,255)), (350,425))
    
    
    
    
    for i in range( const.board_h):
        for j in range(const.board_w):
            curr = game_state.board[i][j]
            if curr != 0:
                current_color = const.color_list[curr]
                pygame.draw.rect(surface, current_color, (const.left+j*const.block_size, const.top+i*const.block_size, const.block_size,const.block_size))
         
    if game_state.curr_piece:        
        for i,j in game_state.curr_piece[1]:
            curr = game_state.curr_piece[0]
            if curr != 0:
                current_color = const.color_list[curr]
                pygame.draw.rect(surface, current_color, (const.left+i*const.block_size, const.top+j*const.block_size, const.block_size,const.block_size))
 
    pygame.display.flip()
    
def game_over_lost():
    pygame.init()
    surface = pygame.display.set_mode((400,500))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        font = pygame.font.SysFont('Arial', 30)
        smallfont = pygame.font.SysFont('Arial', 20)
        surface.blit(font.render('GAME OVER!', True, (255,255,255)), (100,150))
        pygame.display.flip()
        surface.blit(smallfont.render('Sorry you lost :(', True, (255,255,255)), (120, 300))
            

def game_over_win():
    pygame.init()
    surface = pygame.display.set_mode((400,500))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        font = pygame.font.SysFont('Arial', 30)
        smallfont = pygame.font.SysFont('Arial', 20)
        surface.blit(font.render('CONGRATULATIONS!', True, (255,255,255)), (50,150))
        pygame.display.flip()
        surface.blit(smallfont.render('You won! :D', True, (255,255,255)), (150, 300))
            
def rage_quit():
    pygame.init()
    surface = pygame.display.set_mode((400,500))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        font = pygame.font.SysFont('Arial', 30)
        smallfont = pygame.font.SysFont('Arial', 20)
        surface.blit(font.render('GAME OVER!', True, (255,255,255)), (100,150))
        pygame.display.flip()
        surface.blit(smallfont.render('Why did you quit? :C', True, (255,255,255)), (100, 300))
            

def run_game():
    pygame.init()
    surface = pygame.display.set_mode((400,500))
    running = True
    clock = pygame.time.Clock()
    game_state = gamestate.GameState()
    game_over = False
    downclock = 0
    game_win = False
    while running and not game_over and not game_win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_c and game_state.curr_piece:
                    game_state.rotate_cw()
                if event.key == pygame.K_q: 
                    running = False
                if event.key == pygame.K_SPACE:
                    #Needs to set packet to send new row
                    None
        if game_state.curr_piece == None:
            game_state.make_piece()
        #need to check packet if a row was sent, then call game.state.create_incomplete_row() 
        game_state.checkRow()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]: game_state.moveRight();
        if pressed[pygame.K_LEFT]: game_state.moveLeft();
        if pressed[pygame.K_DOWN]: game_state.moveDown();
        
        if(downclock%10==0): 
            if game_state.curr_piece:
                game_state.moveDown()
        
        game_over= game_state.check_game_over()

        OPP_score = 0
        OPP_level = 0
        OPP_lines = 0
        OPP_alive = True
        game_win = game_state.check_win_condition(OPP_score, OPP_alive)
        draw_screen(surface, game_state,OPP_score, OPP_level,OPP_lines)
        downclock+=1
        clock.tick(50*game_state.level)
    if game_win:
        game_over_win()
    elif game_over:
        game_over_lost()
    elif not running:
        rage_quit()



class PacketConnection(Protocol):
        def __init__(self):
		pygame.init()
		self.surface = pygame.display.set_mode((400,500))
		self.running = True
		self.connection = False
		self.game = False
		self.makeStart()
	def checkConnection(self):
		if self.connection:
			self.surface.blit(smallfont.render('Connected! Press enter to continue', True, (255,255,255)), (50, 300))
			self.pressed = pygame.key.get_pressed()
         	if pressed[pygame.K_RETURN]:
			self.running = False
             		self.game = True
        	else:
            	surface.blit(smallfont.render('Connecting... Please wait', True, (255,255,255)), (100,300))
	def connectionMade(self):
		self.connection = True
	def makeStart(self):
		while self.running:
      		for event in pygame.event.get():
         		if event.type == pygame.QUIT:
	    			self.running=False

      		font = pygame.font.SysFont('Arial', 30)
 			smallfont = pygame.font.SysFont('Arial', 20)
			self.surface.blit(font.render('Tetris', True, (255,255,255)), (165,150))
			pygame.display.flip()
       	    self.checkConnection()
			if self.game:
        		run_game()


class PacketConnectionFactory(Factory):
	def __init__(self):
		self.myconn = PacketConnection()
	def buildProtocol(self, addr):
		return self.myconn

def main():
	reactor.listenTCP(40016, PacketConnectionFactory())
	reactor.run()

if __name__=='__main__':
    main()
    
