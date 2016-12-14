import pygame
import  sys
name = "/Users/mutouyuuya/UTLecture/mechatroPy3.5/ufo.mp3"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(name)
pygame.mixer.music.play()
pygame.event.wait()
pygame.mixer.music.stop()
pygame.mixer.quit()
sys.exit()