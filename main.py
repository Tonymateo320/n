
import os
import pygame
import sys
import time
from config import *
from game_objects import Jugador, NPC, Bala, Obstaculo
# En game_objects.py
# from config import DEBUG_MODE, MARRON, ANCHO, ALTO  # Y las demás constantes que necesites
from utils import Boton, generar_obstaculos
from sprite_manager import SpriteManager
from textos import DamegeText

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Counter Strike 2D")
reloj = pygame.time.Clock()



DEBUG_MODE = False

# Verificar y crear estructura de sprites si es necesario
def verificar_estructura_sprites():
    """Verifica si la estructura de directorios para sprites existe, si no, la crea"""
    if not os.path.exists("sprites"):
        print("Directorio 'sprites' no encontrado. Ejecutando preparar_animaciones.py...")
        print("prueba tony mll")
        try:
            import preparar_animaciones
            preparar_animaciones.main()
            print("Estructura de sprites creada correctamente.")
            return True
        except ImportError:
            print("No se pudo importar preparar_animaciones.py")
            return False
    return True

# Inicializar gestor de sprites
sprite_manager = SpriteManager()

# Cargar sprites y animaciones
def cargar_recursos():
    """Carga todos los sprites y animaciones necesarios para el juego"""
    print("Inicializando recursos gráficos...")
    
    # Verificar y crear estructura si es necesario
    if not verificar_estructura_sprites():
        print("¡ADVERTENCIA! No se pudo verificar la estructura de sprites.")
    
    # Cargar sprites individuales
    print("Cargando sprites individuales...")
    if os.path.exists("sprites"):
        sprite_manager.load_all_sprites_from_directory('sprites')
    
    # Cargar todas las animaciones
    print("Cargando animaciones...")
    sprite_manager.load_all_animations()
    
    print("Recursos gráficos inicializados correctamente.")

# Cargar recursos al inicio
cargar_recursos()

# Variables globales
jugador = None
npcs = []
balas = []
obstaculos = []
nivel_actual = 0
max_niveles = 10
estado_juego = "menu"  # menu, jugando, game_over, victoria

