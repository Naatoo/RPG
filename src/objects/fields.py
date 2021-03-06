from src.database.db_tool import DbTool
from src.database.tables import FieldTypeTable, FieldTable


class FieldType(FieldTypeTable):

    def __repr__(self):
        fmt = "FieldType(id={}, name={], image={}, accessible={}"
        return fmt.format(self.id_field_type, self.name, self.image, self.accessible)


class Field(FieldTable):
    def __repr__(self):
        fmt = "Field(x={}, y={}. type_name={})"
        return fmt.format(self.x, self.y, self.type.name)

    @property
    def type(self):
        return DbTool().get_one_row_where(('src.objects.fields', 'FieldType', 'id_field_type'), self.field_type_id)
