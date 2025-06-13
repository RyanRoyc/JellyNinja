import pygame
import random
import math
import numpy as np
from utils.constants import *
from game_states.base_state import BaseState

class Jelly:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 30
        self.vel_x = random.uniform(-6, 6)  # Reduced horizontal speed
        self.vel_y = INITIAL_VELOCITY * random.uniform(0.8, 1.2)  # Randomize initial velocity
        self.squish = 1.0
        self.squish_vel = 0
        self.alive = True
        
    def update(self):
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += GRAVITY
        
        # Bounce off walls
        if self.x < self.radius:
            self.x = self.radius
            self.vel_x *= -0.8
        elif self.x > WINDOW_WIDTH - self.radius:
            self.x = WINDOW_WIDTH - self.radius
            self.vel_x *= -0.8
            
        # Update squish animation
        self.squish += self.squish_vel
        self.squish_vel += (1 - self.squish) * 0.2  # Spring force
        self.squish_vel *= 0.8  # Damping
        
    def draw(self, screen):
        # Draw squished circle
        squished_radius_x = self.radius * (2 - self.squish)
        squished_radius_y = self.radius * self.squish
        pygame.draw.ellipse(screen, self.color,
            (self.x - squished_radius_x, self.y - squished_radius_y,
             squished_radius_x * 2, squished_radius_y * 2))
        
        # Add highlight
        highlight_pos = (
            self.x - squished_radius_x * 0.3,
            self.y - squished_radius_y * 0.3
        )
        pygame.draw.circle(screen, (255, 255, 255), highlight_pos, 5)

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.vel_x = random.uniform(-4, 4)  # Reduced horizontal speed
        self.vel_y = INITIAL_VELOCITY * random.uniform(0.9, 1.1)  # Randomize initial velocity
        self.flash_time = 0
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += GRAVITY
        self.flash_time += 1
        
        # Bounce off walls
        if self.x < self.radius:
            self.x = self.radius
            self.vel_x *= -0.8
        elif self.x > WINDOW_WIDTH - self.radius:
            self.x = WINDOW_WIDTH - self.radius
            self.vel_x *= -0.8
        
    def draw(self, screen):
        # Draw bomb body
        pygame.draw.circle(screen, (30, 30, 30), (self.x, self.y), self.radius)
        
        # Draw fuse
        fuse_start = (self.x, self.y - self.radius)
        fuse_end = (self.x + math.sin(self.flash_time * 0.2) * 10,
                   self.y - self.radius - 15)
        pygame.draw.line(screen, (100, 100, 100), fuse_start, fuse_end, 3)
        
        # Draw flashing effect
        if self.flash_time % 10 < 5:
            pygame.draw.circle(screen, (255, 200, 0),
                             (fuse_end[0], fuse_end[1]), 5)

class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += GRAVITY * 0.5
        self.lifetime -= 1
        
    def draw(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color[:3], alpha)
        surf = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (2, 2), 2)
        screen.blit(surf, (int(self.x - 2), int(self.y - 2)))

