import itertools

from src.database.db_tool import DbTool
from src.database.tables import CreatureGroupTable, CreatureTypeTable, SpawnedCreatureTable


class CreatureGroup(CreatureGroupTable):

    def __repr__(self):
        fmt = 'CreatureGroup(id={}, name={}, talkative={}, trader={}'
        return fmt.format(self.id_creature_group, self.name, self.talkative, self.trader)


class CreatureType(CreatureTypeTable):

    def __repr__(self):
        fmt = 'CreatureType(id={}, name={}, strength={}, agility={}, type_name={}'
        return fmt.format(self.id_creature_type, self.name, self.strength, self.agility, self.group.name)

    @property
    def group(self):
        return DbTool().get_one_row_where(('src.objects.creatures', 'CreatureGroup', 'id_creature_group'), self.type_id)


class SpawnedCreature(SpawnedCreatureTable):

    def __repr__(self):
        fmt = "SpawnedCreature(id={}, name={}, x={}, y={})"
        return fmt.format(self.id_spawned_creature, self.name if self.name is not None else self.type.name,
                          self.x, self.y)

    def __str__(self):
        fmt = '{} stands on field {},{}'
        return fmt.format(self.custom_name if self.custom_name is not None else self.type.name, self.x, self.y)

    @property
    def type(self):
        return DbTool().get_one_row_where(('src.objects.creatures', 'CreatureType', 'id_creature_type'),
                                          self.spawned_creature_type_id)

    @property
    def equipment(self):
        return DbTool().get_one_row_where(('src.objects.items', 'BoundedItem', 'creature_id'), self.id_spawned_creature)

    @property
    def free_eq_slots(self):
        used_ids = [item.container_slot_id for item in DbTool().get_rows_where(
            ('src.objects.items', 'BoundedItem', 'container_id'), self.equipment.id_bounded_item)]
        return [index for index in range(1, 33) if index not in used_ids]

    def get_fields_around_and_self(self):
        rows = range(self.x - 1, self.x + 2)
        columns = range(self.y - 1, self.y + 2)
        return (coords for coords in itertools.product(rows, columns))
