import pygame
from src.database.db_tool import DbTool
from src.tools.globals.singleton import Singleton


class Display(metaclass=Singleton):

    def __init__(self):
        width = 1280
        height = 960
        self.display_window = pygame.display.set_mode((width, height))

        self.camera_x = DbTool().get_player.x
        self.camera_y = DbTool().get_player.y

        self.single_tiles = 7
        self.both_tiles = self.single_tiles * 2
        self.all_tiles = self.both_tiles + 1

        self.pixels_changer = 64

        self.fields = [field for field in DbTool().get_rows_between(
            ('src.objects.fields', 'Field'), self.query_tuple('x'), self.query_tuple('y'))]
        self.field_type_image = {field_type.id_field_type: pygame.transform.scale2x(pygame.image.load(field_type.image))
                                 for field_type in DbTool().get_all_rows(('src.objects.fields', 'FieldType'))}
        self.item_type_image = {item.id_item: pygame.transform.scale2x(pygame.image.load(item.image))
                                for item in DbTool().get_all_rows(('src.objects.items', 'Item'))}
        self.creatures_images = {creature_type.id_creature_type: pygame.transform.scale2x(pygame.image.load(creature_type.image))
                                 for creature_type in DbTool().get_all_rows(('src.objects.creatures', 'CreatureType'))}
        self.sprite_group_items = pygame.sprite.Group()
        self.sprite_group_creatures = pygame.sprite.Group()

    def reload_sprites(self):
        for item in self.get_items():
            self.sprite_group_items.add(ItemSprite((item.x - self.fields[0].x) * self.pixels_changer,
                                                   (item.y - self.fields[0].y) * self.pixels_changer,
                                                   item.id_bounded_item,
                                                   self.item_type_image[item.item_id]))
        for creature in self.get_creatures():
            self.sprite_group_creatures.add(CreatureSprite((creature.x - self.fields[0].x) * self.pixels_changer,
                                                           (creature.y - self.fields[0].y) * self.pixels_changer,
                                                           creature.id_spawned_creature,
                                                           self.creatures_images[creature.spawned_creature_type_id]))
        self.draw_sprite_group()

    def draw_sprite_group(self):
        self.sprite_group_items.draw(self.display_window)
        self.sprite_group_creatures.draw(self.display_window)
        pygame.display.update()
        self.sprite_group_items = pygame.sprite.Group()
        self.sprite_group_creatures = pygame.sprite.Group()

    def get_items(self):
        return DbTool().get_rows_between(('src.objects.items', 'BoundedItem'),
                                                      (self.fields[0].x, self.fields[-1].x),
                                                      (self.fields[0].y, self.fields[-1].y))

    def get_creatures(self):
        return DbTool().get_rows_between(('src.objects.creatures', 'SpawnedCreature'),
                                                      (self.fields[0].x, self.fields[-1].x),
                                                      (self.fields[0].y, self.fields[-1].y))

    def reload_background(self):
        self.update_camera()
        for index_x in range(self.all_tiles):
            for index_y, field in zip(range(self.all_tiles), self.fields):
                self.display_window.blit(self.field_type_image[field.field_type_id],
                                         (index_y * self.pixels_changer, index_x * self.pixels_changer))
        pygame.display.update()

    def query_tuple(self, axis):
        if axis == "x":
            return self.camera_x - self.single_tiles, self.camera_x + self.single_tiles
        elif axis == "y":
            return self.camera_y - self.single_tiles, self.camera_y + self.single_tiles

    def update_camera(self):
        self.camera_x = DbTool().get_player.x
        self.camera_y = DbTool().get_player.y
        self.fields = [field for field in DbTool().get_rows_between(
            ('src.objects.fields', 'Field'), self.query_tuple('x'), self.query_tuple('y'))]


class ItemSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, id_bounded_item, image):
        pygame.sprite.Sprite.__init__(self)
        self.id_bounded_item = id_bounded_item
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class CreatureSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, id_creature, image):
        pygame.sprite.Sprite.__init__(self)
        self.id_creature = id_creature
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)