class Game(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.reset_game()
        
    def reset_game(self):
        self.jellies = []
        self.bombs = []
        self.particles = []
        self.background_splatters = []  # For splatter effects
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.spawn_timer = 0
        self.difficulty_timer = 0
        self.difficulty_level = 1
        self.screen_shake = 0
        self.mouse_positions = []
        self.is_slicing = False
        self.slice_fade = []  # List of tuples (points, alpha)
        self.time = 0
        
    def spawn_objects(self):
        # Spawn new jellies and bombs based on difficulty
        if random.random() < 0.7:  # 70% chance to spawn something
            x = random.randint(50, WINDOW_WIDTH - 50)
            if random.random() < 0.3 * self.difficulty_level:  # Increased bomb frequency
                self.bombs.append(Bomb(x, WINDOW_HEIGHT + 50))
            else:
                self.jellies.append(Jelly(x, WINDOW_HEIGHT + 50, random.choice(JELLY_COLORS)))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_slicing = True
            self.mouse_positions = [event.pos]  # Start new slice
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_slicing and len(self.mouse_positions) >= 2:
                # Add current trail to fading trails
                self.slice_fade.append((self.mouse_positions.copy(), 255))
            self.is_slicing = False
            self.mouse_positions = []
        elif event.type == pygame.MOUSEMOTION and self.is_slicing:
            self.mouse_positions.append(event.pos)
            if len(self.mouse_positions) > SLICE_TRAIL_LENGTH:
                self.mouse_positions.pop(0)
                
            # Check for slicing only while mouse button is held
            if len(self.mouse_positions) >= 2:
                self.check_slices()
                
    def check_slices(self):
        # Get the last two mouse positions for line segment
        p1 = self.mouse_positions[-2]
        p2 = self.mouse_positions[-1]
        
        sliced_something = False
        
        # Check jellies
        for jelly in self.jellies[:]:
            if self.line_circle_intersection(
                p1, p2, (jelly.x, jelly.y), jelly.radius
            ):
                self.slice_jelly(jelly)
                sliced_something = True
                
        # Check bombs
        for bomb in self.bombs[:]:
            if self.line_circle_intersection(
                p1, p2, (bomb.x, bomb.y), bomb.radius
            ):
                self.trigger_bomb(bomb)
                return  # Game over, no need to check more
                
        # Update combo
        if sliced_something:
            self.combo += 1
            self.combo_timer = COMBO_TIME
            if self.combo >= 3:
                self.score += self.combo * 2  # Bonus points for combo
        
    def line_circle_intersection(self, p1, p2, center, radius):
        # Vector from p1 to center
        cx = center[0] - p1[0]
        cy = center[1] - p1[1]
        
        # Vector from p1 to p2
        vx = p2[0] - p1[0]
        vy = p2[1] - p1[1]
        
        # Length of line segment squared
        l2 = vx*vx + vy*vy
        
        # If points are the same, check if center is within radius of point
        if l2 == 0:
            return (cx*cx + cy*cy) <= radius*radius * 1.5  # Increased hit box slightly
            
        # Dot product of v and center-p1
        t = max(0, min(1, (cx*vx + cy*vy) / l2))
        
        # Point on line closest to circle center
        projection_x = p1[0] + t * vx
        projection_y = p1[1] + t * vy
        
        # Check if closest point is within radius (increased hit box)
        dx = center[0] - projection_x
        dy = center[1] - projection_y
        return (dx*dx + dy*dy) <= radius*radius * 1.5  # Increased hit box
        
    def slice_jelly(self, jelly):
        # Add background splatter effect
        splatter = {
            'pos': (jelly.x, jelly.y),
            'color': jelly.color,
            'size': random.randint(40, 80),
            'alpha': 255
        }
        self.background_splatters.append(splatter)
        
        # Remove the jelly
        if jelly in self.jellies:
            self.jellies.remove(jelly)
            self.score += 1
            
            # Create particle effects
            for _ in range(PARTICLE_COUNT):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 8)
                velocity = (
                    math.cos(angle) * speed,
                    math.sin(angle) * speed
                )
                self.particles.append(
                    Particle(
                        jelly.x, jelly.y,
                        jelly.color,
                        velocity,
                        random.randint(20, 40)
                    )
                )
                
            # Create two smaller jellies
            if jelly.radius > 15:  # Only split if big enough
                for _ in range(2):
                    new_jelly = Jelly(
                        jelly.x + random.uniform(-10, 10),
                        jelly.y + random.uniform(-10, 10),
                        jelly.color
                    )
                    new_jelly.radius = jelly.radius * 0.7
                    new_jelly.vel_x = jelly.vel_x + random.uniform(-5, 5)
                    new_jelly.vel_y = jelly.vel_y + random.uniform(-5, 5)
                    new_jelly.squish = 0.5  # Start squished
                    self.jellies.append(new_jelly)
                    
    def trigger_bomb(self, bomb):
        # Remove the bomb
        if bomb in self.bombs:
            self.bombs.remove(bomb)
            
            # Create explosion particles
            for _ in range(PARTICLE_COUNT * 2):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(5, 15)
                velocity = (
                    math.cos(angle) * speed,
                    math.sin(angle) * speed
                )
                self.particles.append(
                    Particle(
                        bomb.x, bomb.y,
                        (255, 100, 0),
                        velocity,
                        random.randint(30, 60)
                    )
                )
            
            # Trigger screen shake
            self.screen_shake = SHAKE_DURATION
            
            # Update high score and change to game over state
            self.game.high_score.update_high_score(self.score)
            self.game.change_state('game_over')
            
    def update(self):
        self.time += 1/60
        
        # Update timers
        self.spawn_timer += 1/60
        self.difficulty_timer += 1/60
        if self.combo > 0:
            self.combo_timer -= 1/60
            if self.combo_timer <= 0:
                self.combo = 0
                
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1/60
            
        # Spawn new objects
        if self.spawn_timer >= SPAWN_INTERVAL / self.difficulty_level:
            self.spawn_timer = 0
            self.spawn_objects()
                
        # Increase difficulty
        if self.difficulty_timer >= DIFFICULTY_INCREASE_INTERVAL:
            self.difficulty_timer = 0
            self.difficulty_level += 0.5
            
        # Update objects
        for jelly in self.jellies[:]:
            jelly.update()
            # Remove if out of bounds
            if jelly.y > WINDOW_HEIGHT + 100 or jelly.y < -100:
                self.jellies.remove(jelly)
                
        for bomb in self.bombs[:]:
            bomb.update()
            # Remove if out of bounds
            if bomb.y > WINDOW_HEIGHT + 100 or bomb.y < -100:
                self.bombs.remove(bomb)
                
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
        # Update background splatters
        for splatter in self.background_splatters[:]:
            splatter['alpha'] -= 15  # Fade quickly
            if splatter['alpha'] <= 0:
                self.background_splatters.remove(splatter)
                
        # Update fading slice trails
        for i in range(len(self.slice_fade) - 1, -1, -1):
            points, alpha = self.slice_fade[i]
            alpha -= 10  # Fade speed
            if alpha <= 0:
                self.slice_fade.pop(i)
            else:
                self.slice_fade[i] = (points, alpha)
                
    def render(self, screen):
        # Draw animated background
        screen.fill((20, 20, 40))
        
        # Draw background effects
        for x in range(0, WINDOW_WIDTH, 100):
            for y in range(0, WINDOW_HEIGHT, 100):
                color = (
                    int(30 + 20 * math.sin(self.time + x / 200)),
                    int(30 + 20 * math.sin(self.time + y / 150)),
                    int(60 + 20 * math.cos(self.time * 0.7))
                )
                size = 80 + 20 * math.sin(self.time * 1.5 + x / 100)
                pygame.draw.circle(screen, color, (x, y), size)
        
        # Draw background splatters
        for splatter in self.background_splatters:
            surf = pygame.Surface((splatter['size'], splatter['size']), pygame.SRCALPHA)
            color = (*splatter['color'][:3], splatter['alpha'])
            pygame.draw.circle(surf, color, (splatter['size']//2, splatter['size']//2), splatter['size']//2)
            screen.blit(surf, (splatter['pos'][0] - splatter['size']//2, splatter['pos'][1] - splatter['size']//2))
        
        # Apply screen shake
        shake_offset = (0, 0)
        if self.screen_shake > 0:
            shake_offset = (
                random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY),
                random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            )
            
        # Draw fading slice trails
        for points, alpha in self.slice_fade:
            if len(points) >= 2:
                trail_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                for i in range(len(points) - 1):
                    start = points[i]
                    end = points[i + 1]
                    progress = i / (len(points) - 1)
                    color = (255, int(255 * (1 - progress)), int(255 * (1 - progress)), int(alpha * (1 - progress)))
                    pygame.draw.line(trail_surf, color, start, end, 4)
                screen.blit(trail_surf, (0, 0))
        
        # Draw active slice trail
        if self.is_slicing and len(self.mouse_positions) >= 2:
            trail_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            for i in range(len(self.mouse_positions) - 1):
                start = self.mouse_positions[i]
                end = self.mouse_positions[i + 1]
                progress = i / (len(self.mouse_positions) - 1)
                color = (255, 255, 255, int(255 * (1 - progress)))
                pygame.draw.line(trail_surf, color, start, end, 4)
            screen.blit(trail_surf, (0, 0))
            
        # Draw objects with screen shake
        for jelly in self.jellies:
            jelly.x += shake_offset[0]
            jelly.y += shake_offset[1]
            jelly.draw(screen)
            jelly.x -= shake_offset[0]
            jelly.y -= shake_offset[1]
            
        for bomb in self.bombs:
            bomb.x += shake_offset[0]
            bomb.y += shake_offset[1]
            bomb.draw(screen)
            bomb.x -= shake_offset[0]
            bomb.y -= shake_offset[1]
            
        for particle in self.particles:
            particle.x += shake_offset[0]
            particle.y += shake_offset[1]
            particle.draw(screen)
            particle.x -= shake_offset[0]
            particle.y -= shake_offset[1]
            
        # Draw score and combo
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        if self.combo >= 3:
            combo_text = self.font.render(f"Combo x{self.combo}!", True, (255, 200, 0))
            screen.blit(combo_text, (20, 60)) 