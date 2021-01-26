# locals.py
import pygame
import os 
from widgets.Button import create_button_theme 
directory = "data/themes/default/NODE/"
class Antivirus():
    coherence = 50
    strength = 40
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Antivirus_node.png")
    hover_img = pygame.image.load(directory + "Antivirus_node.png")
    theme = create_button_theme(default_img, hover_img)
class FireWall():
    coherence = 50
    strength = 20
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Firewall_node.png")
    hover_img = pygame.image.load(directory + "Firewall_node.png")
    theme = create_button_theme(default_img, hover_img)
class Restorer():
    coherence = 80
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Restorer_node.png")
    hover_img = pygame.image.load(directory + "Restorer_node.png")
    theme = create_button_theme(default_img, hover_img)
class Supressor():
    coherence = 60
    strength = 15
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Antivirus_node.png")
    hover_img = pygame.image.load(directory + "Antivirus_node.png")
    theme = create_button_theme(default_img, hover_img)
    
class SystemCore():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Antivirus_node.png")
    hover_img = pygame.image.load(directory + "Antivirus_node.png")
    theme = create_button_theme(default_img, hover_img)
    
class DataCache():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Data_Cache.png")
    hover_img = pygame.image.load(directory + "Data_Cache.png")
    theme = create_button_theme(default_img, hover_img)

class PolymorphicShield():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Polymorphic_shield.png")
    hover_img = pygame.image.load(directory + "Polymorphic_shield.png")
    theme = create_button_theme(default_img, hover_img)

class SecondaryVector():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Secondary_vector.png")
    hover_img = pygame.image.load(directory + "Secondary_vector.png")
    theme = create_button_theme(default_img, hover_img)
    
class SelfRepair():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Self_repair.png")
    hover_img = pygame.image.load(directory + "Self_repair.png")
    theme = create_button_theme(default_img, hover_img)
    
class KernelRot():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    
    default_img = pygame.image.load(directory + "Kernel_rot.png")
    hover_img = pygame.image.load(directory + "Kernel_rot.png")
    
    theme = create_button_theme(default_img, hover_img)
    
class DRY():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Dry_node.png")
    hover_img = pygame.image.load(directory + "Dry_node.png")
    theme = create_button_theme(default_img, hover_img)
    
class WET():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Wet_node.png")
    hover_img = pygame.image.load(directory + "Wet_node_hover.png")
    theme = create_button_theme(default_img, hover_img)
 
class HACKED():
    coherence = 70
    strength = 10
    coherence_strength = (coherence, strength)
    default_img = pygame.image.load(directory + "Empty_node.png")
    hover_img = pygame.image.load(directory + "Empty_node.png")
    theme = create_button_theme(default_img, hover_img)
    
dirr = "data/themes/default/message/"

FIREWALL = FireWall()
ANTIVIRUS = Antivirus()
RESTORER = Restorer()
SUPPRESSOR = Supressor()
SYSTEM_CORE = SystemCore()

DATA_CACHE = DataCache()
SELF_REPAIR = SelfRepair()
KERNEL_ROT = KernelRot()
POLYMORPHIC_SHIELD = PolymorphicShield()
SECONDARY_VECTOR = SecondaryVector()

tooltip_dict = {
    HACKED : pygame.image.load(dirr + "transparant.png"),
    WET : pygame.image.load(dirr + "encrypted_node.png"),
    DRY : pygame.image.load(dirr + "transparant.png"),
    None : pygame.image.load(dirr + "transparant.png"),
    
    FIREWALL : pygame.image.load(dirr + "firewall.png"),
    ANTIVIRUS : pygame.image.load(dirr + "anti_virus.png"),
    RESTORER : pygame.image.load(dirr + "transparant.png"),
    SUPPRESSOR : pygame.image.load(dirr + "transparant.png"),
    
    SYSTEM_CORE : pygame.image.load(dirr + "system_core.png"),
    DATA_CACHE : pygame.image.load(dirr + "encrypted_node.png"),
    
    SELF_REPAIR : pygame.image.load(dirr + "utility_subsystem.png"),
    KERNEL_ROT : pygame.image.load(dirr + "utility_subsystem.png"),
    POLYMORPHIC_SHIELD : pygame.image.load(dirr + "utility_subsystem.png"),
    SECONDARY_VECTOR : pygame.image.load(dirr + "utility_subsystem.png"),
}

SECONDARY_VECTOR = SecondaryVector()

ENCRYPTED = DRY()