# Botones para el menú
boton_iniciar = Boton(ANCHO//2 - 100, ALTO//2 - 50, 200, 50, "Iniciar Juego", VERDE, (0, 200, 0))
boton_salir = Boton(ANCHO//2 - 100, ALTO//2 + 50, 200, 50, "Salir", ROJO, (200, 0, 0))

def iniciar_nivel(nivel):
    global jugador, npcs, balas, obstaculos
    
    jugador = Jugador(ANCHO // 2, ALTO // 2, sprite_manager)
    npcs = []
    balas = []
    
    # Generar obstáculos
    obstaculos = generar_obstaculos(nivel, sprite_manager)
    
    # Configurar NPCs según el nivel
    num_npcs = 3 + nivel * 2
    for _ in range(num_npcs):
        npc = NPC(jugador, obstaculos, sprite_manager)
        if npc.posicion_valida:
            npcs.append(npc)


# Al inicio del archivo, después de las importaciones
DEBUG_MODE = False

def dibujar_debug_info(pantalla, jugador, obstaculos):
    if not DEBUG_MODE:
        return
        
    # Dibujar información de posición del jugador
    fuente = pygame.font.SysFont(None, 24)
    info_jugador = fuente.render(f"Jugador: ({int(jugador.x)}, {int(jugador.y)})", True, (255, 255, 0))
    pantalla.blit(info_jugador, (ANCHO - 220, 10))
    
    # Dibujar rectángulo del jugador
    pygame.draw.rect(pantalla, (0, 255, 255), jugador.rect, 2)
    
    # Dibujar información de obstáculos
    for i, obs in enumerate(obstaculos):
        # Solo mostrar información de obstáculos cercanos al jugador
        distancia = ((jugador.x - obs.rect.x)**2 + (jugador.y - obs.rect.y)**2)**0.5
        if distancia < 200:  # Mostrar solo obstáculos cercanos
            texto = fuente.render(f"#{i}: ({obs.rect.x}, {obs.rect.y})", True, (255, 255, 0))
            pantalla.blit(texto, (obs.rect.x, obs.rect.y - 20))




# En la función dibujar_juego(), al final:
def dibujar_juego():
    # ... (código existente)
    
    # Dibujar información de depuración
    if DEBUG_MODE:
        dibujar_debug_info(pantalla, jugador, obstaculos)


def dibujar_menu():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    titulo = fuente.render("Counter Strike 2D", True, BLANCO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4))
    
    boton_iniciar.dibujar(pantalla)
    boton_salir.dibujar(pantalla)

def dibujar_juego():
    # Dibujar fondo
    pantalla.fill(GRIS)
    
    # Dibujar obstáculos
    for obstaculo in obstaculos:
        obstaculo.dibujar(pantalla)
    
    # Dibujar jugador y NPCs
    jugador.dibujar(pantalla)
    for npc in npcs:
        npc.dibujar(pantalla)
    
    # Dibujar balas
    for bala in balas:
        bala.dibujar(pantalla)
    
    # Mostrar vida y puntuación
    fuente = pygame.font.SysFont(None, 32)
    vida_texto = fuente.render(f"Vida: {jugador.vida}", True, BLANCO)
    puntuacion_texto = fuente.render(f"Puntuación: {jugador.puntuacion}", True, BLANCO)
    nivel_texto = fuente.render(f"Nivel: {nivel_actual + 1}/{max_niveles}", True, BLANCO)
    
    pantalla.blit(vida_texto, (10, 10))
    pantalla.blit(puntuacion_texto, (10, 50))
    pantalla.blit(nivel_texto, (10, 90))


# def mostrar_debug_info(pantalla, jugador, obstaculos):
#     """Muestra información de depuración visual si DEBUG_MODE está activado"""
#     if not DEBUG_MODE:
#         return
    
#     # Fuente para texto de depuración
#     fuente = pygame.font.SysFont(None, 24)
    
#     # Mostrar posición del jugador
#     info_jugador = fuente.render(f"Jugador: ({int(jugador.x)}, {int(jugador.y)})", True, (255, 255, 0))
#     pantalla.blit(info_jugador, (10, 10))
    
#     # Mostrar rectángulo de colisión del jugador
#     pygame.draw.rect(pantalla, (0, 255, 0), jugador.rect, 1)
    
#     # Mostrar rectángulos de colisión de obstáculos cercanos
#     for i, obs in enumerate(obstaculos):
#         # Calcular distancia al jugador
#         dist = ((jugador.x - obs.x)**2 + (jugador.y - obs.y)**2)**0.5
        
#         # Solo mostrar info para obstáculos cercanos
#         if dist < 200:
#             # Resaltar los rectángulos de colisión
#             pygame.draw.rect(pantalla, (255, 0, 0), obs.rect, 1)
            
#             # Mostrar información de posición
#             texto = fuente.render(f"#{i}: ({obs.x}, {obs.y})", True, (255, 255, 0))
#             pantalla.blit(texto, (obs.x, obs.y - 20))

def toggle_debug_mode():
    """Alterna el modo de depuración cuando se presiona F1"""
    global DEBUG_MODE
    DEBUG_MODE = not DEBUG_MODE
    print(f"Modo depuración: {'ACTIVADO' if DEBUG_MODE else 'DESACTIVADO'}")

def mostrar_debug(pantalla, jugador, npcs, obstaculos):
    """Muestra información detallada de depuración"""
    if not DEBUG_MODE:
        return
    
    # Fuente pequeña para texto de depuración
    fuente_debug = pygame.font.SysFont(None, 16)
    
    # Información del jugador
    pos_jugador = f"Jugador: ({int(jugador.x)}, {int(jugador.y)})"
    txt_jugador = fuente_debug.render(pos_jugador, True, (255, 255, 0))
    pantalla.blit(txt_jugador, (10, 130))
    
    # Dibujar rectángulo del jugador
    pygame.draw.rect(pantalla, (0, 255, 0), jugador.rect, 1)
    
    # Mostrar información de NPCs
    for i, npc in enumerate(npcs):
        if npc.posicion_valida:
            info_npc = f"NPC #{i}: ({int(npc.x)}, {int(npc.y)})"
            txt_npc = fuente_debug.render(info_npc, True, (255, 200, 0))
            pantalla.blit(txt_npc, (10, 150 + i*15))
            
            # Mostrar rectángulo del NPC
            pygame.draw.rect(pantalla, (255, 0, 0), npc.rect, 1)
    
    # Mostrar información de obstáculos cercanos
    obstaculos_mostrados = 0
    for i, obs in enumerate(obstaculos):
        # Calcular distancia al jugador
        dist_jugador = ((jugador.x - obs.x)**2 + (jugador.y - obs.y)**2)**0.5
        if dist_jugador < 200:  # Solo mostrar obstáculos cercanos
            info_obs = f"Obs #{i}: ({int(obs.x)}, {int(obs.y)})"
            txt_obs = fuente_debug.render(info_obs, True, (0, 255, 255))
            pantalla.blit(txt_obs, (ANCHO - 150, 10 + obstaculos_mostrados*15))
            obstaculos_mostrados += 1
            
            # Destacar rectángulo de obstáculo
            pygame.draw.rect(pantalla, (255, 0, 255), obs.rect, 1)

# Añadir este código al final de la función dibujar_juego() en main.py:
# if DEBUG_MODE:
#     mostrar_debug_info(pantalla, jugador, obstaculos)

def dibujar_game_over():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    texto = fuente.render("¡GAME OVER!", True, ROJO)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
    
    fuente_pequena = pygame.font.SysFont(None, 32)
    puntuacion_texto = fuente_pequena.render(f"Puntuación final: {jugador.puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (ANCHO//2 - puntuacion_texto.get_width()//2, ALTO//2 + 50))
    
    mensaje = fuente_pequena.render("Presiona ESPACIO para volver al menú", True, BLANCO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 + 100))

def dibujar_victoria():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    texto = fuente.render("¡VICTORIA!", True, VERDE)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
    
    fuente_pequena = pygame.font.SysFont(None, 32)
    puntuacion_texto = fuente_pequena.render(f"Puntuación final: {jugador.puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (ANCHO//2 - puntuacion_texto.get_width()//2, ALTO//2 + 50))
    
    mensaje = fuente_pequena.render("Presiona ESPACIO para volver al menú", True, BLANCO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 + 100))

# Registrar eventos personalizados
EVENTO_FIN_DISPARO_JUGADOR = pygame.USEREVENT + 1
EVENTO_FIN_DISPARO_NPC = pygame.USEREVENT + 2

# Bucle principal del juego
def ejecutar_juego():
    global estado_juego, nivel_actual
    
    ejecutando = True
    ultimo_tiempo = time.time()
    
    while ejecutando:
        # Calcular tiempo delta para animaciones suaves
        tiempo_actual = time.time()
        delta_tiempo = tiempo_actual - ultimo_tiempo
        ultimo_tiempo = tiempo_actual
        
        # Actualizar todas las animaciones
        sprite_manager.update_animations()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_juego == "menu":
                pos = pygame.mouse.get_pos()
                if boton_iniciar.es_clic(pos):
                    estado_juego = "jugando"
                    nivel_actual = 0
                    iniciar_nivel(nivel_actual)
                elif boton_salir.es_clic(pos):
                    ejecutando = False
            
            # elif evento.type == pygame.KEYDOWN:
            #     if evento.key == pygame.K_ESCAPE:
            #         estado_juego = "menu"
                
            #     if estado_juego in ["game_over", "victoria"] and evento.key == pygame.K_SPACE:
            #         estado_juego = "menu"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
                
                elif evento.key == pygame.K_F1:  # F1 para alternar modo depuración
                    global DEBUG_MODE
                    DEBUG_MODE = not DEBUG_MODE
                    print(f"Modo depuración: {'ACTIVADO' if DEBUG_MODE else 'DESACTIVADO'}")
                
                elif estado_juego in ["game_over", "victoria"] and evento.key == pygame.K_SPACE:
                    estado_juego = "menu"
            
            # Eventos para animaciones de disparo
            elif evento.type == EVENTO_FIN_DISPARO_JUGADOR and jugador:
                jugador.estado = "quieto"
                sprite_manager.play_animation(f"jugador_quieto_{jugador.direccion}", jugador.id)
            
            elif evento.type == EVENTO_FIN_DISPARO_NPC:
                # Encontrar el NPC que disparó por su ID
                for npc in npcs:
                    if evento.entity_id == id(npc):
                        npc.estado = "quieto"
                        sprite_manager.play_animation(f"npc_quieto_{npc.direccion}", npc.id)
                        break
        
        if estado_juego == "menu":
            dibujar_menu()
        
        elif estado_juego == "jugando":
            # Movimiento del jugador
            teclas = pygame.key.get_pressed()
            dx, dy = 0, 0
            if teclas[pygame.K_a]: dx -= jugador.velocidad
            if teclas[pygame.K_d]: dx += jugador.velocidad
            if teclas[pygame.K_w]: dy -= jugador.velocidad
            if teclas[pygame.K_s]: dy += jugador.velocidad
            jugador.mover(dx, dy, obstaculos)
            
            # Disparo del jugador
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                bala = jugador.disparar((mx, my))
                if bala and jugador.estado == "disparando":
                    balas.append(bala)
                    # Programar evento para volver al estado quieto
                    pygame.time.set_timer(EVENTO_FIN_DISPARO_JUGADOR, 200, False)
            
            # Actualizar NPCs
            for npc in npcs:
                npc.actualizar(obstaculos)
                npc_bala = npc.disparar(obstaculos)
                if npc_bala and npc.estado == "disparando":
                    balas.append(npc_bala)
                    # Programar evento para volver al estado quieto
                    evento = pygame.event.Event(EVENTO_FIN_DISPARO_NPC, {'entity_id': id(npc)})
                    pygame.event.post(evento)
            
            # Actualizar balas y verificar colisiones
            balas_para_eliminar = []
            for i, bala in enumerate(balas):
                if not bala.actualizar(obstaculos):
                    balas_para_eliminar.append(i)
                    continue
                
                # Colisión con NPCs
                if bala.es_jugador:
                    for j, npc in enumerate(npcs):
                        if bala.rect.colliderect(npc.rect):
                            npc.vida -= 25
                            balas_para_eliminar.append(i)
                            if npc.vida <= 0:
                                npcs.pop(j)
                                jugador.puntuacion += 100
                            break
                # Colisión con jugador
                elif bala.rect.colliderect(jugador.rect):
                    jugador.vida -= 10
                    balas_para_eliminar.append(i)
                    if jugador.vida <= 0:
                        estado_juego = "game_over"
            
            # Eliminar balas
            for i in sorted(balas_para_eliminar, reverse=True):
                if i < len(balas):
                    balas.pop(i)
            
            # Verificar si se han eliminado todos los NPCs
            if not npcs:
                nivel_actual += 1
                if nivel_actual >= max_niveles:
                    estado_juego = "victoria"
                else:
                    iniciar_nivel(nivel_actual)
            
            dibujar_juego()
        
        elif estado_juego == "game_over":
            dibujar_game_over()
        
        elif estado_juego == "victoria":
            dibujar_victoria()
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    ejecutar_juego()